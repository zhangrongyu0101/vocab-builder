# 主要单词增删改查功能
from flask import Blueprint, request, redirect, url_for, flash
from flask_pymongo import ObjectId
from flask import current_app, render_template
from app import mongo

words_bp = Blueprint('words_bp', __name__)

@words_bp.route('/')
def index():
    # 使用 _id 字段逆序排序单词
    words_list = list(mongo.db.words.find().sort('_id', -1))
    return render_template('index.html', words=words_list)

@words_bp.route('/add', methods=['POST'])
def add_word():
    word = request.form.get('word')
    translation = request.form.get('translation')
    usage = request.form.get('usage')

    if word:  # 只检查是否提供了单词
        # 即使没有提供翻译和用法，也插入单词
        mongo.db.words.insert_one({
            'word': word, 
            'translation': translation, 
            'usage': usage, 
            'dictation_count': 0
        })
        flash('Word added successfully!')
    else:
        flash('Word cannot be empty!')  # 修改了错误消息以反映新的验证逻辑

    return redirect(url_for('main.index'))



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
    return redirect(url_for('main.index'))

@words_bp.route('/delete/<word_id>')
def delete_word(word_id):
    mongo = current_app.extensions['pymongo'].mongo
    mongo.db.words.delete_one({'_id': ObjectId(word_id)})
    flash('Word deleted successfully!')
    return redirect(url_for('main.index'))


@words_bp.route('/increment-dictation-count/<word_id>', methods=['POST'])
def increment_dictation_count(word_id):
    mongo.db.words.update_one(
        {'_id': ObjectId(word_id)},
        {'$inc': {'dictation_count': 1}}
    )
    return jsonify({'message': 'Dictation count incremented successfully'})

