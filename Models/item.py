# import sqlite3
from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def findByName(cls, name):
        return cls.query.filter_by(name=name).first()
        '''
        connection = sqlite3.connect('Database.db')
        cursor = connection.cursor()

        select_query = "SELECT * FROM items where name=?"
        result = cursor.execute(select_query, (name,))
        row = result.fetchone()
        connection.close()
        return row
        '''

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        '''
        connection = sqlite3.connect('Database.db')
        cursor = connection.cursor()

        insert_query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(insert_query, (self.name, self.price))
        connection.commit()
        connection.close()
        '''

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        '''
        connection = sqlite3.connect('Database.db')
        cursor = connection.cursor()

        update_query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(update_query, (self.name,self.price)
        connection.commit()
        connection.close()
        '''