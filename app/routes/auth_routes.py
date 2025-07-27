from flask import Blueprint, request, redirect, url_for, render_template
from app.services.user_service import find_user_by_credentials, create_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = find_user_by_credentials(email, password)

        if not user:
            return render_template('login.html', message="Invalid username or password.")

        response = redirect(url_for("recipe.home"))
        response.set_cookie('YourSessionCookie', str(user["id"]))
        return response
    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return render_template('register.html', message="All fields are required.")

        create_user(email, password)

        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/logout')
def logout():
    response = redirect(url_for('auth.login'))
    response.delete_cookie('YourSessionCookie')
    return response
