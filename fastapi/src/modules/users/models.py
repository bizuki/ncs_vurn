from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql.functions import current_timestamp

from ...db import ModelBase


class User(ModelBase):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())

    balance = Column(Float, nullable=False, server_default='50.0')
