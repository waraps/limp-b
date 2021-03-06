from db import db

invoice_product = db.Table('invoice_product', db.metadata,
    db.Column('invoice_id', db.Integer, db.ForeignKey('invoice.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
    db.Column('quantity', db.Float(precision=2), nullable=False)
)