import asyncio
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from copy import deepcopy
from result import Result
from typing import Awaitable, Callable, Iterable, Optional, Any, Generic, Type, TypeVar, List, get_args
from pydantic import BaseModel
from pydantic.generics import GenericModel
from pydantic.utils import sequence_like
from sqlalchemy import distinct
from sqlalchemy.sql.selectable import Select, GenerativeSelect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import func
import math

from .db import ModelBase

import config

GenericORMModel = TypeVar('GenericORMModel', bound=ModelBase)

class OrderConfig(BaseModel):
    ordered: bool
    use_secondary: bool
    secondary_table: Optional[Type[ModelBase]]
    column_name: Optional[str]


class ORMModel(Generic[GenericORMModel], GenericModel):
    __exclude__: set[str] = set()
    __orm_model__: Optional[type[GenericORMModel]] = None

    # some generic shananigans
    def _get_type(self):
        return get_args(self.__orig_bases__[0])[0]

    def _to_model(self, value, **kwargs):
        if isinstance(value, ORMModel):
            return value.to_model(**kwargs)
        elif isinstance(value, BaseModel):
            raise ValueError(f"Can't create model from `BaseModel` of {value}")
        elif sequence_like(value):
            return [self._to_model(v, **kwargs) for v in value]
        elif isinstance(value, dict):
            return {k: self._to_model(v, **kwargs) for k, v in value.items()}
        else:
            return value

    def to_model(self, **kwargs) -> GenericORMModel:
        if self.__orm_model__ is None:
            type(self).__orm_model__ = self._get_type()

        d = deepcopy(self.__dict__)

        values: dict[str, Any] = {}
        values.update({name: self._to_model(value, **kwargs) for name, value in d.items() if name not in self.__exclude__})
        
        assert self.__orm_model__, 'Need to specify __orm_model__ to use method `to_model`'
        
        return self.__orm_model__(**values)


    class Config:
        orm_mode = True


SchemaT = TypeVar('SchemaT', bound=ORMModel)
SchemaK = TypeVar('SchemaK', bound=ORMModel)
T = TypeVar('T')


class Pagination(GenericModel, Generic[T]):
    page: int
    page_size: int
    pages_count: int
    count: int
    items: List[T]

    def __iter__(self):
        return iter(self.items)


def cast_pagination(pagination: Pagination[SchemaT], schema: Type[SchemaK]):
    return Pagination[schema](
        **pagination.dict(exclude={'items'}),
        items=[schema(**item.dict()) for item in pagination]
    )


class Email(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_email

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            examples=['some.email@gmail.ru', 'myemaillolO234..dsa@g.ey'],
        )

    @classmethod
    def validate_email(cls, email: str) -> str:
        if email and not config.security.email_rules.validate_credentials(email):
            raise ValueError('invalid email number')

        return cls(email)


def _generate_count_stmt(stmt, distinct_on=None):
    if distinct_on:
        cnt_f = func.count(distinct(distinct_on))
    else:
        cnt_f = func.count()
    return stmt.order_by(None).with_only_columns(cnt_f, maintain_column_froms=True)


class ApplicationCRUD:
    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]):
        self.session_factory = session_factory

    async def execute(self, stmt):
        async with self.session_factory() as db:
            res = await db.execute(stmt)

        return res

    async def _count(self, session, stmt, distnict_on=None) -> int:
        return (await session.execute(_generate_count_stmt(stmt, distnict_on))).scalars().one()

    async def count(self, stmt, distnict_on=None) -> int:
        async with self.session_factory() as session:
            return await self._count(session, stmt, distnict_on)

    async def create_pagination(
        self,
        stmt: GenerativeSelect,
        page: int,
        page_size: int,
        schema: Type[T],
        mapper: Callable[[Any], T] = lambda x: x
    ):
        count = await self.count(stmt)

        result = (await self.execute(stmt.limit(page_size).offset((page - 1) * (page_size)))).fetchall()
        result = list(map(mapper, result))
        return Pagination[schema](
            items=result,
            page_size=page_size,
            page=page,
            pages_count=math.ceil(count / page_size),
            count=count
        )

    # can't work with distinct properly and with only one distinct_on argument
    async def create_orm_pagination(
        self,
        stmt: Select,
        page: int,
        page_size: int,
        schema: Type[SchemaT],
        model: Optional[Type[ModelBase]] = None,
        distinct_on=None,
        mapper: Optional[Callable[[Any], SchemaT]] = None
    ):
        async with self.session_factory() as session:
            count = await self._count(session, stmt, distinct_on)

            if distinct_on:
                stmt = stmt.distinct(distinct_on)

            items = (await session.execute(stmt.limit(page_size).offset((page - 1) * page_size))).all()

            result = list(map(schema.from_orm if mapper is None else mapper, map(lambda x: x[model.__name__] if model else x[0], items)))

        return Pagination[schema](
            items=result,
            page_size=page_size,
            page=page,
            pages_count=math.ceil(count / page_size),
            count=count
        )


T = TypeVar('T')

def coalesce(a: Optional[T], b: Optional[T]):
    if a is not None:
        return a
    
    return b


async def _default_callback(model):
    return model


class ApplicationService:
    @asynccontextmanager
    async def __call__(self, *args, **kwargs):
        await self._mount(*args, **kwargs)
        closed = False
        try:
            yield self
        except Exception as exc:
            if not closed:
                await self._unmount(exc)
                closed = True
            raise exc
        finally:
            if not closed:
                await self._unmount(None)
                closed = True

    async def _mount(self, *args: Any, **kwargs: Any) -> None:
        pass

    async def _unmount(self, exc: Optional[Exception]) -> None:
        pass

    @staticmethod
    async def process_pagination(
        pagination: Callable[[int, int], Awaitable[Iterable[T]]],
        callback: Callable[[T], Awaitable[T]] = _default_callback,
        page_size: int = 10,
    ) -> list[T]:
        """
            Will go throgh all pagination by some batch and will process
            every entity in process. Very usefull, when we want to process all entities from database,
            without loading everything in memory
            Args:
                page_size - length of batch
                pagination - function that will get batch of new entities from db. Signature will be like this func(page: int, page_size: int)
                callback - main function of processing. Takes entity returned by pagination and will process it. By the end of function
                           should return entity.
            Returns list of processed entities returned by callback
        """
        processed = []
        page = 1

        while True:
            items = (await pagination(page, page_size))
            futures = [callback(item) for item in items]
            if not futures:
                return processed

            processed.extend(await asyncio.gather(*futures))
            page += 1


    def process_errors(self, results: Iterable[Result]):
        if any([result.is_err() for result in results]):
            return next(filter(lambda result: result.is_err(), results))
