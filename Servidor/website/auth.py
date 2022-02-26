from uuid import uuid4
from flask import Blueprint, session, flash, request, redirect, url_for, render_template
from controllers.UserController import get_token_for, store_login, is_login_valid
from sqlalchemy.exc import OperationalError

auth = Blueprint('auth', __name__)

def check_login(token):
    #return False if not token else is_token_valid(token)
    try:
        token, otp = token.split(":")
        return is_login_valid(token, otp)
    except Exception:
        return False

# ----------------------------------------- #

# TODO: isto está péssimo, convém usar hash-salt para prevenir rainbow tables

@auth.route('/login', methods=["GET", "POST"])
def login():
    try:
        # se token estiver válido, redirecionar logo, não vale a pena fazer login
        try:
            if check_login(session["token"]):
                return redirect(url_for("views.votar"))
        except KeyError:
            pass

        if request.method == "POST":
            error = None

            email = request.form["email"]
            # se não houver email, avisar com erro
            if not email:
                error = "Email é obrigatório!"
            else:
                # buscar token de login ao controlador, caso o email seja válido
                token = get_token_for(email)
                if not token:
                    # user não existe
                    error = "Email inválido!"
                else:
                    try:
                        # fazer login
                        random_otp = str(uuid4())
                        store_login(token, random_otp)
                        session.clear()
                        session["token"] = f"{token}:{random_otp}"
                        return redirect(url_for("views.votar"))
                    except:
                        error = "Não foi possível fazer login. Por favor tente novamente!"
                        session.clear()

            flash(error, 'error')
        
    except OperationalError:
        # base de dados deu o prego
        flash("Ocorreu um erro ao ligar à base de dados. Não devia acontecer, oops!", 'error')

    return render_template("auth/login.html")