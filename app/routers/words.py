# 主要单词增删改查功能
from flask import Blueprint, request, redirect, url_for, flash
from flask_pymongo import ObjectId
from flask import current_app, render_template
from app import mongo
from flask import render_template
from flask_login import login_required, current_user
from bson.objectid import ObjectId

words_bp = Blueprint('words_bp', __name__)

@words_bp.route('/')
def index():
    # 使用 _id 字段逆序排序单词
    words_list = list(mongo.db.words.find().sort('_id', -1))
    user_score = 0  # 默认分数
    if current_user.is_authenticated:
        user_id = current_user.get_id()
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if user:
            user_score = user.get('points', 0)  # 获取分数，如果未找到则默认为0

    return render_template('index.html', words=words_list, user_score=user_score)

@words_bp.route('/add', methods=['POST'])
def add_word():
    # 获取表单数据并去除word的前后空格
    word = request.form.get('word').strip() if request.form.get('word') else None
    translation = request.form.get('translation')
    usage = request.form.get('usage')

    if word:
        # 检查数据库中是否已存在该单词
        existing_word = mongo.db.words.find_one({'word': word})
        if existing_word:
            # 如果单词已存在，给用户反馈
            flash(f'The word "{word}" already exists.')
        else:
            # 如果单词不存在，插入新单词
            mongo.db.words.insert_one({
                'word': word,
                'translation': translation,
                'usage': usage,
                'dictation_count': 0
            })
            flash('Word added successfully!')
    else:
        flash('Word cannot be empty!')

    return redirect(url_for('words_bp.index'))


@words_bp.route('/edit/<word_id>')
def edit_word(word_id):
    word = mongo.db.words.find_one({'_id': ObjectId(word_id)})
    return render_template('edit_word.html', word=word)

@words_bp.route('/update/<word_id>', methods=['POST'])
def update_word(word_id):
    mongo.db.words.update_one(
        {'_id': ObjectId(word_id)},
        {'$set': {
            'word': request.form.get('word'),
            'translation': request.form.get('translation'),
            'usage': request.form.get('usage')
        }}
    )
    flash('Word updated successfully!')
    return redirect(url_for('words_bp.index'))

@words_bp.route('/delete/<word_id>')
def delete_word(word_id):
    mongo.db.words.delete_one({'_id': ObjectId(word_id)})
    flash('Word deleted successfully!')
    return redirect(url_for('words_bp.index'))



@words_bp.route('/get-word-info', methods=['GET'])
def get_word_info():
    word = request.args.get('word')  # 从查询参数中获取单词

    if not word:
        return jsonify({'error': 'Word parameter is required.'}), 400

    word_info = mongo.db.words.find_one({'word': word})

    if not word_info:
        return jsonify({'error': 'Word not found.'}), 404

    # 从数据库记录中移除 MongoDB 的 _id 字段
    word_info.pop('_id', None)

    return jsonify(word_info)

