from datetime import datetime
from db import db

class RolModel(db.Model):
    __tablename__ = 'rol'

    id = db.Column(db.Integer, primary_key=True)
    rol = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    employee = db.relationship('EmployeeModel', backref=db.backref('rol'), lazy='dynamic')

    def json(self):
        return {
            'id': self.id,
            'rol': self.rol,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def save_to_db(self):
        db.session.add(self)
        db.sessioncommit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.get(_id)

    @classmethod
    def find_by_name(cls, rol):
        return cls.query.filter_by(rol=rol).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()