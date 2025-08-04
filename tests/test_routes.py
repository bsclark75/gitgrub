import os
import sys
import pytest
import hashlib
from flask import session

# Setup environment
os.environ["DB_PATH"] = "db/test_gitgrub.db"
os.environ["FLASK_ENV"] = "testing"
os.environ["TESTING"] = "1"

# Path to import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from seed import init_db, DB_PATH

# ------------------- Fixtures -------------------

@pytest.fixture(scope="function")
def client():
    # Fresh DB before each test
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    init_db()

    app = create_app()
    app.config["TESTING"] = True
    app.secret_key = "test"  # Needed for session handling

    with app.test_client() as client:
        yield client

@pytest.fixture(scope="function")
def logged_in_client(client):
    with client.session_transaction() as sess:
        sess["user_id"] = 1
        sess["user_email"] = "test@example.com"
    return client

# ------------------- Helper -------------------

def login_helper(client, email="test@example.com", password="password123"):
    rv = client.post("/login", data={"email": email, "password": password}, follow_redirects=True)
    assert rv.status_code == 200
    return rv

# ------------------- Tests -------------------

def test_home_redirects_to_login(client):
    rv = client.get("/")
    assert b"Log In" in rv.data or rv.status_code in (301, 302)

def test_login_and_list_recipes(client):
    login_helper(client)
    rv = client.get("/")
    assert b"All Recipes" in rv.data
    assert b"Spaghetti Bolognese" in rv.data

def test_create_recipe_and_redirect(client):
    login_helper(client)
    rv = client.post("/recipes/create", data={
        "title": "Test Recipe",
        "ingredients": "a, b, c",
        "steps": "do it",
        "tags": "test"
    }, follow_redirects=False)
    assert rv.status_code == 302
    location = rv.headers["Location"]
    assert "/recipes/" in location

    rv2 = client.get(location)
    assert b"Test Recipe" in rv2.data
    assert b"Ingredients" in rv2.data

def test_fork_recipe(client):
    login_helper(client)
    rv = client.post("/recipes/fork/1", follow_redirects=True)
    assert b"Forked from" in rv.data

def test_search_by_title_and_tag(client):
    client.post('/register', data={
        'email': 'searcher@example.com',
        'password': 'pass123'
    })
    client.post('/login', data={
        'email': 'searcher@example.com',
        'password': 'pass123'
    })

    client.post('/recipes/create', data={
        'title': 'Spicy Tofu',
        'ingredients': 'Tofu, Chili, Garlic',
        'steps': 'Cook it all together.',
        'tags': 'vegan,spicy'
    })

    client.post('/recipes/create', data={
        'title': 'Sweet Pancakes',
        'ingredients': 'Flour, Sugar, Eggs',
        'steps': 'Mix and fry.',
        'tags': 'breakfast,sweet'
    })

    response = client.get('/', query_string={'q': 'pancakes'})
    assert b'Sweet Pancakes' in response.data
    assert b'Spicy Tofu' not in response.data

    response = client.get('/', query_string={'q': 'vegan'})
    assert b'Spicy Tofu' in response.data
    assert b'Sweet Pancakes' not in response.data

    response = client.get('/', query_string={'q': 'pizza'})
    assert b'Spicy Tofu' not in response.data
    assert b'Sweet Pancakes' not in response.data

def test_create_recipe_as_logged_in_user(logged_in_client):
    response = logged_in_client.post("/recipes/create", data={
        "title": "Test Recipe",
        "ingredients": "Eggs, Bacon",
        "steps": "Cook it up",
        "tags": "breakfast"
    }, follow_redirects=True)

    assert b"Test Recipe" in response.data
