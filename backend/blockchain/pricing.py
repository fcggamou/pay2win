from decimal import Decimal

from config import CRYPTO_COMPARE_API_KEY
from cryptocompare import cryptocompare
from models import Currency

cryptocompare._set_api_key_parameter(CRYPTO_COMPARE_API_KEY)


def to_usd(amount: Decimal, currency: Currency):
    if currency == Currency.USD:
        return amount
    price = get_usd_price(currency)
    return amount * price


def get_usd_price(currency: Currency):
    data = cryptocompare.get_price(currency.value, currency='USD')
    return Decimal(data[currency.value.upper()]['USD'])
