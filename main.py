import sqlite3
from cryptography.fernet import Fernet
import secrets
import string
import os

DB_FILE = "password_manager.db"
KEY_FILE = "encryption.key"

# Load or generate encryption key
def load_key():
    if not os.path.exists(KEY_FILE):
        with open(KEY_FILE, "wb") as key_file:
            key = Fernet.generate_key()
            key_file.write(key)
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

# Encrypt and decrypt functions
def encrypt(text, cipher):
    return cipher.encrypt(text.encode()).decode()

def decrypt(text, cipher):
    return cipher.decrypt(text.encode()).decode()

# Generating random password
def generate_password(length=10):
    return ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(length))

# Database initialization
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS passwords (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            service TEXT,
                            username TEXT,
                            password TEXT)''')

# Add a password
def add_password(service, username, password, cipher):
    encrypted_password = encrypt(password, cipher)
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('INSERT INTO passwords (service, username, password) VALUES (?, ?, ?)',
                     (service, username, encrypted_password))

# Retrieve password
def retrieve_password(service, cipher):
    with sqlite3.connect(DB_FILE) as conn:
        rows = conn.execute('SELECT username, password FROM passwords WHERE service = ?', (service,)).fetchall()
    return [(row[0], decrypt(row[1], cipher)) for row in rows] if rows else []

# Main program
def main():
    cipher = Fernet(load_key())
    init_db()

    while True:
        print("\n1. Add password")
        print("2. Retrieve password")
        print("3. Generate password")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            service = input("Enter the service: ")
            username = input("Enter the username: ")
            password = input("Enter the password: ")
            add_password(service, username, password, cipher)
            print("🔥 Password added successfully!")

        elif choice == "2":
            service = input("Enter the service to retrieve password: ")
            result = retrieve_password(service, cipher)
            if result:
                for username, password in result:
                    print(f"👤 {username} | 🔐 {password}")
            else:
                print("❌ No password found for this service.")

        elif choice == "3":
            length = int(input("Enter password length: "))
            print("💥 Generated password:", generate_password(length))

        elif choice == "4":
            print("👋 Exiting...")
            break

        else:
            print("⚠️ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
