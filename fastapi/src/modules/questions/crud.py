from sqlalchemy import select, delete, text, or_, and_

from ...base_classes import ApplicationCRUD
from . import schema
from .models import Question


class QuestionCRUD(ApplicationCRUD):
    async def create(self, dto: schema.CreateQuestionDTO):
        async with self.session_factory() as session:
            question = dto.to_model()
            session.add(
                question
            )
            await session.flush()
            new_user = (await session.get(Question, question.id, populate_existing=True))
            assert new_user is not None

            return schema.Question.from_orm(new_user)
        
    async def get_recent(self, page: int, page_size: int):
        stmt = select(Question).order_by(Question.created_at.desc())

        return await self.create_orm_pagination(stmt, page, page_size, schema.Question)
