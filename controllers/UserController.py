from typing import Sequence
from models import User, db

# ----------------------------------------- #
# WebApp
# ----------------------------------------- #

# def start_service():
#     # TODO: iniciar listas de utilizadores, etc etc
#     pass

def is_token_valid(token: str):
    u = User.query.get(token)
    return u is not None

def get_token_for(email: str):
    u = User.query.filter_by(email=email).first()
    if u is None:
        return None
    return u.token

# ----------------------------------------- #
# GUI
# ----------------------------------------- #

def insert_multiple_users(user_emails: Sequence[str]):
    for email in user_emails:
        db.session.add(User(email))
    db.session.commit()
