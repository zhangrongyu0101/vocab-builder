from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_pymongo import ObjectId
from . import mongo

main = Blueprint('main', __name__)

@main.route('/')
def index():
    words = mongo.db.words.find()
    return render_template('index.html', words=words)

@main.route('/add', methods=['POST'])
def add_word():
    word = request.form.get('word')
    translation = request.form.get('translation')
    usage = request.form.get('usage')

    if word and translation:  # 简单的验证
        mongo.db.words.insert_one({'word': word, 'translation': translation, 'usage': usage})
        flash('Word added successfully!')
    else:
        flash('Word and Translation cannot be empty!')

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
