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


app = create_app()


@app.template_filter()
def replace_n(value):
    return value.replace('\n', '<br />')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
