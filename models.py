from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy.inspection import inspect

db = SQLAlchemy()

#############################################
## Classes
#############################################

class User(db.Model):
    token = db.Column(db.String(), primary_key=True)
    email = db.Column(db.String(), unique=True, nullable=False)

    ##poll = db.relationship("Poll", secondary="uservote")

    def __init__(self, email):
        self.email = email
        self.token = str(uuid4())

    def __repr__(self) -> str:
        return f"{self.token}:{self.email}"

class Poll(db.Model):
    id = db.Column(db.String(), primary_key=True)
    description = db.Column(db.String(), unique=True, nullable=False)
    order = db.Column(db.Integer, unique=True, nullable=False)

    ##user = db.relationship("User", secondary="uservote")

    # # criar referencia inversa na tabela User chamada "polls"
    # users = db.relationship(User, secondary='Vote', backref="polls")

    def __init__(self, order, description):
        self.id = str(uuid4())
        self.order = order
        self.description = description

    def __repr__(self) -> str:
        return f"{self.id}:{self.description}"

class Vote(db.Model):
    user_token = db.Column(db.String(), db.ForeignKey('user.token'), primary_key=True)
    poll_id = db.Column(db.String(), db.ForeignKey('poll.id'), primary_key=True)
    vote_option = db.Column(db.Integer, db.CheckConstraint('vote_option >= 0 AND vote_option <= 2'),
        autoincrement=False, nullable=False)

    user = db.relationship(User, backref=db.backref('votes'))
    poll = db.relationship(Poll, backref=db.backref('votes'))

    def __init__(self, user_token, poll_id, vote_option):
        self.user_token = user_token
        self.poll_id = poll_id
        self.vote_option = vote_option

    def __repr__(self) -> str:
        return f"{self.user_token}@{self.poll_id}:{self.vote_option}"

# para marcar o voto ativo
class ActivePoll(db.Model):
    # isto garante que active só pode ser True, e que é único --> só um valor na tabela
    __table_args__ = tuple(
        db.CheckConstraint('active')
    )

    active = db.Column(db.Boolean, primary_key=True, default=True)
    poll_id = db.Column(db.String(), db.ForeignKey('poll.id'), nullable=False)

    def __init__(self, poll_id):
        self.poll_id = poll_id
        self.active = True

    def __repr__(self) -> str:
        return f"Active vote: {self.poll_id}"

#############################################

def as_dict(obj):
    if isinstance(obj, list):
        #print("list: " + str(obj))
        return [as_dict(e) for e in obj]
    elif isinstance(obj, sqlalchemy.engine.row.Row):
        #print("row: " + str(obj))
        dict_obj = obj._asdict()
        return {e: as_dict(dict_obj[e]) for e in dict_obj}
    elif isinstance(obj, db.Model):
        #print("model: " + str(obj))
        try:
            obj = dict(obj)
            obj.pop('_sa_instance_state')
            return obj
        except:
            return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
    else:
        #print("other: " + str(obj))
        return obj