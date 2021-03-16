from datetime import datetime
from db import db

class InvoiceProductModel(db.Model):
    __tablename__ = 'invoice_product'

    id = db.Column(db.Integer. primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)
    store_product_id = db.Column(db.Integer, db.ForeignKey('store_product.id'), nullable=False)
    quantity = db.Column('quantity', db.Float(precision=2), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    invoice = db.relationship('InvoiceModel', backref=db.backref('invoice_product'))
    store_product = db.relationship('StoreProductModel', backref=db.backref('invoice_product'))

    def json(self):
        return {
            'id': self.id,
            'invoice_id': self.invoice_id,
            'invoice': self.invoice.json(),
            'store_product_id': self.store_product_id,
            'store_product': self.store_product.json() if self.store_product else None,
            'quantity': self.quantity,
            'created_at': self.created_at.strftime("%d/%m/%Y %H:%M:%S"),
            'update_at': self.updated_at.strftime("%d/%m/%Y %H:%M:%S"),
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
    def find_by_composite_id(cls, invoice_id, store_product_id):
        return cls.query.filter_by(invoice_id=invoice_id, store_product_id=store_product_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()