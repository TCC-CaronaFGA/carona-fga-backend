"""

CREATE TABLE RATING (
    idRide INT NOT NULL,
    rating INT NOT NULL,
    comment VARCHAR(140) NOT NULL,
    idUser INT NOT NULL,
    CONSTRAINT RATING_USER_FK FOREIGN KEY (idUser) REFERENCES USER (idUser),
    CONSTRAINT RATING_RIDE_FK FOREIGN KEY (idRide) REFERENCES RIDE (idRide)
)engine = InnoDB;"""
from project.api.models.rideModel import RideModel
from database import db

class RatingModel(db.Model):
    __tablename__ = 'RATING'

    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(140), nullable=False)
    idRide = db.Column(db.Integer, primary_key=True) db.ForeignKey('RIDE.idRide', nullable=False)
    idUser = db.Column(db.Integer, primary_key=True, db.ForeignKey('USER.idUser'), nullable=False)
    idRated = db.Column(db.Integer, primary_key=True, db.ForeignKey('USER.idUser'), nullable=False)

    def __init__(self, idRide,rating,comment,idUser,idRated):
        self.rating = rating
        self.comment = comment
        self.idRide = idRide
        self.idUser = idUser
        self.idRated = idRated

    def to_json(self):
        return{
            'data': {
                'rating': self.rating,
                'comment': self.comment,
                'idRide': self.idRide,
                'idUser': self.idUser,
                'idRated': self.idRated
            }
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_plate(cls, plate):
        return cls.query.filter_by(plate=plate).first()

    @classmethod
    def find_by_user(cls, idUser):
        return cls.query.filter_by(idRated=idUser).all()

    @classmethod
    def average_by_user(cls, idUser):
        ratings = cls.query.filter_by(idRated=idUser).all()
        ratingSum = 0
        ratingItems=0
        if(len(ratings) == 0):
            return 0
        else:
            for rating in ratings
                
        return 
