import hashlib
from seed import DB_PATH

def login_helper(client, email="test@example.com", password="password123"):
    # Use plain form data to log in
    rv = client.post("/login", data={"email": email, "password": password}, follow_redirects=True)
    assert rv.status_code == 200
    return rv

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
    # Post new recipe
    rv = client.post("/recipes/create", data={
        "title": "Test Recipe",
        "ingredients": "a, b, c",
        "steps": "do it",
        "tags": "test"
    }, follow_redirects=False)
    assert rv.status_code == 302
    # Should redirect to detail view
    location = rv.headers["Location"]
    assert "/recipes/" in location

    # Fetch that new detail page
    rv2 = client.get(location)
    assert b"Test Recipe" in rv2.data
    assert b"Ingredients" in rv2.data

def test_fork_recipe(client):
    login_helper(client)
    # Fork first recipe
    rv = client.post("/recipes/fork/1", follow_redirects=True)
    assert b"Forked from" in rv.data
