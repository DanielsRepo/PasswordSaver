from . import db
from flask_login import UserMixin
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256), unique=True, nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String(256))
    password = db.Column(db.LargeBinary)
    key = db.Column(db.LargeBinary)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))

    def save_password(self, password):
        self.key = Fernet.generate_key()
        self.password = Fernet(self.key).encrypt(password.encode())

    def decrypt_password(self, password):
        return Fernet(self.key).decrypt(password).decode()

    @staticmethod
    def delete_password(password_id):
        Password.query.filter_by(id=password_id).delete()


db.create_all()
