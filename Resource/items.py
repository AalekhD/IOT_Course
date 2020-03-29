from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from Models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.findByName(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.findByName(name) is not None:
            return {'message': "Item '{}' already exists..cannot create new".format(name)}, 400  # return bad request

        # requested_data = request.get_json()
        requested_data = Item.parser.parse_args()
        item = ItemModel(name, requested_data['price'])
        try:
            item.save_to_db()
        except:
            print('Error occurred')
            return {'message': 'Error occurred inserting the data...'}
        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.findByName(name)
        print(item)
        if item:
            item.delete_from_db()
        else:
            return {'message': 'Item Not Found'}
        '''
        connection = sqlite3.connect('Database.db')
        cursor = connection.cursor()

        insert_query = "DELETE FROM items WHERE name=?"
        cursor.execute(insert_query, (name,))
        connection.commit()
        connection.close()
        '''
        return {'message': 'Item deleted'}

    def put(self, name):
        # data = request.get_json()
        data = Item.parser.parse_args()
        item = ItemModel.findByName(name)

        if item is None:
            item = ItemModel(name, data['price'])
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
        # connection = sqlite3.connect('Database.db')
        # cursor = connection.cursor()
        #
        # select_query = "SELECT * FROM items "
        # result = cursor.execute(select_query)
        # items = []
        # for row in result:
        #     items.append({'name': row[0], 'price': row[1]})
        #
        # connection.close()
        # return {'items': items}, 200s


