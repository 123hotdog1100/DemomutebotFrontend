from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from views import views
from auth import auth

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = "sjabndfkmdn"
app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')

db = SQLAlchemy(app)


class ServerModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    twitch = db.Column(db.String(100))
    prefix = db.Column(db.String(2), nullable=False)

    def __repr__(self):
        return f"ID(id={id})"


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
            result.name = args["prefix"]
        if args["twitch"]:
            result.name = args["twitch"]

        db.session.commit()
        return result


api.add_resource(Backend, "/api/<int:ID>")

if __name__ == '__main__':
    app.run(debug=True)
