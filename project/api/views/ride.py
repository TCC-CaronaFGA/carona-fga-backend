from flask import request, jsonify, Blueprint
from project.api.models.rideModel import RideModel
from project.api.models.rideModel import RequestRideModel
from project.api.models.rideModel import ResponseRideModel
from database import db
from project.api import bcrypt
from project.api.utils import authenticate
import json
import sys
import datetime

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

    # dtRide = post_data["dtRide"]
    format = '%Y-%m-%d %H:%M'
    dtRide = datetime.datetime.strptime(post_data["dtRide"], format)
    location = post_data["location"]
    origin = post_data["origin"]
    destiny = post_data["destiny"]
    availableSeats = post_data["availableSeats"]
    try:
        notes = post_data["notes"]
    except:
        notes = ''
    cost = post_data["cost"]
    idCar = post_data["idCar"]
    idUser = user['idUser']
    finished = False

    ride = RideModel(dtRide,availableSeats,notes,cost,idCar,idUser,location,origin,destiny,finished)

    try:
        ride.save_to_db()
        response_object = createSuccessMessage('Carona criada com sucesso')
        response_object.update(ride.to_json())
        return jsonify(response_object), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(createFailMessage(e)), 503

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
        location = post_data["location"]
    except:
        location = None
    try:
        origin = post_data["origin"]
    except:
        origin = None
    try:
        destiny = post_data["destiny"]
    except:
        destiny = None
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
    try:
        finished = post_data["finished"]
    except:
        finished = None

    ride = RideModel.find_by_id(idRide)
    
    if ride.idUser != user['idUser']:
        return jsonify(createFailMessage(None)), 400

    try:
        ride.dtRide = dtRide if dtRide is not None else ride.dtRide 
        ride.location = location if location is not None else ride.location 
        ride.origin = origin if origin is not None else ride.origin 
        ride.destiny = destiny if destiny is not None else ride.destiny 
        ride.availableSeats = availableSeats if availableSeats is not None else ride.availableSeats 
        ride.notes = notes if notes is not None else ride.notes 
        ride.cost = cost if cost is not None else ride.cost 
        ride.idCar = idCar if idCar is not None else ride.idCar 
        ride.finished = finished if finished is not None else ride.finished 
        db.session.commit()
        response_object = createSuccessMessage('Carona atualizada com sucesso.')
        response_object.update(ride.to_json())
        return jsonify(response_object), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(createFailMessage(e)), 503

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
        return jsonify(createFailMessage(e)), 503

#Ride information get
@rides_blueprint.route('/api/rides/<idRide>', methods=['GET'])
@authenticate
def ride_info(resp, idRide):
    user = resp['data']

    ride = RideModel.find_by_id(idRide)


    if ride is None:
        return jsonify(createFailMessage(None)), 404

    approved_requests = RequestRideModel.find_approved_request_by_ride_json(ride.idRide)

    try:
        json = createSuccessMessage('Requisição enviada com sucesso.')
        json.update(ride.to_json())
        json['data']['passengers'] = approved_requests
        return jsonify(json), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(createFailMessage(e)), 503

#Ride solicitation create
@rides_blueprint.route('/api/rides/<idRide>', methods=['POST'])
@authenticate
def ride_join(resp, idRide):
    user = resp['data']
    post_data = request.json
    requestedSeats = post_data["requestedSeats"]

    ride = RideModel.find_by_id(idRide)

    if ride is None:
        return jsonify(createFailMessage(None)), 404


    if ride.idUser == user['idUser']:
        return jsonify(createFailMessage("Requisitante da carona e o dono são o mesmo usuário.")), 400

    requestRide = RequestRideModel(requestedSeats, idRide, user['idUser'])

    try:
        requestRide.save_to_db()
        return jsonify(createSuccessMessage('Requisição enviada com sucesso.')), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(createFailMessage(e)), 503

#Aceitar solicitação
@rides_blueprint.route('/api/requests/<idRequest>/<requestAnswer>', methods=['POST'])
@authenticate
def request_answer(resp, idRequest  , requestAnswer):
    user = resp['data']
    request = RequestRideModel.find_by_id(idRequest)
    print(request.to_json(), flush=True)

    if request is None:
        return jsonify(createFailMessage(None)), 404

    if request.requestStatus != "P":
        return jsonify("Essa solicitação já foi respondida."), 400

    ride = RideModel.find_by_id(request.idRide)

    if ride.idUser != user['idUser']:
        return jsonify(createFailMessage(None)), 400

    try:
        response = ResponseRideModel(request.idRequest, request.idPassenger, "P")
        if requestAnswer == "1":
            setattr(request, 'requestStatus', "A") 
            response.answer = "A" 
        else:
            setattr(request, 'requestStatus', "R") 
            response.answer = "R" 

        response.save_to_db()

        response_object = createSuccessMessage('Requisição respondida com sucesso.')
        return jsonify(response_object), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(createFailMessage(e)), 503



#notification read route
@rides_blueprint.route('/api/notifications/read', methods=['POST'])
@authenticate
def read_notifications(resp):
    user = resp['data']

    answers = ResponseRideModel.find_requested_by_user(user['idUser'])

    try:   
        for answer in answers:
            answer.alreadySeen = True
        db.session.commit()
        return jsonify(createSuccessMessage('Notificações lidas com sucesso.')), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(createFailMessage(e)), 503
