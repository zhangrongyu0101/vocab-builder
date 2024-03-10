from flask import Blueprint, request, redirect, url_for, flash, jsonify, render_template
from flask_pymongo import ObjectId
from app import mongo
import re

sentences_bp = Blueprint('sentences_bp', __name__)

@sentences_bp.route('/sentences')
def sentences():
    # 使用 _id 字段逆序排序句子
    sentences_list = list(mongo.db.sentences.find().sort('_id', -1))
    return render_template('sentences.html', sentences=sentences_list)

@sentences_bp.route('/sentences/add', methods=['POST'])
def add_sentence():
    sentence = request.form.get('sentence').strip() if request.form.get('sentence') else None
    translation = request.form.get('translation')
    keywords_str = request.form.get('keywords')  # 获取关键词字符串
    usage = request.form.get('usage')  # 获取用法字符串
    
    if not sentence:
        flash('Sentence cannot be empty!')
        return redirect(url_for('sentences_bp.sentences'))
    
    # 使用正则表达式分割字符串，允许使用逗号、分号等作为分隔符
    keywords = [keyword.strip() for keyword in re.split('[,，;；]', keywords_str) if keyword.strip()]

    # 检查数据库中是否已存在该句子
    existing_sentence = mongo.db.sentences.find_one({'sentence': sentence})
    if existing_sentence:
        flash(f'The sentence "{sentence}" already exists.')
    else:
        # 如果句子不存在，插入新句子
        mongo.db.sentences.insert_one({
            'sentence': sentence,
            'translation': translation,
            'keywords': keywords,
            'usage': usage  # 存储用法
        })
        flash('Sentence added successfully!')

    return redirect(url_for('sentences_bp.sentences'))

@sentences_bp.route('/sentences/edit/<sentence_id>')
def edit_sentence(sentence_id):
    sentence = mongo.db.sentences.find_one({'_id': ObjectId(sentence_id)})
    return render_template('edit_sentence.html', sentence=sentence)

@sentences_bp.route('/sentences/update/<sentence_id>', methods=['POST'])
def update_sentence(sentence_id):
    # 获取表单数据
    sentence = request.form.get('sentence')
    translation = request.form.get('translation')
    keywords = request.form.getlist('keywords')  # 从表单获取关键词数组
    usage = request.form.get('usage')  # Don't forget to fetch the 'usage' from the form!

    mongo.db.sentences.update_one(
        {'_id': ObjectId(sentence_id)},
        {'$set': {
            'sentence': sentence,
            'translation': translation,
            'keywords': keywords,
            'usage': usage  # Now 'usage' is correctly fetched and updated
        }}
    )
    flash('Sentence updated successfully!')
    return redirect(url_for('sentences_bp.sentences'))

@sentences_bp.route('/sentences/delete/<sentence_id>')
def delete_sentence(sentence_id):
    mongo.db.sentences.delete_one({'_id': ObjectId(sentence_id)})
    flash('Sentence deleted successfully!')
    return redirect(url_for('sentences_bp.sentences'))

@sentences_bp.route('/sentences/get-sentence-info', methods=['GET'])
def get_sentence_info():
    sentence = request.args.get('sentence')  # 从查询参数中获取句子

    if not sentence:
        return jsonify({'error': 'Sentence parameter is required.'}), 400

    sentence_info = mongo.db.sentences.find_one({'sentence': sentence})

    if not sentence_info:
        return jsonify({'error': 'Sentence not found.'}), 404

    sentence_info.pop('_id', None)  # 移除 MongoDB 的 _id 字段

    return jsonify(sentence_info)
