# 听写相关功能
from flask import Blueprint, jsonify, request, render_template, current_app
from flask_login import login_required, current_user
from app import mongo
from datetime import datetime
from bson.objectid import ObjectId
import random

dictation_bp = Blueprint('dictation_bp', __name__)


@dictation_bp.route('/dictation')
def dictation():
    # 获取可选的标签参数
    selected_tag = request.args.get('tag')
    # 构建查询条件
    query = {}
    if selected_tag:
        query['tags'] = selected_tag

    # 查找听写次数最少的单词
    min_dictation_count = mongo.db.words.find(query).sort('dictation_count', 1).limit(1)[0]['dictation_count']
    words_with_min_count = list(mongo.db.words.find({'dictation_count': min_dictation_count, **query}))

    if words_with_min_count:
        # 选择列表中的第一个单词
        dictation_prompt = words_with_min_count[0]
    else:
        dictation_prompt = None

    return render_template('dictation.html', dictation_prompt=dictation_prompt)


@dictation_bp.route('/check-word', methods=['POST'])
def check_word():
    data = request.get_json()  
    input_word = data.get('inputWord')
    correct_word = data.get('correctWord')
    if current_user.is_authenticated:
        user_id = ObjectId(current_user.get_id())  # 确保从字符串转换为ObjectId
        if input_word.lower() == correct_word.lower():
            # 用户答对了，加3分
            mongo.db.users.update_one({'_id': user_id}, {'$inc': {'points': 3}})
            return jsonify({'message': 'Correct!'})
        else:
            # 用户答错了，减1分
            mongo.db.users.update_one({'_id': user_id}, {'$inc': {'points': -1}})
            return jsonify({'message': 'Incorrect, try again.'})
    else:
        if input_word.lower() == correct_word.lower():
            return jsonify({'message': 'Correct!'})
        else:
            return jsonify({'message': 'Incorrect, try again.'})
        

@dictation_bp.route('/save_records', methods=['POST'])
def save_records():
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    if not current_user.is_authenticated:
        return jsonify({"error": "User not authenticated"}), 401

    try:
        user_id = ObjectId(current_user.get_id())
        mode = data.get('mode')
        total_words = data.get('total_words')
        error_words = data.get('error_words')

        if mode is None or total_words is None or error_words is None:
            return jsonify({"error": "Incomplete data"}), 400

        dictation_record = {
            "mode": mode,
            "total_words": total_words,
            "error_words": error_words,
            "timestamp": datetime.utcnow()
        }

        result = mongo.db.users.update_one(
            {"_id": user_id},
            {"$push": {"dictation_history": dictation_record}}
        )

        if result.modified_count == 0:
            return jsonify({"error": "Failed to update user record"}), 500

        return jsonify({"message": "Statistics saved successfully"}), 201

    except Exception as e:
        # Add logging here
        return jsonify({"error": str(e)}), 500



@dictation_bp.route('/new-word', methods=['GET'])
def new_word():
    # 获取可选的标签参数
    selected_tag = request.args.get('tag')
    sort_method = request.args.get('sort', 'least_dictated')
    # 构建查询条件
    query = {}
    if selected_tag:
        query['tags'] = selected_tag

    # 查找听写次数最少的单词
    
    if sort_method == 'least_dictated':
        words_with_min_count = list(mongo.db.words.find(query).sort('dictation_count', 1))

        if words_with_min_count:
            min_dictation_count = words_with_min_count[0]['dictation_count']
            filtered_words = [word for word in words_with_min_count if word['dictation_count'] == min_dictation_count]

            dictation_prompt = random.choice(filtered_words)
            return jsonify({
                '_id': str(dictation_prompt['_id']),  # 确保ID被转换为字符串
                'word': dictation_prompt['word'],
                'translation': dictation_prompt['translation'],
                'usage': dictation_prompt.get('usage', 'No usage available.'),
            })
        else:
            return jsonify({'error': 'No words available'}), 404
        
    elif sort_method == 'most_errors':
        words_with_max_errors = list(mongo.db.words.find(query).sort('errors_count', -1))

        if words_with_max_errors:
            max_error_count = words_with_max_errors[0]['errors_count']
            filtered_words = [word for word in words_with_max_errors if word['errors_count'] == max_error_count]

            dictation_prompt = random.choice(filtered_words)
            return jsonify({
                '_id': str(dictation_prompt['_id']),
                'word': dictation_prompt['word'],
                'translation': dictation_prompt['translation'],
                'usage': dictation_prompt.get('usage', 'No usage available.'),
            })
        else:
            return jsonify({'error': 'No words available'}), 404
        
    else:
        
        return jsonify({'error': 'Invalid sort method'}), 400
    

    
@dictation_bp.route('/increment-dictation-count/<word_id>', methods=['POST'])
def increment_dictation_count(word_id):
    mongo.db.words.update_one(
        {'_id': ObjectId(word_id)},
        {'$inc': {'dictation_count': 1}}
    )
    return jsonify({'message': 'Dictation count incremented successfully'})

@dictation_bp.route('/increment-errors-count/<word_id>', methods=['POST'])
def increment_errors_count(word_id):
    mongo.db.words.update_one(
        {'_id': ObjectId(word_id)},
        {'$inc': {'errors_count': 1}}
    )
    return jsonify({'message': 'Errors count incremented successfully'})


@dictation_bp.route('/get-count/<word_id>', methods=['GET'])
def get_count(word_id):
    word_doc = mongo.db.words.find_one({'_id': ObjectId(word_id)})
    if word_doc:
        dictation_count = word_doc.get('dictation_count', 0)
        error_count = word_doc.get('errors_count', 0)
        return jsonify({
            'dictation_count': dictation_count,
            'error_count': error_count
        })
    else:
        return jsonify({'error': 'Word not found'}), 404

    
@dictation_bp.route('/get-points', methods=['GET'])
@login_required
def get_points():
    user_id = current_user.get_id()
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        return jsonify({'points': user.get('points', 0)})  
    else:
        return jsonify({'error': 'User not found'}), 404