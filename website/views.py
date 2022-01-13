from flask import Blueprint, Response, request, session, flash, render_template, redirect, url_for
from .auth import checkLogin
from controllers.VoteController import voteWithToken, alreadyVoted

views = Blueprint('views', __name__)

# ----------------------------------------- #

VOTOS = ["SIM", "NAO", "ABSTER"]

# ----------------------------------------- #
# Views
# ----------------------------------------- #

@views.route('/', methods=["GET"])
def home():
    # se token estiver inválido, redirecionar para login
    if not checkLogin(session["token"]):
        return redirect(url_for("votar.html"))
    return redirect(url_for(views.votar))

@views.route('/votar',methods=["GET", "POST"])
def votar():
    # se token estiver inválido, redirecionar para login
    token = session["token"]
    if not checkLogin(token):
        return redirect(url_for("votar.html"))

    if request.method == "POST":
        error = None

        voto = request.form["voto"]
        # se não houver voto, avisar com erro
        if not voto:
            error = "Voto é obrigatório!"
        elif alreadyVoted(token):
            error = "Já votaste nesta proposta!"
        else:
            try:
                voteWithToken(token, voto)
                return Response(status = 200)
            except:
                # TODO: voteWithToken devia devolver erros dependendo de varias coisas, tratar deles aqui e meter em mensagem de erro
                pass

        flash(error)
    
    return render_template("votar.html")