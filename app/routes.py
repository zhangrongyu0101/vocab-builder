from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify
from flask_pymongo import ObjectId
from . import mongo
import random
import csv
from io import StringIO
from flask import Flask, request, Response
import requests
from bs4 import BeautifulSoup
from flask import Flask, request
import requests
import re
from urllib.parse import quote 
import html

from googletrans import Translator, LANGUAGES

main = Blueprint('main', __name__)


@main.route('/dictation')
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


@main.route('/')
def index():
    # 使用 _id 字段逆序排序单词
    words_list = list(mongo.db.words.find().sort('_id', -1))
    return render_template('index.html', words=words_list)


@main.route('/add', methods=['POST'])
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



@main.route('/edit/<word_id>')
def edit_word(word_id):
    word = mongo.db.words.find_one({'_id': ObjectId(word_id)})
    return render_template('edit_word.html', word=word)

@main.route('/update/<word_id>', methods=['POST'])
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

@main.route('/delete/<word_id>')
def delete_word(word_id):
    mongo.db.words.delete_one({'_id': ObjectId(word_id)})
    flash('Word deleted successfully!')
    return redirect(url_for('main.index'))


@main.route('/check-word', methods=['POST'])
def check_word():
    data = request.get_json()  # 使用 get_json 方法
    input_word = data.get('inputWord')
    correct_word = data.get('correctWord')
    
    # 这里添加你的逻辑来检查单词是否正确
    if input_word.lower() == correct_word.lower():
        return jsonify({'message': 'Correct!'})
    else:
        return jsonify({'message': 'Incorrect, try again.'})


@main.route('/new-word', methods=['GET'])
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

@main.route('/import-words', methods=['POST'])
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


@main.route('/increment-dictation-count/<word_id>', methods=['POST'])
def increment_dictation_count(word_id):
    mongo.db.words.update_one(
        {'_id': ObjectId(word_id)},
        {'$inc': {'dictation_count': 1}}
    )
    return jsonify({'message': 'Dictation count incremented successfully'})

#----------------------谷歌api后端-------------------------

# 定义Google翻译API的URL

GOOGLE_TRANSLATE_URL = "https://translate.googleapis.com/translate_a/single"
GOOGLE_TTS_URL = "http://translate.google.com/translate_tts"
# GOOGLE_TRANSLATE_URL = 'http://translate.google.com/m?q=%s&tl=%s&sl=%s'

@main.route('/translate', methods=['GET'])
def translate():
    text = request.args.get('text', '')
    # 设置源语言为英文
    source = 'en'
    # 设置目标语言为简体中文
    target = 'zh-CN'
    params = {
        'client': 'gtx',
        'sl': source,
        'tl': target,
        'dt': 't',
        'q': text,
    }
    
    # 定义代理配置
    proxies = {
        "http": "http://127.0.0.1:4780",  # 替换为你的HTTP代理地址
        "https": "https://127.0.0.1:4780",  # 替换为你的HTTPS代理地址
    }
    
    try:
        response = requests.get(GOOGLE_TRANSLATE_URL, params=params, proxies=proxies)
        response.raise_for_status()
        # 简化响应处理，直接返回第一个翻译结果
        translation = response.json()[0][0][0]
        return jsonify({'translation': translation})
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

@main.route('/pronounce', methods=['GET'])
def pronounce():
    text = request.args.get('text', '')
    lang = request.args.get('lang', 'en')
    params = {
        'client': 'tw-ob',
        'ie': 'UTF-8',
        'tl': lang,
        'q': text,
    }
    try:
        response = requests.get(GOOGLE_TTS_URL, params=params, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        # 直接返回音频数据
        return Response(response.content, mimetype='audio/mpeg')
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500