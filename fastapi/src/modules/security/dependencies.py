from typing import Optional
from fastapi import Depends, Security, HTTPException
from fastapi.security.oauth2 import SecurityScopes
from dependency_injector.wiring import inject, Provide

from ...exceptions import ForbiddenException
from ...containers import Container
from ..users.crud import UserCRUD
from ..users import schema as user_schema
from .auth_schema import oauth2_scheme
from .util import decode_token
from . import schema


async def _get_token_data(
    security_scopes: SecurityScopes,
    token: Optional[str],
    strict: bool = True
): 
    if token is None:
        if strict:
            raise HTTPException(
                    status_code=401,
                    detail='Not authenticated',
                    headers={'WWW-Authenticate': 'Bearer'},
                )
        return None

    token_data = decode_token(token)

    return token_data

async def get_token_data(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
):  
    return await _get_token_data(security_scopes, token)


async def try_get_token_data(
    security_scopes: SecurityScopes,
    token: Optional[str] = Depends(oauth2_scheme),
):  
    return await _get_token_data(security_scopes, token, strict=False)


@inject
async def _get_current_user(
    token_data: Optional[schema.TokenData],
    user_crud: UserCRUD,
):  
    if token_data is None:
        return None
    user = await user_crud.get_by_email(token_data.email)
    
    if not user:
        raise ForbiddenException()

    return user


@inject
async def get_current_user(
    token_data: schema.TokenData = Security(get_token_data, scopes=['me:read']),
    user_crud: UserCRUD = Depends(Provide[Container.user_crud]),
):  
    return await _get_current_user(token_data, user_crud)


@inject
async def try_get_current_user(
    token_data: Optional[schema.TokenData] = Security(try_get_token_data, scopes=['me:read']),
    user_crud: UserCRUD = Depends(Provide[Container.user_crud]),
):  
    return await _get_current_user(token_data, user_crud)
