# src/models/entities/User.py

import bcrypt
from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, id, username, password, fullname="", role="") -> None:
        self.id = id
        self.username = username
        self.password = password
        self.fullname = fullname
        self.role = role

    @classmethod
    def check_password(cls, hashed_password, password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
