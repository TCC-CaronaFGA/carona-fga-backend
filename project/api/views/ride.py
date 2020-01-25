from flask import request, jsonify, Blueprint
from project.api.models.rideModel import RideModel
from database import db
from project.api import bcrypt
from project.api.utils import authenticate
import json
import sys

rides_blueprint = Blueprint('ride', __name__)

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

#Rides list route
@rides_blueprint.route('/api/rides', methods=['get'])
@authenticate
def ride_list(resp):

    if(not request.is_json):
        return jsonify(createFailMessage("Invalid Payload")), 400

    rides = RideModel.find_all()

    rides_json = []

    for ride in rides:
        ride_json = ride.to_json()['data']
        rides_json.append(ride_json)

    response_object = createSuccessMessage(None)
    response_object['data'] = rides_json
    return jsonify(response_object), 200


#User Rides list route
@rides_blueprint.route('/api/user/rides', methods=['get'])
@authenticate
def user_ride_list(resp):
    user = resp['data']

    if(not request.is_json):
        return jsonify(createFailMessage("Invalid Payload")), 400

    rides = RideModel.find_by_user(user['idUser'])

    rides_json = []

    for ride in rides:
        ride_json = ride.to_json()['data']
        rides_json.append(ride_json)

    response_object = createSuccessMessage(None)
    response_object['data'] = rides_json
    return jsonify(response_object), 200



#rides registration route
@rides_blueprint.route('/api/rides', methods=['POST'])
@authenticate
def ride_registration(resp):
    post_data = request.json
    user = resp['data']

    if(not request.is_json or not post_data):
        return jsonify(createFailMessage("Invalid Payload")), 400

    dtRide = post_data["dtRide"]
    availableSeats = post_data["availableSeats"]
    notes = post_data["notes"]
    cost = post_data["cost"]
    idCar = post_data["idCar"]
    idUser = user['idUser']

    ride = RideModel(dtRide, availableSeats, notes, cost, idCar,idUser)

    try:
        ride.save_to_db()
        response_object = createSuccessMessage('Carona criada com sucesso')
        response_object.update(ride.to_json())
        return jsonify(response_object), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(createFailMessage(e.message)), 503

#ride update route
@rides_blueprint.route('/api/rides/<idRide>', methods=['PATCH'])
@authenticate
def ride_update(resp, idRide):
    post_data = request.json
    user = resp['data']

    if(not request.is_json or not post_data):
        return jsonify(createFailMessage("Invalid Payload")), 400

    try:
        dtRide = post_data["dtRide"]
    except:
        dtRide = None
    try:
        availableSeats = post_data["availableSeats"]
    except:
        availableSeats = None
    try:
        notes = post_data["notes"]
    except:
        notes = None
    try:
        cost = post_data["cost"]
    except:
        cost = None
    try:
        idCar = post_data["idCar"]
    except:
        idCar = None

    ride = RideModel.find_by_id(idRide)
    
    if ride.idUser != user['idUser']:
        return jsonify(createFailMessage(None)), 400

    try:
        ride.dtRide = dtRide if dtRide is not None else ride.dtRide 
        ride.availableSeats = availableSeats if availableSeats is not None else ride.availableSeats 
        ride.notes = notes if notes is not None else ride.notes 
        ride.cost = cost if cost is not None else ride.cost 
        ride.idCar = idCar if idCar is not None else ride.idCar 
        db.session.commit()
        response_object = createSuccessMessage('Carona atualizada com sucesso.')
        response_object.update(ride.to_json())
        return jsonify(response_object), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(createFailMessage(e.message)), 503

#Ride delete route
@rides_blueprint.route('/api/rides/<idRide>', methods=['DELETE'])
@authenticate
def ride_delte(resp, idRide):
    user = resp['data']

    if(not request.is_json):
        return jsonify(createFailMessage("Invalid Payload")), 400

    ride = RideModel.find_by_id(idRide)

    if ride is None:
        return jsonify(createFailMessage(None)), 404


    if ride.idUser != user['idUser']:
        return jsonify(createFailMessage(None)), 400

    try:
        ride.delete_from_db()
        return jsonify(createSuccessMessage('Carona deletada com sucesso.')), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(createFailMessage(e.message)), 503