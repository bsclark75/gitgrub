import hashlib
import os
import sqlite3
from custom import DB_PATH

def init_db(connection):

    cursor = connection.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            ingredients TEXT,
            steps TEXT,
            notes TEXT,
            tags TEXT,
            user_id INTEGER,
            forked_from INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(forked_from) REFERENCES recipes(id)
        )
    ''')

    # Seed user if not exists
    user_email = 'test@example.com'
    password_hash = hashlib.sha256('password123'.encode()).hexdigest()

    cursor.execute('SELECT * FROM users WHERE email = ?', (user_email,))
    if cursor.fetchone() is None:
        cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (user_email, password_hash))
        user_id = cursor.lastrowid

        # Seed 5 recipes for the user
        recipes = [
            ("Spaghetti Bolognese", "beef, pasta, tomato", "cook beef, boil pasta, mix", "classic favorite", "italian"),
            ("Grilled Cheese", "bread, cheese, butter", "butter bread, grill with cheese", "", "lunch,quick"),
            ("Pancakes", "flour, eggs, milk", "mix and fry", "add syrup", "breakfast,sweet"),
            ("Veggie Stir Fry", "broccoli, peppers, soy sauce", "stir-fry in pan", "serve with rice", "vegan,asian"),
            ("Chili", "beans, beef, spices", "slow cook everything", "good for cold days", "spicy,winter"),
        ]

        for title, ingredients, steps, notes, tags in recipes:
            cursor.execute('''
                INSERT INTO recipes (title, ingredients, steps, notes, tags, user_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (title, ingredients, steps, notes, tags, user_id))

        print("✅ Seeded 1 user and 5 recipes.")
    else:
        print("⚠️ Seed already exists, skipping.")

    connection.commit()
  

def db_make_connection():
    os.makedirs('db', exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    return connection

def db_close_connection(connection):
      connection.close()

def find_by_name_and_password(email, password):
    """Find a user by email and password. Password is hashed before comparison."""
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

def get_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE id = ?", (user_id))
    user = cursor.fetchone()

    conn.close()

    if user:
        return {
            "id": user[0]
        }
    else:
        return None