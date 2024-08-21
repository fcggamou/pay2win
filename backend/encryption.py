# For simplicity, we assume the key is stored in an environment variable
import os

from config import ENCRYPTION_KEY
from cryptography.fernet import Fernet

cipher_suite = Fernet(ENCRYPTION_KEY)


def encrypt(private_key: str) -> str:
    encrypted_key = cipher_suite.encrypt(private_key.encode())
    return encrypted_key.decode()


def decrypt(encrypted_key: str) -> str:
    decrypted_key = cipher_suite.decrypt(encrypted_key.encode())
    return decrypted_key.decode()
