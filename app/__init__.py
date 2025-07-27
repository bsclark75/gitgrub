from flask import Flask

def create_app():
    app = Flask(__name__)

    from .routes.auth_routes import auth_bp
    from .routes.recipe_routes import recipe_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(recipe_bp)

    return app
