from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_login import LoginManager
from bson.objectid import ObjectId 
from .models.user import User
from config import config

# 在这里创建并初始化 PyMongo 实例
mongo = PyMongo()

# 初始化 Flask-Login
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    
    # 初始化 PyMongo 与当前应用
    mongo.init_app(app)

    # 初始化 Flask-Login 与当前应用
    login_manager.init_app(app)

    # 导入蓝图，避免循环导入
    from .routers.auth import auth_bp
    from .routers.words import words_bp
    from .routers.dictation import dictation_bp
    from .routers.google_api import google_api_bp
    from .routers.import_words import import_words_bp
    from .routers.similar_words import similar_words_bp
    from .routers.sentences import sentences_bp
    
    # 注册蓝图
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(words_bp)
    app.register_blueprint(dictation_bp)
    app.register_blueprint(google_api_bp)
    app.register_blueprint(import_words_bp, url_prefix='/import')
    app.register_blueprint(similar_words_bp)
    app.register_blueprint(sentences_bp)
    
    # 设置 Flask-Login 的登录视图
    login_manager.login_view = "auth_bp.login"
    
    CORS(app)  # 应用 CORS 到整个 Flask 应用

    # Flask-Login 用户加载器
    @login_manager.user_loader
    def load_user(user_id):
        user = mongo.db.users.find_one({"_id": ObjectId('65ed4977413a6e6063965b8e')})
        if user:
            return User(username=user['username'], email=user['email'], password=user['password'])
        return None

    return app