from pydantic import BaseModel


class AuthenticationModel(BaseModel):
    username: str
    password: str


class AuthenticationResponseModel(BaseModel):
    id: int
    username: str


class RegisterNewAuthenticationModel(BaseModel):
    username: str
    password: str
