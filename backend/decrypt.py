from decimal import Decimal

from blockchain.pricing import get_usd_price, to_usd
from encryption import decrypt
from models import Currency

print(decrypt('gAAAAABmxlPDQgSxGwUyv8_IXyvBlpDlve6MurhsiC1In1rEZiMYk1xzNKrDEonIUHR6XsR3GRIX6POEqDYTj35Ur7F4_MhTGt3ShB0ODdXIkBp8DZ58HQKoEKDY_0Z4f-haSDPhknHc1oNAbjrSanjAkCVrmukSNBK8dEuU0YPuqEEtf8fexRE='))
print(get_usd_price(Currency.BTC))
print(to_usd(Decimal('1000'), Currency.ETH))
