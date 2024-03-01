from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS

from config import config

# 在这里创建并初始化mongo实例
mongo = PyMongo()
    
def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    
    
    # 初始化PyMongo与当前应用
    mongo.init_app(app)
    
    # 导入蓝图，avoid circular import at the same time. 
    from .routers.words import words_bp
    from .routers.dictation import dictation_bp
    from .routers.google_api import google_api_bp
    from .routers.import_words import import_words_bp
    from .routers.similar_words import similar_words_bp
    # 注册蓝图
    app.register_blueprint(words_bp)
    app.register_blueprint(dictation_bp)
    app.register_blueprint(google_api_bp)
    app.register_blueprint(import_words_bp, url_prefix='/import')
    app.register_blueprint(similar_words_bp)

    CORS(app)  # 使CORS应用于整个Flask应用

    return app
