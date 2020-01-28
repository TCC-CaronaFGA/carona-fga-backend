from flask import request, jsonify, Blueprint
from project.api.models.carModel import CarModel
from database import db
from project.api import bcrypt
from project.api.utils import authenticate
import json
import sys

cars_blueprint = Blueprint('car', __name__)


def createFailMessage(message):
    response_object = {
        'status': 'fail',
        'message': '{}'.format(message)
    }
    return response_object


def createSuccessMessage(message):
    response_object = {
        'status': 'success',
    }
    if message is not None:
        response_object['message'] = '{}'.format(message)
        
    return response_object

#Cars list route
@cars_blueprint.route('/api/cars', methods=['get'])
@authenticate
def car_list(resp):
    user = resp['data']

    if(not request.is_json):
        return jsonify(createFailMessage("Invalid Payload")), 400

    idUser = user['idUser']

    cars = CarModel.find_by_user(idUser)

    cars_json = []

    for car in cars:
        car_json = car.to_json()['data']
        cars_json.append(car_json)

    response_object = createSuccessMessage(None)
    response_object['data'] = cars_json
    return jsonify(response_object), 200


#Cars registration route
@cars_blueprint.route('/api/cars', methods=['POST'])
@authenticate
def car_registration(resp):
    post_data = request.json
    user = resp['data']

    if(not request.is_json or not post_data):
        return jsonify(createFailMessage("Invalid Payload.")), 400

    plate = post_data["plate"]
    color = post_data["color"]
    year = post_data["year"]
    model = post_data["model"]
    idUser = user['idUser']

    car = CarModel(plate, color, year, model, idUser)

    if CarModel.find_by_plate(plate):
        return jsonify(createFailMessage('{} já está cadastrado.'.format(plate))), 400

    try:
        car.save_to_db()
        response_object = createSuccessMessage('Carro criado com sucesso.')
        response_object.update(car.to_json())
        return jsonify(response_object), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(createFailMessage(e)), 503

#Car update route
@cars_blueprint.route('/api/cars/<idCar>', methods=['PATCH'])
@authenticate
def car_update(resp, idCar):
    post_data = request.json
    user = resp['data']

    if(not request.is_json or not post_data):
        return jsonify(createFailMessage("Invalid Payload")), 400
    try:
        plate = post_data["plate"]
    except:
        plate = None
    try:
        color = post_data["color"]
    except:
        color = None
    try:
        year = post_data["year"]
    except:
        year = None
    try:
        model = post_data["model"]
    except:
        model = None

    car = CarModel.find_by_id(idCar)

    if car.idUser != user['idUser']:
        return jsonify(createFailMessage('{} não pertence a você.'.format(plate))), 400

    try:
        car.plate = plate if plate is not None else car.plate 
        car.color = color if color is not None else car.color 
        car.year = year if year is not None else car.year 
        car.model = model if model is not None else car.model 
        db.session.commit()
        response_object = createSuccessMessage('Dados do carro atualizados com sucesso.')
        response_object.update(car.to_json())
        return jsonify(response_object), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(createFailMessage(e)), 503

#Car delete route
@cars_blueprint.route('/api/cars/<idCar>', methods=['DELETE'])
@authenticate
def car_delte(resp, idCar):
    user = resp['data']

    if(not request.is_json):
        return jsonify(createFailMessage("Invalid Payload")), 400

    car = CarModel.find_by_id(idCar)

    if car is None:
        return jsonify(createFailMessage('{} não existe'.format(idCar))), 404


    if car.idUser != user['idUser']:
        return jsonify(createFailMessage('{} não pertence a você'.format(idCar))), 400

    try:
        car.delete_from_db()
        return jsonify(createSuccessMessage('Carro deletado com sucesso.')), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(createFailMessage(e)), 503
