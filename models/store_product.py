from db import db

store_product = db.Table('store_product', db.metadata,
    db.Column('store_id', db.Integer, db.ForeignKey('store.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
    db.Column('stock', db.Float(precision=2), nullable=False)
)