from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from app.currencies.external_api import (
    check_currencies,
    convert_currency,
    list_of_currencies,
)
from app.currencies.schemas import CurrencyExchange
from app.exceptions import NoSuchCurException, WrongAmountException
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(prefix='/currencies', tags=['Currency Exchange'])


# @cache(expire=60)
@router.get('/list')
async def get_currencies(current_user: Users = Depends(get_current_user)):
    return list_of_currencies()


@router.get('/exchange')
async def exchange(cur_1: str, cur_2: str, amount: float,
                   current_user: Users = Depends(get_current_user)):
    if not check_currencies(cur_1, cur_2):
        raise NoSuchCurException
    if amount < 0:
        raise WrongAmountException
    result = convert_currency(cur_1, cur_2, amount)
    return result.json()
