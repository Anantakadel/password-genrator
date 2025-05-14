import sqlite3
from cryptography.fernet import Fernet
import secrets
import string
import os

DB_FILE ="password_manager.db"
KEY_FILE ="encryption.key"

#load or generate encryption key
def load_key():
    if not os.path.exist(KEY_FILE)
       with open(KEY_FILE, "wb") as key_file:
           key = Fernet.generate_key()
            key_file.write(key)
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

#encrypt and decrypt function
def encrypt(text,cypher):
    return cypher.encrypt(text.encode()).decode()

def decrypt(text,cypher):
    return cypher.decrypt(text.encode()).decode()

#genarating random password
def generate_password(length=10):
    return ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(length))

#database initialization
def init_db():
    with sqlite3.connect(DB_FILE) as conn: