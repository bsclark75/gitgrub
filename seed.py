# seed.py

import os
import sqlite3
import hashlib
from custom import DB_PATH

def init_db():
    is_testing = os.getenv('FLASK_ENV') == 'testing' or os.getenv('TESTING') == '1'

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    if is_testing:
        cursor.execute('DROP TABLE IF EXISTS recipes')
        cursor.execute('DROP TABLE IF EXISTS users')

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

    connection.commit()
    connection.close()

    if is_testing or os.getenv('SEED') == '1':
        seed_db()

def seed_db():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    user_email = 'test@example.com'
    password_hash = hashlib.sha256('password123'.encode()).hexdigest()

    cursor.execute('SELECT id FROM users WHERE email = ?', (user_email,))
    user = cursor.fetchone()

    if not user:
        cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (user_email, password_hash))
        user_id = cursor.lastrowid
    else:
        user_id = user[0]

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

    connection.commit()
    connection.close()

    print("✅ Seeded 1 user and 5 recipes.")
