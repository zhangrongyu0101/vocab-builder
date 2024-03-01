# app/routers/similar_words.py
from flask import Blueprint, current_app

# 定义蓝图
similar_words_bp = Blueprint('similar_words', __name__)

# 使用蓝图定义路由
@similar_words_bp.route('/similar-words')
def similar_words():
    mongo = current_app.extensions['pymongo'].mongo
    # 你的处理逻辑
    return "Similar Words Page"
