from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

put_args = reqparse.RequestParser()
put_args.add_argument("prefix", type=str, help="Prefix of bot")

ids = {}

class Backend(Resource):
    def get(self,ID):
        return ids[ID]

    def post(self):
        return {"data": "posted"}

    def put(self, ID):
        args = put_args.parse_args()
        return {ID: args}




api.add_resource(Backend, "/helloworld/<int:ID>")

if __name__ == '__main__':
    app.run(debug=True)
