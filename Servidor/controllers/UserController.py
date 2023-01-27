from typing import List, Sequence
from models import User
from sqlalchemy.orm import Session

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

def get_token_for(s: Session, email: str):
    u = s.query(User).filter_by(email=email).first()
    if u is None:
        return None
    return u.token

def is_login_valid(s: Session, token: str, otp: str):
    u = s.query(User).get(token)
    if u is None:
        return False
    return u.otp == otp

def store_login(s: Session, token: str, otp: str):
    u = s.query(User).get(token)
    if u is None:
        raise UserNotFoundError()
    if u.otp is not None:
        raise UserAlreadyLoggedIn()
    u.otp = otp
    s.merge(u)

def log_out(s: Session, token: str, otp: str):
    u = s.query(User).filter_by(token=token, otp=otp).first()
    if u is None:
        raise UserNotFoundError()
    u.otp = None
    s.merge(u)

# ----------------------------------------- #
# GUI
# ----------------------------------------- #

def insert_multiple_users(s: Session, user_emails: Sequence[str]) -> List[User]:
    new_users = [User(email) for email in user_emails]
    s.add_all(new_users)
    return new_users

def get_all_users(s: Session) -> List[User]:
    return s.query(User).all()

def delete_user(s: Session, user_token: str) -> None:
    user = s.query(User).get(user_token)
    if user is None:
        raise UserNotFoundError()
    
    s.delete(user)

def clean_all_user_cache(s: Session) -> None:
    users = get_all_users(s)
    for u in users:
        u.otp = None
        s.merge(u)
