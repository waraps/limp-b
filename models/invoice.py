from datetime import datetime
from db import db

from invoice_product import invoice_product

class InvoiceModel(db.Model):
    __tablename__ = 'invoice'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(15), nullable=False, required=True)
    mount = db.Column(db.Float(precision=2), nullable=False, required=True)
    status = db.Column(db.Boolean, nullable=False, required=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    tienda_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    rate_id = db.Column(db.Integer, db.ForeignKey('rate.id'))

    products = db.relationship('ProductModel', secondary=invoice_product, db.backref="products")

    def json(self):
        return {
            'id': self.id,
            'code': self.code,
            'mount': self.mount,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.get(_id)

    @classmethod
    def find_all(cls):
        return cls.query.all()
    