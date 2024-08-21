from decimal import Decimal

from blockchain.crypto_client import CryptoClient
from config import get_rpc_url
from eth_account import Account
from models import BlockchainNetwork, CryptoAddress
from web3 import Web3


class Eth(CryptoClient):
    def __init__(self):
        self._web3_by_network = {}
        networks = [BlockchainNetwork.ETH_SEPOLIA]

        for network in networks:
            rpc = get_rpc_url(network)
            web3 = Web3(Web3.HTTPProvider(rpc))
            if not web3.is_connected():
                raise ConnectionError(f"Failed to connect to the {network.value} network.")
            self._web3_by_network[network] = web3

    def _get_web3(self, network: BlockchainNetwork) -> Web3:
        return self._web3_by_network[network]

    def generate_crypto_address(self) -> CryptoAddress:

        account = Account.create()
        private_key = account.key.hex()
        eth_address = account.address

        return CryptoAddress(eth_address, private_key)

    def get_balance(self, address: str, network: BlockchainNetwork) -> Decimal:
        web3 = self._get_web3(network)

        balance_wei = web3.eth.get_balance(address)
        balance_eth = web3.from_wei(balance_wei, 'ether')

        return balance_eth
