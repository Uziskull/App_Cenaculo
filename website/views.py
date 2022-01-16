from flask import Blueprint, Response, request, session, flash, render_template, redirect, url_for
from controllers.VoteController import get_current_poll, get_all_polls, voteWithToken, alreadyVoted, VoteError
from .auth import check_login

views = Blueprint('views', __name__)

# ----------------------------------------- #
# Views
# ----------------------------------------- #

@views.route('/', methods=["GET"])
def home():
    # if not check_login(session["token"]):
    #     return redirect(url_for("auth.login"))
    # return redirect(url_for("views.votar"))

    # redirecionar para página de voto, a verificação do token é feita lá
    return redirect(url_for("views.votar"))

@views.route('/votar',methods=["GET", "POST"])
def votar():
    # se token estiver inválido, redirecionar para login
    token = session["token"]
    if not check_login(token):
        return redirect(url_for("auth.login"))

    # obter a proposta atual
    current_poll = get_current_poll()

    if request.method == "POST":
        error = None

        vote = request.form["voto"]
        # se não houver voto, avisar com erro
        if not vote:
            error = "Voto é obrigatório!"
        elif alreadyVoted(token, current_poll.id):
            error = "Já votaste nesta proposta!"
        else:
            try:
                voteWithToken(token, vote, current_poll.id)
                flash("Votaste com sucesso!", 'message')
            except VoteError as e:
                # voteWithToken devolve erros dependendo de varias coisas, meter em mensagem de erro
                error = str(e)

        if error:
            flash(error, 'error')
    
    return render_template("votar.html", poll=current_poll)

@views.route('/historico',methods=["GET"])
def historico():
    # se token estiver inválido, redirecionar para login
    token = session["token"]
    if not check_login(token):
        return redirect(url_for("auth.login"))

    # obter todas as propostas
    all_polls = get_all_polls()

    return render_template("historico.html", polls=all_polls)