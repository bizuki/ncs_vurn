from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.sql.functions import current_timestamp

from ...db import ModelBase


class Question(ModelBase):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, index=True)

    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())

    text = Column(String, nullable=False)
