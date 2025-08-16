# 📖 GitGrub

**GitGrub** is a lightweight Flask web app for sharing, searching, and forking recipes.  
Users can register, log in, add their own recipes, view others', and fork them to make personalized edits.

---

## 🚀 Features

- 🔐 User authentication (login & registration)
- 📚 Add, edit, and delete recipes
- 🍴 Fork recipes created by other users
- 🔍 Search recipes by title or tags
- 🖼️ Simple and clean UI with responsive layout
- 🧪 Test suite using `pytest`
- 🗄️ SQLite-based persistent storage

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/bsclark75/gitgrub.git
cd gitgrub
```

### 2. Create environment file

Copy the example `.env` file and edit as needed (at minimum, update `SECRET_KEY`):

```bash
cp env.example .env
```

- `SECRET_KEY` → generate with  
  ```bash
  python -c "import secrets; print(secrets.token_hex(16))"
  ```
- `ADMIN_EMAIL` → default admin user email
- `ADMIN_PASSWORD` → optional; if left blank, a strong random password is generated and printed when seeding the DB

### 3. Run setup script

This will:
- Create and activate a virtual environment
- Install dependencies
- Always reset the database (`db/gitgrub.sqlite3`)
- Seed the DB with one admin user and 5 sample recipes

```bash
chmod +x setup.sh
./setup.sh
```

### 4. Start the app

Activate the virtual environment, then launch Flask:

```bash
source venv/bin/activate
flask run
```

Now open your browser and visit:  
👉 [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🧪 Running Tests

```bash
pytest
```

---

## ⚠️ Notes

- `.env` and the SQLite database file (`db/gitgrub.sqlite3`) are **not committed** to GitHub.  
- Each run of `setup.sh` resets the database to a clean state.  
- If no `ADMIN_PASSWORD` is set in `.env`, one will be generated and shown in the console after seeding.  
