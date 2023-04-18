from typing import Generic
from datetime import datetime

from ...base_classes import ORMModel, GenericORMModel, Email

from . import models

class CreateUserDTO(ORMModel[models.User]):    
    email: Email
    password: str

    first_name: str
    last_name: str


class UserDTO(ORMModel):
    id: int
    first_name: str
    last_name: str
    email: Email

    balance: float

    created_at: datetime


class UserWithoutDTO(ORMModel):
    id: int
    first_name: str
    last_name: str
    email: Email

    created_at: datetime


class User(ORMModel[GenericORMModel], Generic[GenericORMModel]):
    id: int
    first_name: str
    last_name: str
    email: str
    password: str

    balance: float

    created_at: datetime
