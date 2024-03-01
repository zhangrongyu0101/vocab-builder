from flask import Blueprint, request, jsonify, current_app
import csv
from io import StringIO
from app import mongo

import_words_bp = Blueprint('import_words_bp', __name__)

@import_words_bp.route('/import-words', methods=['POST'])
def import_words():
    file = request.files['file']
    if not file:
        return jsonify({'error': 'No file provided'}), 400

    stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)
    for row in csv_input:
        # 使用解包赋值同时提供默认值以处理行元素数量不足的情况
        word, translation, usage = (row + [None, None, None])[:3]
        # 将单词、翻译和用法保存到数据库
        mongo.db.words.insert_one({'word': word or "未知", 
                                'translation': translation or "未知", 
                                'usage': usage or "无",
                                'dictation_count': 0  # 初始化听写次数为0
                                })

    return jsonify({'message': 'Upload successful'})