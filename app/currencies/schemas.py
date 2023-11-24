from pydantic import BaseModel, field_validator

from app.exceptions import WrongAmountException, WrongCurrencyLen


class CurrencyExchange(BaseModel):
    cur_1: str
    cur_2: str
    amount: float = 1

    @field_validator('cur_1')
    def cur_1_validate(cls, cur: str):
        if len(cur) == 3:
            return cur
        else:
            raise WrongCurrencyLen

    @field_validator('cur_2')
    def cur_2_validate(cls, cur: str):
        if len(cur) == 3:
            return cur
        else:
            raise WrongCurrencyLen


