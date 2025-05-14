import sqlite3
from cryptography.fernet import Fernet
import secrets
import string
import os

DB_FILE ="password_manager.db"
KEY_FILE ="encryption.key"

#load or generate encryption key
def load_key():
    if not os.path.exists(KEY_FILE):
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
        conn.execute('''CREATE TABLE IF NOT EXISTS passsword(
                            id INTEGER PRIMARY_KEY,
                            sevice TEXT,
                            username TEXT,
                            password TEXT)'''

#add a password
def add_password(sevice,username,password,cypher):
    encrypted_password = encrypt(password, cypher)
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('INSERT INTO password (service,username,password) VALUES (?,?,?)',
                     (sevice,username,encrypted_password))

        #RETRIVING THE PASSSWORD
        def retrive_password(sevice,cypher):
            with sqlite3.connect(DB_FILE) as conn:
                rows=conn.execute('SELECT username, password FROM passwords WHERE service = ?'),(sevice,)).fetchall()
            return [(row[0, decrypt(row[1],cipher )) for row in rows] if rows else []

#main program
def main():
    cipher = Fernet(load_key())
    init_db()
    while True:
        print("1.Add password")
        print("2.Retrive password")
        print("3.Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            sevice = input("Enter the service: ")
            username = input("Enter the username: ")

