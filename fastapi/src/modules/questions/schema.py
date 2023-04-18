from datetime import datetime

from ...base_classes import ORMModel

from . import models


class CreateQuestionDTO(ORMModel[models.Question]):    
    text: str


class Question(ORMModel):
    id: int
    created_at: datetime
    text: str
