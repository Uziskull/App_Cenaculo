from flask import Blueprint, session, flash, request, redirect, url_for, render_template
from controllers.UserController import isTokenValid, getTokenFor

auth = Blueprint('auth', __name__)

# ----------------------------------------- #

def checkLogin(token):
    return False if not token else isTokenValid(token)

# ----------------------------------------- #

@auth.route('/login', methods=["GET", "POST"])
def login():
    # se token estiver válido, redirecionar logo, não vale a pena fazer login
    if checkLogin(session["token"]):
        return redirect(url_for("views/votar.html"))

    if request.method == "POST":
        error = None

        email = request.form["email"]
        # se não houver email, avisar com erro
        if not email:
            error = "Email é obrigatório!"
        else:
            # buscar token de login ao controlador, caso o email seja válido
            token = getTokenFor(email)
            if not token:
                # user não existe
                error = "Email inválido!"
            else:
                # fazer login
                session.clear()
                session["token"] = token
                return redirect(url_for("views/votar.html"))

        flash(error)

    return render_template("auth/login.html")