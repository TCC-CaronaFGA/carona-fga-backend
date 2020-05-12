from project.api.models.rideModel import RequestRideModel
from project.api.models.rideModel import ResponseRideModel
from database import db
from project.api import bcrypt
from flask import current_app
import datetime
import jwt
import traceback

class UserModel(db.Model):
    __tablename__ = 'USER'

    idUser = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    course = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(11), nullable=False)
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
        idUser = self.idUser
        email = self.email
        name = self.name
        course = self.course
        phone = self.phone
        userType = self.userType
        gender = self.gender
        points = self.points
        notifications = RequestRideModel.find_request_pending_to_user(idUser)
        notificationsAnswer = ResponseRideModel.find_requested_by_user_json(idUser)
        return{
            'data': {
                'idUser': idUser,
                'email': email,
                'name': name,
                'course': course,
                'phone': phone,
                'userType': userType,
                'gender': gender,
                'points': points,
                'notifications': notifications,
                'notificationsAnswer': notificationsAnswer
            }
        }


    def to_min_json(self):
        idUser = self.idUser
        email = self.email
        name = self.name
        course = self.course
        phone = self.phone
        userType = self.userType
        gender = self.gender
        return{
            'data': {
                'idUser': idUser,
                'email': email,
                'name': name,
                'course': course,
                'phone': phone,
                'userType': userType,
                'gender': gender
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
            self_json = self.to_json()
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    days=30,
                    seconds=0
                ),
                'iat': datetime.datetime.utcnow(),
                'sub': self_json
            }
            return jwt.encode(
                payload,
                "secret_key_rocks_0edf07a1b8a5f5f1aed7580fffb69ce8972edc16a505916a77",
                algorithm='HS256'
            )
        except Exception as e:
            print(traceback.format_exc(), flush=True)
            return traceback.format_exc()

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(
                auth_token, "secret_key_rocks_0edf07a1b8a5f5f1aed7580fffb69ce8972edc16a505916a77")
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

