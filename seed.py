import os
import hashlib
import sqlite3
from custom import DB_PATH

def init_db():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Check if we're in test mode (based on environment variable)
    is_testing = os.getenv('FLASK_ENV') == 'testing' or os.getenv('TESTING') == '1'

    if is_testing:
        # Drop tables to ensure fresh state
        cursor.execute('DROP TABLE IF EXISTS recipes')
        cursor.execute('DROP TABLE IF EXISTS users')
    else:
        # In prod, don't drop tables — just create if not exist
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

    # If in testing or if users table just created, seed data
    if is_testing or not table_has_user(cursor, 'test@example.com'):
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

        # Seed user and recipes
        user_email = 'test@example.com'
        password_hash = hashlib.sha256('password123'.encode()).hexdigest()

        cursor.execute('INSERT OR IGNORE INTO users (email, password) VALUES (?, ?)', (user_email, password_hash))
        user_id = cursor.lastrowid or cursor.execute('SELECT id FROM users WHERE email=?', (user_email,)).fetchone()[0]

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

    connection.commit()

def table_has_user(cursor, email):
    cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
    return cursor.fetchone() is not None
 
