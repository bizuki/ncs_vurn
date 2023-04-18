from ...base_classes import ApplicationService
from ...exceptions import NotFoundException, BadRequestException
from .crud import UserCRUD
from . import schema

from result import Ok, Err

import config

class UserService(ApplicationService):
    def __init__(
        self, 
        user_crud: UserCRUD
    ):
        self._user_crud = user_crud

    async def get_by_id(self, id: int):
        user = await self._user_crud.get(id)

        if user is None:
            return Err(NotFoundException())
        
        return Ok(schema.UserDTO(**user.dict()))

    async def get_by_email(self, email: str):
        user = await self._user_crud.get_by_email(email)

        if user is None:
            return Err(NotFoundException())
        
        return Ok(schema.UserDTO(**user.dict()))
    
    async def transfer_money(self, user: schema.User, target: str, sum: float):
        if user.balance < sum:
            return Err(BadRequestException(context={'message': 'Not enough money'}))
        
        target_user = await self._user_crud.get_by_email(target)

        if target_user is None:
            return Err(NotFoundException(context={'message': 'Target user is not exists'}))

        await self._user_crud.transfer(user.email, target, sum)

        return Ok('ok')
