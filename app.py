import flask
from flask import Flask, Response
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from model import ServerModel, db
from views import views
from auth import auth
import TwitchAPI as T
from multiprocessing import Process, Value

Tauth = T.getOauth()

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = "sjabndfkmdn"

db.init_app(app)
db.create_all(app=app)
put_args = reqparse.RequestParser()
put_args.add_argument("prefix", type=str, help="Prefix of bot", required=True)
put_args.add_argument("twitch", type=str, help="Twitch username")

update_args = reqparse.RequestParser()
update_args.add_argument("prefix", type=str, help="Prefix of bot")
update_args.add_argument("twitch", type=str, help="Twitch username")

resource_fields = {
    'id': fields.Integer,
    'twitch': fields.String,
    'prefix': fields.String
}

sync_args = reqparse.RequestParser()
sync_args.add_argument("Command", type=str, help="The command you wish to run", required=True)
sync_args.add_argument("ID", type=str, help="Server ID", required=True)
sync_args.add_argument("Username", type=str, help="Username")

sync_put_args = reqparse.RequestParser()
sync_put_args.add_argument("ID", type=str, help="Server ID", required=True)

checked = []


class Backend(Resource):
    @marshal_with(resource_fields)
    def get(self, ID):
        result = ServerModel.query.filter_by(id=ID).first()
        if not result:
            abort(404, message="Could not find Server id")
        return result

    def post(self):
        return {"data": "posted"}

    @marshal_with(resource_fields)
    def put(self, ID):
        args = put_args.parse_args()
        result = ServerModel.query.filter_by(id=ID).first()
        if result:
            abort(409, message="Server ID taken")
        server = ServerModel(id=ID, prefix=args['prefix'], twitch=args['twitch'])
        db.session.add(server)
        db.session.commit()
        return server, 201

    @marshal_with(resource_fields)
    def patch(self, ID):
        args = update_args.parse_args()
        result = ServerModel.query.filter_by(id=ID).first()
        if not result:
            abort(404, message="Server not found")

        if args["prefix"]:
            result.prefix = args["prefix"]
        if args["twitch"]:
            result.twitch = args["twitch"]

        db.session.commit()
        return result


class sync(Resource):
    def get(self, ID):
        check = "No"
        args = sync_args.parse_args()
        username = args['Username']
        if args['Command'] == 'checkuser':  ##Checks to see if someone is live
            check = T.checkUser(username, Tauth)
        if args['Command'] == 'getstream':  ##Returns the stream title
            check = T.getstream(username, Tauth)
        if args['Command'] == 'getchecked':  ##returns success if the id is in the checked list
            if ID in checked:
                return 201
            else:
                return 200

        return check, 200

    def put(self, ID):
        # args = sync_put_args.parse_args()
        # args[ID] = args
        checked.append(ID)
        print(checked)
        return True, 201

    def patch(self, ID):
        if ID in checked:
            checked.remove(ID)
            return 200
        else:
            abort(404, message="ID not checked")


api.add_resource(Backend, "/api/<int:ID>")
api.add_resource(sync, "/sync/<int:ID>")
app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=80)
