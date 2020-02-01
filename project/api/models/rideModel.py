from database import db
from datetime import datetime
import json

class RideModel(db.Model):
    __tablename__ = 'RIDE'

    idRide = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dtRide = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(140), nullable=False)
    origin = db.Column(db.String(140), nullable=False)
    destiny = db.Column(db.String(140), nullable=False)
    availableSeats = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.String(140), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    finished = db.Column(db.Boolean, nullable=False)
    idCar = db.Column(db.Integer, db.ForeignKey('CAR.idCar'), nullable=False)
    idUser = db.Column(db.Integer, db.ForeignKey('USER.idUser'), nullable=False)

    def __init__(self, dtRide,availableSeats,notes,cost,idCar,idUser,location,origin,destiny,finished):
        self.dtRide = dtRide
        self.availableSeats = availableSeats
        self.notes = notes
        self.cost = cost
        self.idCar = idCar
        self.idUser = idUser
        self.location = location
        self.origin = origin
        self.destiny = destiny
        self.finished = finished

    def to_json(self):
        requests = RequestRideModel.find_approved_request_by_ride(self.idRide)
        availableSeats = self.availableSeats
        for request in requests:
            request_json = request.to_json()['data']
            availableSeats = availableSeats - request_json['requestedSeats']


        return{
            'data': {
                'idRide': self.idRide,
                'dtRide': self.dtRide,
                'location': self.location,
                'origin': self.origin,
                'destiny': self.destiny,
                'availableSeats': availableSeats,
                'notes': self.notes,
                'cost': self.cost,
                'idCar': self.idCar,
                'idUser': self.idUser,
                'finished': self.finished,
            }
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(idRide=id).first()

    @classmethod
    def find_all(cls):
        now = datetime.now().utcnow()
        return db.session.query(RideModel).filter(RideModel.dtRide >= now).all()

    @classmethod
    def find_by_plate(cls, plate):
        return cls.query.filter_by(plate=plate).first()

    @classmethod
    def find_by_user(cls, idUser):
        return cls.query.filter_by(idUser=idUser).all()


class RequestRideModel(db.Model):
    __tablename__ = 'REQUEST_RIDE'

    idRequest = db.Column(db.Integer, primary_key=True, autoincrement=True)
    requestedSeats = db.Column(db.Integer, nullable=False)
    requestStatus = db.Column(db.String(1), nullable=False)
    idRide = db.Column(db.Integer, db.ForeignKey('RIDE.idRide'), nullable=False)
    idPassenger = db.Column(db.Integer, db.ForeignKey('USER.idUser'), nullable=False)

    def __init__(self,requestedSeats,idRide,idPassenger):
        self.requestedSeats = requestedSeats
        self.requestStatus = "P"
        self.idRide = idRide
        self.idPassenger = idPassenger

    def to_json(self):
        return{
            'data': {
                'idRequest': self.idRequest,
                'requestedSeats': self.requestedSeats,
                'requestStatus': self.requestStatus,
                'idRide': self.idRide,
                'idPassenger': self.idPassenger,
            }
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    def answer_yes(self):
        self.requestStatus = "A"
        db.session.commit()

    def answer_no(self):
        self.requestStatus = "R"
        db.session.commit()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(idRequest=id).first()

    @classmethod
    def find_requested_by_user(cls, idUser):
        return cls.query.filter_by(idPassenger=idUser).all()

    @classmethod
    def find_request_by_ride(cls, idRide):
        return cls.query.filter_by(idRide=idRide).all()

    @classmethod
    def find_approved_request_by_ride(cls, idRide):
        return db.session.query(RequestRideModel).filter(RequestRideModel.idRide == idRide).filter(RequestRideModel.requestStatus == "A").all()

    @classmethod
    def find_approved_request_by_ride_json(cls, idRide):
        from project.api.models.userModel import UserModel
        requests = RequestRideModel.find_approved_request_by_ride(idRide)
        requests_json = []
        for request in requests:
            idPassenger = request.idPassenger
            user = UserModel.find_by_id(idPassenger).to_json()['data']
            user.update(requestedSeats = request.requestedSeats)
            requests_json.append(user)
        return requests_json


    @classmethod
    def find_request_pending_to_user(cls, idUser):
        rideList = RideModel.find_by_user(idUser)
        requests_json = []
        for ride in rideList:
            rideRequests = db.session.query(RequestRideModel).filter(RequestRideModel.idRide == ride.idRide).filter(RequestRideModel.requestStatus == "P").all()
            for rideRequest in rideRequests:
                request_json = rideRequest.to_json()['data']
                requests_json.append(request_json)
        return requests_json


class ResponseRideModel(db.Model):
    __tablename__ = 'RESPONSE_RIDE'

    answer = db.Column(db.String(1), nullable=False)
    alreadySeen = db.Column(db.Boolean, nullable=False)
    idRequest = db.Column(db.Integer,db.ForeignKey('REQUEST_RIDE.idRequest'), nullable=False, primary_key=True)
    idPassenger = db.Column(db.Integer, db.ForeignKey('USER.idUser'), nullable=False, primary_key=True)
    

    def __init__(self,idRequest,idPassenger, answer):
        self.idRequest = idRequest
        self.idPassenger = idPassenger
        self.alreadySeen = False
        self.answer = answer

    def to_json(self):
        return{
            'data': {
                'idRequest': self.idRequest,
                'idPassenger': self.idPassenger,
                'alreadySeen': self.alreadySeen,
                'answer': self.answer
            }
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(idRequest=id).all()

    @classmethod
    def find_requested_by_user(cls, idUser):
        return db.session.query(ResponseRideModel).filter(ResponseRideModel.idPassenger == idUser).filter(ResponseRideModel.alreadySeen == False).all()

    @classmethod
    def find_requested_by_user_json(cls, idUser):
        answers = ResponseRideModel.find_requested_by_user(idUser)
        json = []
        for answer in answers:
            json.append(answer.to_json()['data'])
        return json
