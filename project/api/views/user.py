from flask import request, jsonify, Blueprint
from project.api.models.userModel import UserModel
from database import db
from project.api import bcrypt
from project.api.utils import authenticate

users_blueprint = Blueprint('users', __name__)


def createFailMessage(message):
    response_object = {
        'status': 'fail',
        'message': '{}'.format(message)
    }
    return response_object


def createSuccessMessage(message):
    response_object = {
        'status': 'success',
        'message': '{}'.format(message)
    }
    return response_object

# User Registration Route
@users_blueprint.route('/api/auth/registration', methods=['POST'])
def user_registration():
    post_data = request.json

    if(not request.is_json or not post_data):
        return jsonify(createFailMessage("Invalid Payload")), 400

    email = post_data["email"]
    name = post_data["name"]
    course = post_data["course"]
    phone = post_data["phone"]
    userType = post_data["userType"]
    gender = post_data["gender"]
    password = post_data["password"]

    user = UserModel(email,name,course,phone,userType,gender,password,0)

    if UserModel.find_by_email(email):
        return jsonify(createFailMessage('{} already exists'.format(email))), 400

    try:
        user.save_to_db()
        auth_token = user.encode_auth_token()
        response_object = createSuccessMessage('User was created')
        response_object["auth_token"] = auth_token.decode()
        response_object.update(user.to_json())
        return jsonify(response_object), 201
    except Exception as e:
        db.session.rollback()
        return jsonify(createFailMessage(e.message)), 503
        # User Login Route


@users_blueprint.route('/api/auth/login', methods=['POST'])
def user_login():
    post_data = request.json

    if(not request.is_json or not post_data):
        return jsonify(createFailMessage("Invalid Payload")), 400

    email = post_data["email"]
    password = post_data["password"]

    try:
        current_user = UserModel.find_by_email(email)

        if not current_user:
            return jsonify(createFailMessage('User {} doesn\'t exist'.format(email))), 404

        if current_user and bcrypt.check_password_hash(current_user.password, password):
            auth_token = current_user.encode_auth_token()
            response_object = createSuccessMessage('Successfully logged in.')
            response_object["auth_token"] = auth_token.decode()
            response_object.update(current_user.to_json())
            return jsonify(response_object), 200
        else:
            return jsonify(createFailMessage('Wrong Credentials')), 401
    except Exception as e:
        return jsonify(createFailMessage(e.message)), 503

# Logout for access
@users_blueprint.route('/api/auth/logout', methods=['GET'])
@authenticate
def user_logout(resp):
    response_object = {
        'status': 'success',
        'message': 'Successfully logged out.'
    }
    return jsonify(response_object), 200


@users_blueprint.route('/api/auth/status', methods=['GET'])
@authenticate
def get_user_status(resp):
    response_object = {
        'status': 'success',
        'message': 'success',
        'data': resp
    }
    return jsonify(response_object), 200
