from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS

mongo = None

def create_app():
    global mongo
    app = Flask(__name__)
    CORS(app)  # 使CORS应用于整个Flask应用
    
    app.config.from_pyfile('../config.py')

    mongo = PyMongo(app)

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
