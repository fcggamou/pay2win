from abc import abstractmethod
from decimal import Decimal

from models import BlockchainNetwork, CryptoAddress


class CryptoClient():

    @abstractmethod
    def generate_crypto_address(self) -> CryptoAddress:
        pass

    def get_balance(self, address: str, network: BlockchainNetwork) -> Decimal:
        pass
