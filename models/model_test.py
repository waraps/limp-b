from datetime import datetime
from db import db

class ModelTest(db.Model):
    __tablename__ = 'model'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return "<Test(id='%s' name='%s')>" % (
                                self.id, self.name)

    def json(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def save_to_db(self):
        print(self)