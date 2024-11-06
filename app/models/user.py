from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from bson.objectid import ObjectId 

class User(UserMixin):
    def __init__(self, username, email, password, _id=None):
        self._id = _id  # MongoDB 中的 _id 字段
        self.username = username
        self.email = email
        self.password_hash = password
        self.points = 0

    def set_password(self, password):
            self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        # 确保 _id 不是 None
        return str(self._id) if self._id else None

    @staticmethod
    def create_user(username, email, password):
        user_data = {
            'username': username,
            'email': email,
            'password_hash': User().set_password(password),
            'points': 0
        }
        mongo.db.users.insert_one(user_data)

    @staticmethod
    def find_by_username(username):
        user_data = mongo.db.users.find_one({'username': username})
        if user_data:
            return User(username=user_data['username'], email=user_data['email'], password=user_data['password_hash'])
        return None

    @staticmethod
    def find_by_email(email):
        user_data = mongo.db.users.find_one({'email': email})
        if user_data:
            return User(username=user_data['username'], email=user_data['email'], password=user_data['password_hash'])
        return None
