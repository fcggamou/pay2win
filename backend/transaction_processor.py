import time
from typing import List

from blockchain.factory import get_crypto_client
from blockchain.pricing import to_usd
from db import fetch_pending_transactions, get_db_context, update_transaction
from models import Transaction, TransactionStatus, get_currency


def check_balance_and_update_transaction(connection, transaction: Transaction) -> None:
    try:
        transaction_id = transaction.id
        blockchain_address = transaction.blockchain_address
        blockchain_network = transaction.blockchain_network
        crypto_client = get_crypto_client(blockchain_network)
        amount = crypto_client.get_balance(blockchain_address, blockchain_network)

        if amount > 0:
            currency = get_currency(blockchain_network)
            usd_amount = to_usd(amount, currency)
            update_transaction(connection, transaction_id, TransactionStatus.COMPLETED, amount, usd_amount)

    except Exception as e:
        print(f"Error processing transaction {transaction_id}: {e}")


def process_pending_transactions() -> None:
    try:
        while True:
            with get_db_context() as connection:
                pending_transactions: List[Transaction] = fetch_pending_transactions(connection)

                for transaction in pending_transactions:
                    check_balance_and_update_transaction(connection, transaction)

                time.sleep(60)
    except Exception as e:
        print(f"Error in transaction processing loop: {e}")


if __name__ == "__main__":
    process_pending_transactions()
