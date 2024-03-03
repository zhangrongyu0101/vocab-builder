# app/routers/similar_words.py
from flask import Blueprint, current_app, jsonify ,request,render_template,flash
from flask import request, jsonify, redirect, url_for
from bson import ObjectId
from app import mongo
from flask import jsonify
from bson.objectid import ObjectId
from pymongo import MongoClient
from flask import Blueprint
import re
# 定义蓝图
similar_words_bp = Blueprint('similar_words', __name__)

# # 使用蓝图定义路由

@similar_words_bp.route('/similar-words')
def similar_words():
    word_groups = mongo.db.similar_words.find({}).sort('_id', -1)
    word_groups_list = []

    # 收集所有单词以进行批量查询
    all_words = set(word for group in word_groups for word in group['words'])
    words_info = mongo.db.words.find({'word': {'$in': list(all_words)}})
    words_info_dict = {info['word']: info for info in words_info}

    # 重置游标
    word_groups.rewind()

    for group in word_groups:
        group_detail = {
            'words': [],
            'similarityType': group['similarityType'],
            '_id': str(group['_id'])
        }
        
        for word in group['words']:
            word_info = words_info_dict.get(word)
            if word_info:
                group_detail['words'].append({
                    'word': word,
                    'translation': word_info.get('translation', 'No translation found'),
                    'usage': word_info.get('usage', 'No usage found'),
                    '_id': str(word_info.get('_id', 'No _id found'))
                })
            else:
                # 没有找到单词信息的情况
                group_detail['words'].append({
                    'word': word,
                    'translation': 'No translation found',
                    'usage': 'No usage found'
                })
        
        word_groups_list.append(group_detail)

    return render_template('similar_words.html', word_groups=word_groups_list)




@similar_words_bp.route('/add/similar-words', methods=['POST'])
def add_similar_words():
    # 从表单中获取数据
    words_str = request.form.get('words')
    similarityType = request.form.get('similarityType')
    
    if not words_str or not similarityType:
        # 你可能想要重定向用户到一个错误页面或显示一个错误消息
        return jsonify({'error': 'Missing data'}), 400
    
    words = [word.strip() for word in re.split('[,，;；]', words_str) if word.strip()]
    data = {'words': words, 'similarityType': similarityType}
    
    try:
        # 将新的相似单词组插入到数据库
        mongo.db.similar_words.insert_one(data)
        # 这里重定向到相似单词组列表页面，或者其他你认为合适的地方
        return redirect(url_for('similar_words.similar_words'))
    except Exception as e:
        return jsonify({'error': 'Failed to add similar words', 'exception': str(e)}), 500


@similar_words_bp.route('/edit/similar-words/<group_id>')
def edit_similar_words(group_id):
    group = mongo.db.similar_words.find_one({'_id': ObjectId(group_id)})
    if group is None:
        flash('Similar word group not found.', 'error')
        return redirect(url_for('similar_words.similar_words'))

    # 如果找到相似单词组，渲染编辑页面
    return render_template('edit_similar_words.html', group=group)



@similar_words_bp.route('/update/similar-words/<group_id>', methods=['POST'])
def update_similar_words(group_id):
    # 从表单获取数据
    words_str = request.form.get('words')
    words = [word.strip() for word in re.split('[,，;；]', words_str) if word.strip()]
    similarityType = request.form.get('similarityType')

    # 更新数据库记录
    mongo.db.similar_words.update_one(
        {'_id': ObjectId(group_id)},
        {'$set': {
            'words': words,
            'similarityType': similarityType
        }}
    )
    flash('Similar word group updated successfully!')
    return redirect(url_for('similar_words.similar_words'))


    
@similar_words_bp.route('/delete/similar-words/<groupId>')
def delete_similar_words(groupId):
    mongo.db.similar_words.delete_one({'_id': ObjectId(groupId)})
    flash('Word deleted successfully!')
    return redirect(url_for('similar_words.similar_words'))