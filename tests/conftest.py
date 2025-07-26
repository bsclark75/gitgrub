import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import sqlite3
from gitgrub import app as flask_app
from seed import init_db, DB_PATH

@pytest.fixture
def client(tmp_path):
    # Setup test database file
    test_db = tmp_path / "test.db"
    os.environ['DB_PATH'] = str(test_db)

    # Create app configured for testing
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False

    # Initialize fresh database
    conn = sqlite3.connect(str(test_db))
    init_db()
    conn.close()

    with flask_app.test_client() as client:
        yield client
