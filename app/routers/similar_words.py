# app/routers/similar_words.py
from flask import Blueprint, current_app, jsonify
from app import mongo
# 定义蓝图
similar_words_bp = Blueprint('similar_words', __name__)

# 使用蓝图定义路由
@similar_words_bp.route('/similar-words')
def similar_words():
    # 从MongoDB获取所有相似单词组
    word_groups = mongo.db.similar_words.find({})
    # 将查询结果转换为列表
    word_groups_list = list(word_groups)
    # 转换ObjectId为字符串，以便能够进行JSON序列化
    for group in word_groups_list:
        group["_id"] = str(group["_id"])
    # 返回JSON响应
    return jsonify(word_groups_list)