from flask import Blueprint, Response, request, session, flash, render_template, redirect, url_for
from controllers.VoteController import get_current_poll, get_all_polls, vote_with_token, already_voted, PollError
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
    try:
        token = session["token"]
        if not check_login(token):
            return redirect(url_for("auth.login"))
    except KeyError:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        error = None

        vote = request.form["voto"]
        poll_id = request.form["proposta"]
        # se não houver voto, avisar com erro
        if not vote:
            error = "Voto é obrigatório!"
        # elif already_voted(token, poll_id):
        #     error = "Já votaste nesta proposta!"
        else:
            try:
                vote_with_token(token, vote, poll_id)
                flash("Votaste com sucesso!", 'message')
            except PollError as e:
                # voteWithToken devolve erros dependendo de varias coisas, meter em mensagem de erro
                error = str(e)

        if error:
            flash(error, 'error')
    
    # obter a proposta atual
    current_poll = get_current_poll()
    return render_template("views/votar.html", poll=current_poll)

@views.route('/historico',methods=["GET"])
def historico():
    # se token estiver inválido, redirecionar para login
    try:
        token = session["token"]
        if not check_login(token):
            return redirect(url_for("auth.login"))
    except KeyError:
        return redirect(url_for("auth.login"))

    # obter todas as propostas
    all_polls = get_all_polls()

    return render_template("views/historico.html", polls=all_polls)