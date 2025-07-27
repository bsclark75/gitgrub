import sqlite3
from custom import DB_PATH

def get_all_recipes():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recipes")
    recipes = cursor.fetchall()
    conn.close()
    return recipes

def search_recipes(query):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    search = f"%{query.lower()}%"
    cursor.execute("""
        SELECT * FROM recipes 
        WHERE LOWER(title) LIKE ? OR LOWER(tags) LIKE ?
        """, (search, search))
    recipes = cursor.fetchall()
    conn.close()
    return recipes

def recipe_create(title, ingredients, steps, tags, user_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO recipes (title, ingredients, steps, tags, user_id) VALUES (?, ?, ?, ?, ?)", (title, ingredients, steps, tags, user_id))
        recipe_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return recipe_id

def get_recipe(id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM recipes WHERE id = ?", (id,))
    recipe = cursor.fetchone()
    conn.close()
    return recipe

def change_recipe(title, ingredients, steps, tags, recipe_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
            "UPDATE recipes SET title = ?, ingredients = ?, steps = ?, tags = ? WHERE id = ?",
            (title, ingredients, steps, tags, recipe_id)
        )
    conn.commit()
    conn.close()

def del_recipe(recipe_id, user):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if the recipe belongs to the user
    cursor.execute("SELECT user_id FROM recipes WHERE id = ?", (recipe_id,))
    row = cursor.fetchone()

    if row and str(row[0]) == str(user['id']):
        cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
        conn.commit()

    conn.close()


def get_forks(id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()    
    cursor.execute("SELECT * FROM recipes WHERE forked_from = ?", (id,))
    forks = cursor.fetchall()

    conn.close()
    return forks

def new_fork(recipe_id, user):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get the original recipe
    original = get_recipe(recipe_id)

    if not original:
        conn.close()
        return "Recipe not found", 404

    # Fork it for the current user
    cursor.execute("""
        INSERT INTO recipes (title, ingredients, steps, tags, user_id, forked_from)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        original['title'],
        original['ingredients'],
        original['steps'],
        original['tags'],
        user['id'],
        original['id']
    ))

    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id
