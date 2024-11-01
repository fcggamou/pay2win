
from decimal import Decimal
from typing import Dict, List, Union

from api_models import CreateTransactionRequest
from blockchain import eth
from blockchain.factory import get_crypto_client
from blockchain.pricing import to_usd
from db import fetch_leaderboard, get_db, insert_transaction
from encryption import encrypt
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import get_currency
from pydantic import BaseModel

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LeaderboardEntryResponse(BaseModel):
    user_name: str
    message: str
    amount: float


@app.post("/api/transactions")
def submit_transaction(transaction: CreateTransactionRequest, db=Depends(get_db)) -> Dict[str, Union[str, int]]:
    try:
        crypto_client = get_crypto_client(transaction.blockchain_network)
        blockchain_address = crypto_client.generate_crypto_address()
        encrypted_private_key = encrypt(blockchain_address.private_key)
        currency = get_currency(transaction.blockchain_network)

        transaction_id = insert_transaction(
            db,
            transaction.user_name,
            Decimal(0),
            currency,
            Decimal(0),
            transaction.message,
            blockchain_address.address,
            transaction.blockchain_network,
            encrypted_private_key,

        )
        return {"status": "success", "transaction_id": transaction_id, "blockchain_address": blockchain_address.address}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing transaction: {e}")


@app.get("/api/leaderboard", response_model=List[LeaderboardEntryResponse])
def leaderboard(db=Depends(get_db)) -> List[LeaderboardEntryResponse]:
    try:
        leaderboard_entries = fetch_leaderboard(db)
        return [LeaderboardEntryResponse(user_name=entry.user_name, message=entry.message, amount=entry.amount) for entry in leaderboard_entries]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching leaderboard: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=7001)
