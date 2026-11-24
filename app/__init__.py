
from flask import Flask
from config import Config
from app.database import init_db


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        init_db()

    return app
