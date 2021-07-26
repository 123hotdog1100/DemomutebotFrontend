from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
class ServerModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    twitch = db.Column(db.String(100))
    prefix = db.Column(db.String(2), nullable=False)

    def __repr__(self):
        return f"ID(id={id})"
