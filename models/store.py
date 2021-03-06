from datetime import datetime
from db import db

from store_product import store_product

class StoreModel(db.Model):
    __tablename__ = 'store'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    employees = db.relationship('EmployeeModel', db.backref='store', lazy='dynamic')
    products = db.relationship('ProductModel', secondary=store_product, db.backref="products")
    invoices = db.relationship('InvoiceModel', db.backref='store', lazy='dynamic')

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
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
    def find_by_id(cls):
        return cls.query.all()