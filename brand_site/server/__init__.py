import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder=f"{os.getcwd()}/templates", static_folder=f"{os.getcwd()}/static")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://oleg:oleg2000@localhost/parser_brands'
    db.init_app(app)

    from .routes import app as server_app
    app.register_blueprint(server_app)

    with app.app_context():
        db.create_all()

    return app
