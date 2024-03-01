# 听写相关功能
from flask import Blueprint, jsonify, current_app,render_template
import random
from app import mongo

dictation_bp = Blueprint('dictation_bp', __name__)

@dictation_bp.route('/dictation')
def dictation():
    # 查找听写次数最少的单词
    min_dictation_count = mongo.db.words.find().sort('dictation_count', 1).limit(1)[0]['dictation_count']
    words_with_min_count = list(mongo.db.words.find({'dictation_count': min_dictation_count}))

    if words_with_min_count:
        # 由于这里不需要随机选择，我们可以直接选择列表中的第一个单词
        dictation_prompt = words_with_min_count[0]
    else:
        dictation_prompt = None

    return render_template('dictation.html', dictation_prompt=dictation_prompt)

@dictation_bp.route('/check-word', methods=['POST'])
def check_word():
    data = request.get_json()  # 使用 get_json 方法
    input_word = data.get('inputWord')
    correct_word = data.get('correctWord')
    
    # 这里添加你的逻辑来检查单词是否正确
    if input_word.lower() == correct_word.lower():
        return jsonify({'message': 'Correct!'})
    else:
        return jsonify({'message': 'Incorrect, try again.'})


@dictation_bp.route('/new-word', methods=['GET'])
def new_word():
    # 查找听写次数最少的单词
    min_dictation_count = mongo.db.words.find().sort('dictation_count', 1).limit(1)[0]['dictation_count']
    words_with_min_count = list(mongo.db.words.find({'dictation_count': min_dictation_count}))

    if words_with_min_count:
        dictation_prompt = random.choice(words_with_min_count)
        return jsonify({
            '_id': str(dictation_prompt['_id']),  # 确保ID被转换为字符串
            'word': dictation_prompt['word'],
            'translation': dictation_prompt['translation'],
            'usage': dictation_prompt.get('usage', 'No usage available.')
        })
    else:
        return jsonify({'error': 'No words available'}), 404