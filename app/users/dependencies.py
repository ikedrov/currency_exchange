from datetime import datetime

from fastapi import Depends, Request
from jose import JWTError, jwt

from app.config import settings
from app.exceptions import (
    IncorrectFormatTokenException,
    NoTokenException,
    NoUserException,
    TokenExpiredException,
)
from app.users.dao import UsersDAO
from app.users.models import Users


def get_token(request: Request):
    token = request.cookies.get('exchange_access_token')
    if not token:
        raise NoTokenException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        raise IncorrectFormatTokenException
    expire: int = payload.get('exp')
    if not expire or int(expire) < datetime.utcnow().timestamp():
        raise TokenExpiredException
    user_id = payload.get('sub')
    if not user_id:
        raise NoUserException
    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise NoUserException
    return user


