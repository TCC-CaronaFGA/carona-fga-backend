from database import db

""" 
CREATE TABLE RIDE (
    idRide INT NOT NULL AUTO_INCREMENT,
    dtRide DATETIME NOT NULL,
    availableSeats INT NOT NULL,
    notes VARCHAR(140) NOT NULL,
    cost NUMERIC(4,2) NOT NULL,
    idCar INT NOT NULL,
    idUser INT NOT NULL,
    CONSTRAINT RIDE_PK PRIMARY KEY (idRide),
    CONSTRAINT RIDE_CAR_FK FOREIGN KEY (idCar) REFERENCES CAR (idCar),
    CONSTRAINT RIDE_USER_FK FOREIGN KEY (idUser) REFERENCES USER(idUser)
)engine = InnoDB; """


class RideModel(db.Model):
    __tablename__ = 'RIDE'

    idRide = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dtRide = db.Column(db.DateTime, nullable=False)
    availableSeats = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.String(140), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    idCar = db.Column(db.Integer, db.ForeignKey('CAR.idCar'), nullable=False)
    idUser = db.Column(db.Integer, db.ForeignKey('USER.idUser'), nullable=False)

    def __init__(self, dtRide,availableSeats,notes,cost,idCar,idUser):
        self.dtRide = dtRide
        self.availableSeats = availableSeats
        self.notes = notes
        self.cost = cost
        self.idCar = idCar
        self.idUser = idUser

    def to_json(self):
        return{
            'data': {
                'idRide': self.idRide,
                'dtRide': self.dtRide,
                'availableSeats': self.availableSeats,
                'notes': self.notes,
                'cost': self.cost,
                'idCar': self.idCar
                'idUser': self.idUser
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
        return cls.query.filter_by(idCar=id).first()

    @classmethod
    def find_by_plate(cls, plate):
        return cls.query.filter_by(plate=plate).first()

    @classmethod
    def find_by_user(cls, idUser):
        return cls.query.filter_by(idUser=idUser).all()
