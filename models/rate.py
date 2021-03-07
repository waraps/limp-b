from datetime import datetime
from db import db

class RateModel(db.Model):
    __tablename__ = 'rate'

    id = db.Column(db.Integer, primary_key=True)
    rate = db.Column(db.Float(precision=2), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    invoices = db.relationship('InvoiceModel', backref=db.backref('rate'), lazy='dynamic')

    def json(self):
        return {
            'id': self.id,
            'rate': self.rate,
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
    def find_all(cls):
        return cls.query.all()