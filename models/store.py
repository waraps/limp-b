from datetime import datetime
from db import db

from models.store_product import store_product

class StoreModel(db.Model):
    __tablename__ = 'store'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(120), nullable=False)
    mail = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    employees = db.relationship('EmployeeModel', backref=db.backref('store'), lazy='dynamic')
    products = db.relationship('ProductModel', secondary=store_product, backref=db.backref("products"))
    invoices = db.relationship('InvoiceModel', backref=db.backref('store'), lazy='dynamic')

    def __repr__(self):
        return "<Store(id='%s' name='%s', created_at='%s')>" % (
                                self.id, self.name, self.created_at)

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'mail': self.mail,
            'phone': self.phone,
            'created_at': self.created_at.strftime("%d/%m/%Y %H:%M:%S"),
            'updated_at': self.updated_at.strftime("%d/%m/%Y %H:%M:%S")
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        print(self)

    def delete_from_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.get(_id)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()