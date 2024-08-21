from contextlib import contextmanager
from datetime import datetime
from decimal import Decimal
from typing import Generator, List

import psycopg2
from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
from models import (BlockchainNetwork, Currency, LeaderboardEntry, Transaction,
                    TransactionStatus)
from psycopg2.extensions import connection as _connection


def get_db_connection() -> _connection:
    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return connection


def get_db() -> Generator[_connection, None, None]:
    db = get_db_connection()
    try:
        yield db
    finally:
        if db:
            db.close()


@contextmanager
def get_db_context():
    db = get_db_connection()
    try:
        yield db
    finally:
        if db:
            db.close()


def insert_transaction(
    connection: _connection,
    user_name: str,
    amount: Decimal,
    currency: Currency,
    usd_amount: Decimal,
    message: str,
    blockchain_address: str,
    blockchain_network: BlockchainNetwork,
    private_key: str
) -> int:
    try:
        with connection.cursor() as cursor:
            query = """
                INSERT INTO transactions (amount, user_name, currency, amount_usd, message, blockchain_address, blockchain_network, status, private_key, created_at)
                VALUES (%(amount)s, %(user_name)s, %(currency)s, %(amount_usd)s, %(message)s, %(blockchain_address)s, %(blockchain_network)s, %(status)s, %(private_key)s, %(created_at)s)
                RETURNING id;
            """
            params = {
                'user_name': user_name,
                'amount': amount,
                'currency': currency.value,
                'amount_usd': usd_amount,
                'message': message,
                'blockchain_address': blockchain_address,
                'blockchain_network': blockchain_network.value,
                'status': TransactionStatus.PENDING.value,
                'private_key': private_key,
                'created_at': datetime.now()
            }
            cursor.execute(query, params)
            transaction_id = cursor.fetchone()[0]
            connection.commit()
        return transaction_id
    except Exception as e:
        raise Exception(f"Error processing transaction: {e}")


def fetch_pending_transactions(connection: psycopg2.extensions.connection) -> List[Transaction]:

    with connection.cursor() as cursor:
        query = """
                SELECT id, blockchain_address, blockchain_network
                FROM transactions
                WHERE status = %(status)s;
            """
        cursor.execute(query, {'status': TransactionStatus.PENDING.value})
        pending_transactions = cursor.fetchall()
    return [Transaction(row[0], row[1], BlockchainNetwork(row[2])) for row in pending_transactions]


def update_transaction(
    connection: _connection,
    transaction_id: int,
    status: TransactionStatus,
    amount: Decimal,
    usd_amount: Decimal
) -> None:
    try:
        with connection.cursor() as cursor:
            update_query = """
                UPDATE transactions
                SET status = %(status)s, amount = %(amount)s, amount_usd = %(usd_amount)s
                WHERE id = %(transaction_id)s;
            """
            cursor.execute(update_query, {'transaction_id': transaction_id, 'status': status.value, 'amount': amount, 'usd_amount': usd_amount})
            connection.commit()
    except Exception as e:
        connection.rollback()
        raise Exception(f"Error updating transaction {transaction_id} status: {e}")


def fetch_leaderboard(connection: _connection) -> List[LeaderboardEntry]:

    with connection.cursor() as cursor:
        query = """
                SELECT user_name, message, amount_usd
                FROM transactions
                WHERE status = %(status)s
                ORDER BY amount_usd DESC
                LIMIT 100;
            """
        cursor.execute(query, {'status': TransactionStatus.COMPLETED.value})
        rows = cursor.fetchall()
        leaderboard = [LeaderboardEntry(row[0], row[1], row[2])for row in rows]
    return leaderboard
