from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

put_args = reqparse.RequestParser()
put_args.add_argument("prefix", type=str, help="Prefix of bot")

ids = {}


def abort_if_not(ID):
    if ID not in ids:
        abort("ID is not valid")


class Backend(Resource):
    def get(self, ID):
        abort_if_not(ID)
        return ids[ID]

    def post(self):
        return {"data": "posted"}

    def put(self, ID):
        args = put_args.parse_args()
        ids[ID] = args
        return ids[ID], 201


api.add_resource(Backend, "/helloworld/<int:ID>")

if __name__ == '__main__':
    app.run(debug=True)
