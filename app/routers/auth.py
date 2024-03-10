from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.user import User
from app import mongo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # 简单的验证逻辑
        user = mongo.db.users.find_one({'username': username})
        if user:
            flash('Username already exists.')
            return redirect(url_for('auth_bp.register'))

        # 创建新用户并保存到数据库
        hashed_password = generate_password_hash(password)
        mongo.db.users.insert_one({'username': username, 'email': email, 'password': hashed_password, 'points': 0})
        
        flash('Registration successful. Please log in.')
        return redirect(url_for('auth_bp.login'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = mongo.db.users.find_one({'username': username})
        if not user or not check_password_hash(user['password'], password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth_bp.login')) # 如果用户不存在或密码不正确，则重新定向到登录页面

        # 登录用户
        user_obj = User(username=user['username'], email=user['email'], password=password)
        login_user(user_obj, remember=True)
        return redirect(url_for('words_bp.index'))

    return render_template('login.html')