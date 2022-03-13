from typing import List, Sequence
from models import User, db

# ----------------------------------------- #
# Erros
# ----------------------------------------- #

class UserError(Exception):
    pass

class UserNotFoundError(UserError):
    def __init__(self):
        super().__init__("Esse utilizador não existe!")

class UserAlreadyLoggedIn(UserError):
    def __init__(self):
        super().__init__("Alguém já entrou com este email. Se fores o dono deste email, avisa-nos!")

# ----------------------------------------- #
# WebApp
# ----------------------------------------- #

def get_token_for(email: str):
    u = User.query.filter_by(email=email).first()
    if u is None:
        return None
    return u.token

def is_login_valid(token: str, otp: str):
    u = User.query.get(token)
    if u is None:
        return False
    return u.otp == otp

def store_login(token: str, otp: str):
    u = User.query.get(token)
    if u is None:
        raise UserNotFoundError()
    if u.otp is not None:
        raise UserAlreadyLoggedIn()
    u.otp = otp
    db.session.merge(u)
    db.session.commit()

def log_out(token: str, otp: str):
    u = User.query.filter_by(token=token, otp=otp).first()
    if u is None:
        raise UserNotFoundError()
    u.otp = None
    db.session.merge(u)
    db.session.commit()

# ----------------------------------------- #
# GUI
# ----------------------------------------- #

def insert_multiple_users(user_emails: Sequence[str]) -> List[User]:
    new_users = [User(email) for email in user_emails]
    db.session.add_all(new_users)
    db.session.commit()
    return new_users

def get_all_users() -> List[User]:
    return User.query.all()

def delete_user(user_token: str) -> None:
    user = User.query.get(user_token)
    if user is None:
        raise UserNotFoundError()
    
    db.session.delete(user)
    db.session.commit()
