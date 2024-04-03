# 主要单词增删改查功能
from flask import Blueprint, request, redirect, url_for, flash
from flask_pymongo import ObjectId
from flask import Flask, request, jsonify
from flask import current_app, render_template
from app import mongo
from flask import render_template
from flask_login import login_required, current_user
from bson.objectid import ObjectId
import gridfs
from werkzeug.utils import secure_filename
import base64

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
    
    count = mongo.db.words.count_documents({})

    return render_template('index.html', words=words_list, user_score=user_score, word_count=count)


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

@words_bp.route('/edit_by_word/<word>')
def edit_by_word(word):
    find = mongo.db.words.find_one({'word': word})
    if find is None:
        # 插入新单词并获取其_id
        result = mongo.db.words.insert_one({
            'word': word,
            'dictation_count': 0
        })
        # 重定向到编辑页面，使用插入文档的_id
        word_id = result.inserted_id
    else:
        # 如果单词已存在，使用找到的单词的_id
        word_id = find['_id']

    # 重定向到edit_word视图函数，传入word_id
    return redirect(url_for('words_bp.edit_word', word_id=word_id))
    

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


# 动态创建 fs 实例的函数
def get_fs():
    fs = gridfs.GridFS(mongo.db)
    return fs

@words_bp.route('/word/upload-image/<word_id>', methods=['GET'])
def show_upload_image_form(word_id):
    fs = gridfs.GridFS(mongo.db)
    word = mongo.db.words.find_one({"_id": ObjectId(word_id)})

    # 转换ObjectId为字符串
    word_id_str = str(word['_id'])
    # 如果单词中包含图片ID，获取这些图片的数据
    images_data = []
    if 'images' in word:
        for image_id in word['images']:
            image_file = fs.get(ObjectId(image_id))
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
            images_data.append({'id': str(image_id), 'data': image_data})

    return render_template('upload_image.html', word_id=word_id_str, word=word, images=images_data)


@words_bp.route('/word/upload-image/<word_id>', methods=['POST'])
def upload_image_for_word(word_id):
    fs = get_fs()
    image_file = request.files.get('image')
    
    if image_file:
        filename = secure_filename(image_file.filename)
        content_type = image_file.content_type
        # 存储图片到GridFS
        image_id = fs.put(image_file, filename=filename, content_type=content_type)
        
        # 根据提供的word_id更新单词记录以包含图片ID
        result = mongo.db.words.update_one({'_id': ObjectId(word_id)}, {'$push': {'images': image_id}})
        
        if result.matched_count > 0:
            flash('Image uploaded successfully.')
        else:
            flash('Word not found.')
    else:
        flash('No image selected.')
    
    return redirect(url_for('words_bp.show_upload_image_form', word_id=word_id))

@words_bp.route('/word/<word_id>/delete-image/<image_id>', methods=['DELETE'])
def delete_image(word_id, image_id):
    fs = get_fs()
    try:
        # 从单词文档中移除图片ID
        mongo.db.words.update_one(
            {"_id": ObjectId(word_id)},
            {"$pull": {"images": ObjectId(image_id)}}
        )
        # 从GridFS中删除图片文件
        fs.delete(ObjectId(image_id))
        return jsonify({"message": "Image deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    