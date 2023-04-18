from typing import Optional

from fastapi import APIRouter, Depends, Security, Request
from dependency_injector.wiring import inject, Provide

from ..security.dependencies import get_token_data, get_current_user
from ..security.schema import TokenData
from ...util import handled_result_async
from ...base_classes import Pagination
from ...containers import Container
from .service import UserService
from . import schema

router = APIRouter(prefix='/users', tags=['closed', 'users'])


@router.get('/me', response_model=schema.UserDTO)
@handled_result_async
@inject
async def get_info_about_me(
    service: UserService = Depends(Provide[Container.user_service]),
    token: TokenData = Security(get_token_data),
):
    async with service() as s:
        res = await s.get_by_email(token.email)
    return res


@router.get('/{id}', response_model=schema.UserDTO)
@handled_result_async
@inject
async def get_by_id(
    id: int,
    service: UserService = Depends(Provide[Container.user_service]),
    token: TokenData = Security(get_token_data),
):
    async with service() as s:
        res = await s.get_by_id(id)
    return res


@router.get('/transfer/{to}/{sum}')
@handled_result_async
@inject
async def transfer_money(
    to: str,
    sum: float,
    service: UserService = Depends(Provide[Container.user_service]),
    user: schema.User = Security(get_current_user),
):
    async with service() as s:
        res = await s.transfer_money(user, to, sum)
    return res


@router.get('/test/{email}')
@handled_result_async
@inject
async def get_test_info(
    email: str,
    service: UserService = Depends(Provide[Container.user_service]),
):
    async with service() as s:
        res = await s.get_by_email(email)
    return res
