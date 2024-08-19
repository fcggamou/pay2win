import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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


class Transaction(BaseModel):
    user_name: str
    message: str = None
    amount: float


# In-memory storage (for simplicity)
transactions = []


@app.get("/api/addresses")
def generate_address():
    return {"address": str(uuid.uuid4())}  # Simulating a unique address


@app.post("/api/transactions")
def submit_transaction(transaction: Transaction):
    transactions.append(transaction.dict())
    return {"status": "success", "transaction": transaction}


@app.get("/api/leaderboard")
def leaderboard():
    sorted_transactions = sorted(transactions, key=lambda x: x['amount'], reverse=True)
    return {"leaderboard": sorted_transactions[:10]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=7000)
