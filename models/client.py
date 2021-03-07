from datetime import datetime
from db import db

class ClientModel(db.Model):
    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    mail = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(80), nullable=False)
    dni = db.Column(db.String(80), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    invoices = db.relationship('InvoiceModel', backref=db.backref('client'), lazy='dynamic')

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'lastname': self.lastname,
            'mail': self.mail,
            'phone': self.phone,
            'dni': self.dni,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.get(_id)

    @classmethod
    def find_by_dni(cls, dni):
        return cls.query.filter_by(dni=dni).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()