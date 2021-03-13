from datetime import datetime
from db import db

class StoreProductModel(db.Model):
    __tablename__ = 'store_product'

    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    stock = db.Column('stock', db.Float(precision=2), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    store = db.relationship('StoreModel', backref=db.backref('store_product'))
    products = db.relationship('ProductModel', backref=db.backref('store_product'))