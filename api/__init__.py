from flask import Flask
from config import SQLALCHEMY_DATABASE_URI
from models import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from routes import api_blueprint
    app.register_blueprint(api_blueprint)

    return app
