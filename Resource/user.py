import sqlite3
from flask_restful import Resource, reqparse
from Models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):
        data = UserRegister.parser.parse_args()
        connection = sqlite3.connect('Database.db')
        cursor = connection.cursor()

        if UserModel.findByUsername(data['username']) is not None:
            return {"message": "user {} already exists".format(data['username'])}, 400
        user = UserModel(**data)
        user.save_to_db()
        #
        # insert_query = "INSERT INTO users VALUES (NULL, ?, ?)"
        #
        # cursor.execute(insert_query, (data['username'], data['password']))
        #
        # connection.commit()
        # connection.close()

        return {"message": "UserCreated "}, 201  # created
