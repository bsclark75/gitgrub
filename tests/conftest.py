import os
import sys
import pytest
import sqlite3

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from seed import init_db

@pytest.fixture
def client(tmp_path):
    test_db = tmp_path / "test.db"
    os.environ['DB_PATH'] = str(test_db)

    app = create_app()  # ✅ FIX: CALL the factory
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    os.environ['FLASK_ENV'] = 'testing'
    os.environ['TESTING'] = '1'

    init_db()  # initialize schema & seed

    with app.test_client() as client:
        yield client
