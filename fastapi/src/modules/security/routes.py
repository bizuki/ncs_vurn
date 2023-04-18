from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm 
from dependency_injector.wiring import inject, Provide

from ...containers import Container
from ...util import handled_result_async
from ..users import schema as user_schema
from .service import SecurityService
from . import schema

router = APIRouter(prefix='/security', tags=['security'])


@router.post('/token', response_model=schema.Token, tags=['login', 'token'])
@handled_result_async
@inject
async def issue_token(
    form_data: OAuth2PasswordRequestForm  = Depends(),
    service: SecurityService = Depends(Provide[Container.security_service]),
):
    async with service() as s:
        res = await s.issue_tokens(form_data)

    return res


@router.post('/refresh', response_model=schema.Token, tags=['login', 'token'])
@handled_result_async
@inject
async def issue_refresh_token(
    token: schema.Token,  # optionally create new model for refresh token only
    service: SecurityService = Depends(Provide[Container.security_service]),
):
    async with service() as s:
        res = await s.issue_tokens_by_refresh_token(token.refresh_token)
    
    return res


@router.post('/register', response_model=user_schema.UserDTO, tags=['login', 'email'])
@handled_result_async
@inject
async def create_user(
    user: user_schema.CreateUserDTO,
    service: SecurityService = Depends(Provide[Container.security_service])
):
    async with service() as s:
        res = await s.register_user(user)
    return res
