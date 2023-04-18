from ...base_classes import ApplicationService
from ...exceptions import NotFoundException, BadRequestException
from .crud import QuestionCRUD
from . import schema

from result import Ok, Err

import config

class QuestionService(ApplicationService):
    def __init__(
        self, 
        question_crud: QuestionCRUD
    ):
        self._question_crud = question_crud

    async def create(self, dto: schema.CreateQuestionDTO):
        return Ok(await self._question_crud.create(dto))
    
    async def get_recent(self, page: int, page_size: int):
        return Ok(await self._question_crud.get_recent(page, page_size))
