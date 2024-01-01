from flask import Flask

def create_app():
    app = Flask(__name__)

    from .routes.user_routes import user_blueprint
    from .routes.category_routes import category_blueprint
    from .routes.record_routes import record_blueprint

    app.register_blueprint(user_blueprint)
    app.register_blueprint(category_blueprint)
    app.register_blueprint(record_blueprint)

    return app
