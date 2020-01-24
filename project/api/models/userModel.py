from database import db
from project.api import bcrypt
from flask import current_app
import datetime
import jwt

class UserModel(db.Model):
    __tablename__ = 'USER'

    idUser = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    course = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    userType = db.Column(db.String(1), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, email,name,course,phone,userType,gender,password,points):
        self.email = email
        self.name = name
        self.course = course
        self.phone = phone
        self.userType = userType
        self.gender = gender
        self.points = points
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get('BCRYPT_LOG_ROUNDS')).decode()

    def to_json(self):
        return{
            'data': {
                'idUser': self.idUser,
                'email': self.email,
                'name': self.name,
                'course': self.course,
                'phone': self.phone,
                'userType': self.userType,
                'gender': self.gender,
                'points': self.points
            }
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(idUser=id).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def encode_auth_token(self):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    days=current_app.config.get('TOKEN_EXPIRATION_DAYS'),
                    seconds=current_app.config.get('TOKEN_EXPIRATION_SECONDS')
                ),
                'iat': datetime.datetime.utcnow(),
                'sub': self.to_json()
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(
                auth_token, current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

