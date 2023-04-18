from typing import Optional

from fastapi import APIRouter, Depends, Security, Request
from dependency_injector.wiring import inject, Provide

from ..security.dependencies import get_token_data, get_current_user
from ..security.schema import TokenData
from ...util import handled_result_async
from ...base_classes import Pagination
from ...containers import Container
from .service import QuestionService
from . import schema

router = APIRouter(prefix='/questions', tags=['open', 'questions'])


@router.post('/', response_model=schema.Question)
@handled_result_async
@inject
async def create_question(
    dto: schema.CreateQuestionDTO,
    service: QuestionService = Depends(Provide[Container.question_service]),
):
    async with service() as s:
        res = await s.create(dto)
    return res


@router.get('/recent', response_model=Pagination[schema.Question])
@handled_result_async
@inject
async def get_recent_questions(
    page: int = 1,
    page_size: int = 10,
    service: QuestionService = Depends(Provide[Container.question_service]),
):
    async with service() as s:
        res = await s.get_recent(page, page_size)
    return res
