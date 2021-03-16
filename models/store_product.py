from datetime import datetime
from db import db

class StoreProductModel(db.Model):
    __tablename__ = 'store_product'

    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    stock = db.Column(db.Float(precision=2), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    store = db.relationship('StoreModel', backref=db.backref('store_product'))
    products = db.relationship('ProductModel', backref=db.backref('store_product'))

    def __repr__(self):
        return "<StoreProduct(id='%s' store_id='%s', product_id='%s', stock='%s')>" % (
                                self.id, self.store_id, self.product_id, self.stock)

    def json(self):
        print(self.products)
        return {
            'id': self.id,
            'store_id': self.store_id,
            'store': self.store.json(),
            'product_id': self.product_id,
            'product': self.products.json() if self.products else None,
            'stock': self.stock,
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
    def find_by_composite_id(cls, store_id, product_id):
        return cls.query.filter_by(store_id=store_id, product_id=product_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()