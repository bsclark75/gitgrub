from flask import Flask, request, redirect, url_for, render_template
from seed import *
import hashlib    

app = Flask(__name__)

@app.route("/")
def home():
    user_id = request.cookies.get('YourSessionCookie')
    if user_id:
        user = get_user(user_id)
        if user:
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM recipes")
            recipes = cursor.fetchall()
            conn.close()
            return render_template('recipe_list.html', user=user, recipes=recipes)
    return redirect(url_for('login'))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        email = request.form.get('email')
        password = request.form.get('password')

        user = find_by_name_and_password(email, password)

        if not user:
            raise ValueError("Invalid username or password supplied")

        response = redirect(url_for("home"))
        response.set_cookie('YourSessionCookie', str(user["id"]))
        return response
    else:
        response = render_template('login.html')
        return response 

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return render_template('register.html', message="All fields are required.")

        password_hash = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            conn.close()
            return render_template('register.html', message="User already exists.")

        # Insert new user
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password_hash))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))  # Assuming you have a login route

    return render_template('register.html')
 
@app.route('/recipes/create', methods=['GET', 'POST'])
def create_recipe():
    if request.method == 'POST':
        title = request.form.get('title')
        ingredients = request.form.get('ingredients')
        steps = request.form.get('steps')
        tags = request.form.get('tags')
        user_id = request.cookies.get("YourSessionCookie")

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO recipes (title, ingredients, steps, tags, user_id) VALUES (?, ?, ?, ?, ?)", (title, ingredients, steps, tags, user_id))
        recipe_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return redirect(url_for('view_recipe', recipe_id=recipe_id))
    return render_template('new_recipe.html')

@app.route('/recipes/<int:recipe_id>/edit', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    user_id = request.cookies.get("YourSessionCookie")
    user = get_user(user_id)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
    recipe = cursor.fetchone()

    if not recipe:
        conn.close()
        return "Recipe not found", 404

    if str(recipe["user_id"]) != user_id:
        conn.close()
        return "Unauthorized", 403

    if request.method == 'POST':
        title = request.form.get('title')
        ingredients = request.form.get('ingredients')
        steps = request.form.get('steps')
        tags = request.form.get('tags')

        cursor.execute(
            "UPDATE recipes SET title = ?, ingredients = ?, steps = ?, tags = ? WHERE id = ?",
            (title, ingredients, steps, tags, recipe_id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('view_recipe', recipe_id=recipe_id))

    conn.close()
    return render_template('edit_recipe.html', recipe=recipe, user=user)

@app.route('/recipes/<int:recipe_id>')
def view_recipe(recipe_id):
    user_id = request.cookies.get("YourSessionCookie")
    user = get_user(user_id)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get the main recipe
    cursor.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
    recipe = cursor.fetchone()

    if not recipe:
        conn.close()
        return "Recipe not found", 404

    # Get first-generation forks
    cursor.execute("SELECT * FROM recipes WHERE forked_from = ?", (recipe_id,))
    forks = cursor.fetchall()

    conn.close()

    return render_template('recipe_detail.html', recipe=recipe, user=user, forks=forks)

@app.route('/recipes/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe(recipe_id):
    user_id = request.cookies.get("YourSessionCookie")
    user = get_user(user_id)

    if not user:
        return redirect(url_for('login'))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if the recipe belongs to the user
    cursor.execute("SELECT user_id FROM recipes WHERE id = ?", (recipe_id,))
    row = cursor.fetchone()

    if row and str(row[0]) == str(user['id']):
        cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
        conn.commit()

    conn.close()
    return redirect(url_for('home'))

@app.route('/recipes/fork/<int:recipe_id>', methods=['POST'])
def fork_recipe(recipe_id):
    user_id = request.cookies.get("YourSessionCookie")
    user = get_user(user_id)
    if not user:
        return redirect(url_for('login'))

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get the original recipe
    cursor.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
    original = cursor.fetchone()
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

    return redirect(url_for('view_recipe', recipe_id=new_id))

@app.route('/logout')
def logout():
    response = redirect(url_for('login'))
    response.delete_cookie('YourSessionCookie')
    return response

if __name__ == '__main__':
    db = db_make_connection()
    init_db(db)
    app.run(debug=True)
   