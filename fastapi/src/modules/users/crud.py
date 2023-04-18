from sqlalchemy import select, delete, text

from ...base_classes import ApplicationCRUD
from . import schema
from .models import User


class UserCRUD(ApplicationCRUD):
    async def create(self, dto: schema.CreateUserDTO):
        async with self.session_factory() as session:
            user = dto.to_model()
            session.add(
                user
            )
            await session.flush()
            new_user = (await session.get(User, user.id, populate_existing=True))
            assert new_user is not None

            return schema.User.from_orm(await session.get(User, user.id, populate_existing=True))

    async def get(self, user_id: int):
        stmt = (select(User).where(User.id == user_id))
        res = await self.execute(stmt)
        found = res.fetchone()

        if not found:
            return None

        return schema.User.from_orm(found.User)

    async def get_by_email(self, email: str):
        stmt = text(f'select * from users where email = \'{email}\'')
        res = await self.execute(stmt)
        found = res.first()

        if not found:
            return None

        return schema.User.from_orm(found)

    async def delete_by_id(self, id: int) -> int:
        stmt = (delete(User).where(User.id == id))
        res = await self.execute(stmt)
        
        return res.rowcount

    async def get_all(self, page: int, page_size: int):
        stmt = select(User)
        return await self.create_orm_pagination(stmt, page, page_size, schema.UserDTO, User)
    
    async def transfer(self, source: str, target: str, sum: float):
        async with self.session_factory() as session:
            await session.execute(text(f'update users set balance=balance - {sum} where email = \'{source}\''))
            await session.execute(text(f'update users set balance=balance + {sum} where email = \'{target}\''))
