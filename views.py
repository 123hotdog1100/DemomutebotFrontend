from flask import Blueprint, render_template, request
from model import ServerModel, db
from flask_restful import reqparse
import TwitchAPI as T

views = Blueprint('views', __name__)
update_args = reqparse.RequestParser()
update_args.add_argument("prefix", type=str, help="Prefix of bot")
update_args.add_argument("twitch", type=str, help="Twitch username")

Tauth = T.getOauth()


@views.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == "POST":
        ID = request.form.get("id")
        result = ServerModel.query.filter_by(id=ID).first()
        prefix = request.form.get("prefix")
        twitch = request.form.get("twitch")
        if len(twitch) > 0:
            result.twitch = twitch
        if len(prefix) > 0:
            result.prefix = prefix

        db.session.commit()

    return render_template("Settings.html")


@views.route('/', methods=['GET', 'POST'])
def home():
    check = T.checkUser("demomute", Tauth)

    if check:
        output = "Yes"
    elif not check:
        output = "No"
    return render_template("Home.html", check=output)
