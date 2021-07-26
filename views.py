from flask import Blueprint, render_template, request
from model import ServerModel, db
from flask_restful import reqparse
import TwitchAPI as T
import requests

views = Blueprint('views', __name__)
update_args = reqparse.RequestParser()
update_args.add_argument("prefix", type=str, help="Prefix of bot")
update_args.add_argument("twitch", type=str, help="Twitch username")

username = "demomute"
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

BASE = "http://127.0.0.1:5000/"

def checking(ID):
    r = requests.get(BASE + "sync/1", {'Command': 'getchecked', 'ID': ID})
    if r.json() == 201:
        return True

@views.route('/', methods=['GET', 'POST'])
def home():
    check = T.checkUser(username, Tauth)
    output2 = checking(1)

    if check:
        output = "Yes"
    elif not check:
        output = "No"
    return render_template("Home.html", check=output, check2=output2)
