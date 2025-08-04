import os
os.environ["DB_PATH"] = "db/test_gitgrub.db"
os.environ["FLASK_ENV"] = "testing"
os.environ["TESTING"] = "1"
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_app
from seed import init_db, DB_PATH

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    init_db()  # This will create & seed db/test_gitgrub.db

@pytest.fixture(scope="function")
def client():
    # Ensure fresh DB
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    init_db()

    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client
