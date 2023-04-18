from pydantic import BaseModel

class Token(BaseModel):
    refresh_token: str
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str