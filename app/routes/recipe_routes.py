from flask import Blueprint, request, redirect, render_template, url_for
from app.services.recipe_service import (
    get_all_recipes,
    search_recipes,
    recipe_create,
    get_recipe,
    change_recipe,
    get_forks,
    del_recipe,
    new_fork
)
from app.services.user_service import get_user

recipe_bp = Blueprint("recipe", __name__)

@recipe_bp.route('/recipes/create', methods=['GET', 'POST'])
def create_recipe():
    if request.method == 'POST':
        title = request.form.get('title')
        ingredients = request.form.get('ingredients')
        steps = request.form.get('steps')
        tags = request.form.get('tags')
        user_id = request.cookies.get("YourSessionCookie")
        recipe_id = recipe_create(title, ingredients, steps, tags, user_id)
        return redirect(url_for('recipe.view_recipe', recipe_id=recipe_id))
    return render_template('new_recipe.html')

@recipe_bp.route('/recipes/<int:recipe_id>/edit', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    user_id = request.cookies.get("YourSessionCookie")
    user = get_user(user_id)
    recipe = get_recipe(recipe_id)

    if not recipe:
        return "Recipe not found", 404

    if str(recipe["user_id"]) != user_id:
        return "Unauthorized", 403

    if request.method == 'POST':
        title = request.form.get('title')
        ingredients = request.form.get('ingredients')
        steps = request.form.get('steps')
        tags = request.form.get('tags')

        change_recipe(title, ingredients, steps, tags, recipe_id)
        return redirect(url_for('recipe.view_recipe', recipe_id=recipe_id))

    return render_template('edit_recipe.html', recipe=recipe, user=user)

@recipe_bp.route('/recipes/<int:recipe_id>')
def view_recipe(recipe_id):
    user_id = request.cookies.get("YourSessionCookie")
    user = get_user(user_id)

    recipe = get_recipe(recipe_id)

    if not recipe:
        return "Recipe not found", 404

    forks = get_forks(recipe_id)

    return render_template('recipe_detail.html', recipe=recipe, user=user, forks=forks)

@recipe_bp.route('/recipes/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe(recipe_id):
    user_id = request.cookies.get("YourSessionCookie")
    user = get_user(user_id)

    if not user:
        return redirect(url_for('auth.login'))
    del_recipe(recipe_id, user)
    return redirect(url_for('recipe.home'))

@recipe_bp.route('/recipes/fork/<int:recipe_id>', methods=['POST'])
def fork_recipe(recipe_id):
    user_id = request.cookies.get("YourSessionCookie")
    user = get_user(user_id)
    if not user:
        return redirect(url_for('auth.login'))

    new_id = new_fork(recipe_id, user)

    return redirect(url_for('recipe.view_recipe', recipe_id=new_id))

@recipe_bp.route("/")
def home():
    user_id = request.cookies.get('YourSessionCookie')
    if not user_id:
        return redirect(url_for('auth.login'))

    user = get_user(user_id)
    if not user:
        return redirect(url_for('auth.login'))

    query = request.args.get('q', '').strip()

    if query:
        recipes = search_recipes(query)
    else:
        recipes = get_all_recipes()

    return render_template('recipe_list.html', user=user, recipes=recipes)
