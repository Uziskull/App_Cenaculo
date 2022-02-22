from typing import Sequence
from models import User, db

# ----------------------------------------- #
# Erros
# ----------------------------------------- #

class UserError(Exception):
    pass

class UserNotFoundError(UserError):
    def __init__(self):
        super().__init__("Esse utilizador não existe!")

# ----------------------------------------- #
# WebApp
# ----------------------------------------- #

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

def insert_multiple_users(user_emails: Sequence[str]) -> None:
    new_users = [User(email) for email in user_emails]
    db.session.add_all(new_users)
    db.session.commit()
    return new_users

def get_all_users() -> None:
    return User.query.all()

def delete_user(user_token: str) -> None:
    user = User.query.get(user_token)
    if user is None:
        raise UserNotFoundError()
    
    db.session.delete(user)
    db.session.commit()
