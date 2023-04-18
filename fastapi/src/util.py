from result import Result
from typing import Any, Iterable, TypeVar
from arq import create_pool

import functools

import config


# function to be used to convert row/mapped instance to a dto
def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = getattr(row, column.name)

    return d


def handle_result(res: Result[Any, Exception]):
    if not res.is_ok():
        raise res.value
    return res.value


# TODO: make the decorator work for both async and sync functions
def handled_result_async(f):
    @functools.wraps(f)
    async def wrapper(*args, **kwargs):
        res = await f(*args, **kwargs)
        return handle_result(res)
    return wrapper


T = TypeVar('T')


def batch(iterable: Iterable[T], n: int = 1):
    iterator = iter(iterable)
    
    while True:
        items: list[T] = []
        for _ in range(n):
            item = next(iterator, None)
            if item is None:
                yield items
                return
            
            items.append(item)
        yield items


def get_arq():
    return create_pool(config.redis.get_redis_settings())
