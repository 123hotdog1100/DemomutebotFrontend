from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

put_args = reqparse.RequestParser()
put_args.add_argument("prefix", type=str, help="Prefix of bot", required=True)
put_args.add_argument("twitch", type=str, help="Twtich username")

ids = {}


def abort_if_not(ID):
    if ID not in ids:
        abort("ID is not valid")


def abort_if_exists(ID):
    if ID in ids:
        abort(409, message="ID already exists")

class Backend(Resource):
    def get(self, ID):
        abort_if_not(ID)
        return ids[ID]

    def post(self):
        return {"data": "posted"}

    def put(self, ID):
        abort_if_exists(ID)
        args = put_args.parse_args()
        ids[ID] = args
        return ids[ID], 201

    def delete(self, ID):
        abort_if_not(ID)
        del ids[ID]
        return '', 204


api.add_resource(Backend, "/helloworld/<int:ID>")

if __name__ == '__main__':
    app.run(debug=True)
