from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Transaction:
    def __init__(self, id: int, blockchain_address: str, blockchain_network: str):
        self.id = id
        self.blockchain_address = blockchain_address
        self.blockchain_network = blockchain_network


class LeaderboardEntry:
    def __init__(self, address: str, amount: float):
        self.address = address
        self.amount = amount


class BlockchainNetwork(Enum):
    ETH_MAINNET = "eth_mainnet"
    ETH_SEPOLIA = "eth_sepolia"
    BTC_MAINNET = "bitcoin_mainnet"
    BTC_TESTNET = "bitcoin_testnet"
    FIAT = "fiat"


class TransactionStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class LeaderboardEntry:
    def __init__(self, user_name: str, message: Optional[str], amount: float):
        self.user_name = user_name
        self.message = message
        self.amount = amount


class Currency(Enum):
    ETH = "eth"
    BTC = "btc"
    USD = "usd"


class CryptoAddress:
    def __init__(self, address, private_key):
        self.address = address
        self.private_key = private_key


def get_currency(network: BlockchainNetwork) -> Currency:
    if network in [BlockchainNetwork.ETH_MAINNET, BlockchainNetwork.ETH_SEPOLIA]:
        return Currency.ETH
    elif network in [BlockchainNetwork.BTC_MAINNET, BlockchainNetwork.BTC_TESTNET]:
        return Currency.BTC
    elif network == BlockchainNetwork.FIAT:
        return Currency.USD
    else:
        raise ValueError("Invalid blockchain network")
