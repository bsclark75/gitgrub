# seed.py
import os
import sqlite3
import hashlib
import secrets
from pathlib import Path
from custom import DB_PATH

def init_db():
    # Ensure db folder exists
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Always drop old tables (since setup.sh wipes db file, this is just safety)
    cursor.execute('DROP TABLE IF EXISTS recipes')
    cursor.execute('DROP TABLE IF EXISTS users')

    # Recreate schema
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE recipes (
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

    seed_db()  # always seed

def seed_db():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Get admin credentials from env (fallbacks safe for open source)
    user_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_password:
        admin_password = secrets.token_urlsafe(12)  # generate safe random pass
        print("\n⚠️ No ADMIN_PASSWORD set in .env, generated one-time password:")
        print(f"   Email:    {user_email}")
        print(f"   Password: {admin_password}\n")

    password_hash = hashlib.sha256(admin_password.encode()).hexdigest()

    # Insert admin user
    cursor.execute(
        'INSERT INTO users (email, password) VALUES (?, ?)',
        (user_email, password_hash)
    )
    user_id = cursor.lastrowid

    # Insert sample recipes
    recipes = [
        ("Spaghetti Bolognese", "beef, pasta, tomato", "cook beef, boil pasta, mix", "classic favorite", "italian"),
        ("Grilled Cheese", "bread, cheese, butter", "butter bread, grill with cheese", "", "lunch,quick"),
        ("Pancakes", "flour, eggs, milk", "mix and fry", "add syrup", "breakfast,sweet"),
        ("Veggie Stir Fry", "broccoli, peppers, soy sauce", "stir-fry in pan", "serve with rice", "vegan,asian"),
        ("Chili", "beans, beef, spices", "slow cook everything", "good for cold days", "spicy,winter"),
    ]

    cursor.executemany('''
        INSERT INTO recipes (title, ingredients, steps, notes, tags, user_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', [(t, i, s, n, tags, user_id) for (t, i, s, n, tags) in recipes])

    connection.commit()
    connection.close()

    print("✅ Seeded 1 admin user and 5 recipes.")

if __name__ == "__main__":
    init_db()
