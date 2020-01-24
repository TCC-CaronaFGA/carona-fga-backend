from database import db

class CarModel(db.Model):
    __tablename__ = 'CAR'

    idCar = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plate = db.Column(db.String(7), unique=True, nullable=False)
    color = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    model = db.Column(db.String(20), nullable=False)
    idUser = db.Column(db.Integer, db.ForeignKey('USER.idUser'), nullable=False)

    def __init__(self, plate,color,year,model,idUser):
        self.plate = plate
        self.color = color
        self.year = year
        self.model = model
        self.idUser = idUser

    def to_json(self):
        return{
            'data': {
                'idCar': self.idCar,
                'plate': self.plate,
                'color': self.color,
                'year': self.year,
                'model': self.model,
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
