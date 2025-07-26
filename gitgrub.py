from flask import Flask
import sqlite3
import os

app = Flask(__name__)

DB_PATH = 'db/gitgrub.db'

@app.route('/')
def home():
    return 'Hello, GitGrub!'

def init_db():
    # Ensure the db folder exists
    os.makedirs('db', exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Create a basic users table and recipes table
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

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
   