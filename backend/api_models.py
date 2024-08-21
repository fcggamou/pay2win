from models import BlockchainNetwork
from pydantic import BaseModel


class CreateTransactionRequest(BaseModel):
    user_name: str
    message: str = None
    blockchain_network: BlockchainNetwork
