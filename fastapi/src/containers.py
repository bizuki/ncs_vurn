from dependency_injector import containers, providers

from .db import Database
from .util import get_arq
from .modules.users.crud import UserCRUD
from .modules.users.service import UserService
from .modules.questions.crud import QuestionCRUD
from .modules.questions.service import QuestionService
from .modules.security.service import SecurityService


import config


class Container(containers.DeclarativeContainer):
    db = providers.Singleton(Database, db_url=config.db.get_async_url())
    arq = providers.Singleton(get_arq)

    user_crud = providers.Factory(
        UserCRUD,
        session_factory=db.provided.session
    )

    question_crud = providers.Factory(
        QuestionCRUD,
        session_factory=db.provided.session
    )

    user_service = providers.Factory(
        UserService,
        user_crud=user_crud,
    )

    question_service = providers.Factory(
        QuestionService,
        question_crud=question_crud
    )

    security_service = providers.Factory(
        SecurityService,
        user_crud=user_crud,
        arq=arq
    )
