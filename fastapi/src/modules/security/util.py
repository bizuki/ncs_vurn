from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from uuid import uuid4

import config

from ...exceptions import UnauthorizedException
from .schema import TokenData

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    
def validate_credentials(credential: str, rules: config.CredentialsRules):
    if not rules.validate_credentials(credential):
        raise UnauthorizedException(context={'message': 'invalid credentials'})
    
    
def verify_password(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)

def get_password_hash(password: str):
    return pwd_context.hash(password)

# try to decode token
def decode_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, config.security.public_secret, algorithms=[config.security.algorithm])        
        
        email: str = payload.get('sub')
        if not email:
            raise JWTError()
        
        return TokenData(
            email=email,
        )
    except JWTError:
        raise UnauthorizedException()

def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy() 

    expire = datetime.utcnow() + expires_delta
    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(to_encode, config.security.private_secret, algorithm=config.security.algorithm)
    return encoded_jwt

def generate_tokens(data: dict) -> tuple[str, str]:
    data.update({'jti': uuid4().hex})
    access_token = create_token(
        data,
        expires_delta=timedelta(minutes=config.security.access_token_expire_minutes)
    )
    refresh_token = create_token(
        data,
        expires_delta=timedelta(minutes=config.security.refresh_token_expire_minutes)
    )
    return access_token, refresh_token
