from fastapi import APIRouter, Depends, HTTPException, Response

from app.exceptions import IncorrectEmailOrPasswordException, UserAlreadyExistsException
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import SUserAuth

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/register')
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)
    return 'User registered successfully'


@router.post('/login')
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie('exchange_access_token', access_token, httponly=True)
    return 'Welcome!'


@router.post('/logout')
async def logout_user(response: Response, current_user: Users = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401)
    response.delete_cookie('exchange_access_token')
    return 'Goodbye'


@router.get('/me')
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user.email