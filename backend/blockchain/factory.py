
from blockchain.crypto_client import CryptoClient
from blockchain.eth import Eth
from models import BlockchainNetwork


def get_crypto_client(network: BlockchainNetwork) -> CryptoClient:
    if network == BlockchainNetwork.ETH_MAINNET:
        return Eth()
    elif network == BlockchainNetwork.ETH_SEPOLIA:
        return Eth()
    else:
        raise ValueError("Invalid blockchain network")
