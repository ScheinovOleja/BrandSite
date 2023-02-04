from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://oleg:oleg2000@localhost/parser_brands'
    db.init_app(app)

    from server.routes import app as server_app
    app.register_blueprint(server_app)

    with app.app_context():
        db.create_all()

    return app
