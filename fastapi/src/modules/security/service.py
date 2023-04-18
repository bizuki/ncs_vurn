from arq import ArqRedis
from result import Ok, Err
from fastapi.security import OAuth2PasswordRequestForm 

from ...base_classes import ApplicationService
from ..users import schema as users_schema
from ..users.crud import UserCRUD
from ...exceptions import BadRequestException, UnauthorizedException
from . import schema
from .util import *

import config


class SecurityService(ApplicationService):
    def __init__(self, user_crud: UserCRUD, arq: ArqRedis):
        self._user_crud = user_crud
        self._arq = arq

    async def register_user(self, user: users_schema.CreateUserDTO):
        if await self._user_crud.get_by_email(user.email):
            raise BadRequestException(
                context={'message': 'This email already used'}
            )

        validate_credentials(user.email, config.security.email_rules)
        validate_credentials(user.password, config.security.password_rules)
        
        user.password = get_password_hash(user.password)
        new_user = await self._user_crud.create(user)
        
        return Ok(users_schema.UserDTO(**new_user.dict()))
    
    async def authenticate_user(self, email: str, password: str):
        user = await self._user_crud.get_by_email(email)
        
        if not user or not verify_password(password, user.password):
            return Err(UnauthorizedException(
                context={'message': 'Invalid username or password'}
            ))

        return Ok(user)

    async def issue_tokens(self, form_data: OAuth2PasswordRequestForm):
        user = await self.authenticate_user(form_data.username, form_data.password)
        
        if user.is_err():
            return user
        user = user.unwrap()

        access_token, refresh_token = generate_tokens(
            data={
                'sub': user.email
            }
        )

        # TODO: make arq task to delete expired token (enqueue it on expiration date)
        await self._arq.sadd(f'tokens:{user.email}', refresh_token)

        return Ok(schema.Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type='bearer'
        ))

    async def issue_tokens_by_refresh_token(self, refresh_token: str):
        token = decode_token(refresh_token)
        
        is_valid = await self._arq.sismember(f'tokens:{token.email}', refresh_token)
        
        if not is_valid:
            raise UnauthorizedException(context={'message': 'Invalid token'})

        access_token, new_refresh_token = generate_tokens(
            data={
                'sub': token.email,
            }
        )
        
        async with self._arq.pipeline() as trx:
            trx = trx.srem(f'tokens:{token.email}', refresh_token)
            trx = trx.sadd(f'tokens:{token.email}', new_refresh_token)
            await trx.execute()
        
        return Ok(schema.Token(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type='bearer'
        ))
