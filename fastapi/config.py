# mypy: ignore-errors
import re
import os
from typing import Any, Pattern
from pydantic import BaseModel
from sqlalchemy.engine.url import URL
from arq.connections import RedisSettings


class db:
    username = 'root'
    password = 'C7yYPlzTPhBb8GqLTosj'
    host = 'postgres'
    port = 5432
    database = 'ncs_vurn'
    query_sync = None
    query = None

    @classmethod
    def _get_url_object(cls, driver: str):
        return URL(
            driver,
            username=cls.username,
            password=cls.password,
            host=cls.host,
            port=cls.port,
            database=cls.database,
            query=cls.query_sync if driver == 'postgresql' else cls.query
        )

    @classmethod
    def get_async_url(cls):
        return cls._get_url_object('postgresql+asyncpg')

    @classmethod
    def get_async_url_str(cls):
        return cls.get_async_url().render_as_string(hide_password=False).replace('%', '%%')

    @classmethod
    def get_sync_url(cls):
        return cls._get_url_object('postgresql')

    @classmethod
    def get_sync_url_str(cls):
        return cls.get_sync_url().render_as_string(hide_password=False).replace('%', '%%')
    

class redis:
    host = 'redis'
    port = 6379
    password = None
    ssl = None


    @classmethod
    def get_url(cls):
        return f"redis://:{cls.password if cls.password is not None else ''}@{cls.host}:{cls.port}/0"

    @classmethod
    def get_redis_settings(cls):
        return RedisSettings(
            host=cls.host,
            port=cls.port,
            password=cls.password,
            ssl=cls.ssl,
        )


class hypercorn:
    bind_ip = '0.0.0.0'
    bind_port = 8080

class sqlalchemy:
    pool_size = 20
    max_overflow = 9

class CredentialsRules(BaseModel):
    forbidden_patterns: list[Pattern]
    necessary_patterns: list[Pattern]
    length: Any # magic

    def validate_credentials(self, credential: str) -> bool:
        if len(credential) not in self.length:
            return False
        if not all([re.search(pattern, credential) for pattern in self.necessary_patterns]):
            return False

        if any([re.search(pattern, credential) for pattern in self.forbidden_patterns]):
            return False
        return True


class security:
    access_token_expire_minutes = 60 * 24 * 7
    refresh_token_expire_minutes = 60 * 24 * 7
    confirmation_uuid_expire_minutes = 60 * 24
    reset_password_uuid_expire_minutes = 60 * 24
    cooldown_confirmation_uuid_expire_minutes = 2
    cooldown_reset_password_uuid_expire_minutes =2
    private_secret = os.environ.get('RSA').encode('ascii') # TODO: move to vault
    public_secret = os.environ.get('RSA_PUB').encode('ascii')
    algorithm = 'RS256'

    email_rules = CredentialsRules(
        necessary_patterns=[
            r'[^@]+@[^@]+\.[^@]+',
        ],
        forbidden_patterns=[],
        length=range(5, 100),
    )

    password_rules = CredentialsRules(
        necessary_patterns=[
            r'[a-z]',
            r'[A-Z]',
            r'[0-9]',
        ],
        forbidden_patterns=[],
        length=range(6, 18),
    )
