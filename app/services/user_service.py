import sqlite3
import hashlib
from custom import DB_PATH

def find_user_by_credentials(email, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, email FROM users WHERE email = ? AND password = ?", (email, password_hash))
    user = cursor.fetchone()

    conn.close()

    if user:
        return {
            "id": user[0],
            "email": user[1]
        }
    else:
        return None

def create_user(email, password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()   
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))

        # Insert new user
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password_hash))
        conn.commit()
        conn.close()

def get_user(id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE id = ?", (id))
    user = cursor.fetchone()

    conn.close()
    
    if user:
        return {
            "id": user[0]
        }
    else:
        return None