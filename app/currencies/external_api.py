from requests import Response, get

from app.config import settings
from app.currencies.schemas import CurrencyExchange

API_KEY_CURRENCY = settings.API_KEY
URL = 'https://api.apilayer.com/currency_data/'
headers = {'apikey': API_KEY_CURRENCY}


def list_of_currencies():
    response: Response = get(url=URL + 'list', headers=headers, data={})
    currencies = response.json()['currencies']
    return currencies


def check_currencies(cur_1, cur_2):
    currency_lst = list_of_currencies()
    result = all([cur_1.upper() in currency_lst, cur_2 in currency_lst])
    return result


def convert_currency(cur_1, cur_2, amount):
    url = URL + f'convert?to={cur_1}&from={cur_2}&amount={amount}'
    response: Response = get(url=url, headers=headers, data={})
    return response

