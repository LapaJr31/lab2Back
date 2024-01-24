from flask import Flask
from flask_migrate import Migrate
from .extensions import db
from .routes import main_routes
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(main_routes)
    db.init_app(app)
    migrate = Migrate(app, db)


    with app.app_context():
        db.create_all()


    return app