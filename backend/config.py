import os

from dotenv import load_dotenv
from models import BlockchainNetwork

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

ETH_SEPOLIA_RPC_URL = os.getenv('ETH_SEPOLIA_RPC_URL')
ETH_MAINNET_RPC_URL = os.getenv('ETH_MAINNET_RPC_URL')
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')

CRYPTO_COMPARE_API_KEY = os.getenv('CRYPTO_COMPARE_API_KEY')


def get_rpc_url(network: BlockchainNetwork) -> str:
    if network == BlockchainNetwork.ETH_MAINNET:
        return ETH_MAINNET_RPC_URL
    elif network == BlockchainNetwork.ETH_SEPOLIA:
        return ETH_SEPOLIA_RPC_URL
    else:
        raise ValueError("Invalid blockchain network")
