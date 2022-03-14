from flask import Blueprint, Response, request, session, flash, render_template, redirect, url_for
from controllers.VoteController import get_current_poll, get_all_polls_and_results, vote_with_token, already_voted, PollError, VOTOS
from .auth import check_login
from sqlalchemy.exc import OperationalError

views = Blueprint('views', __name__)

# ----------------------------------------- #
# Views
# ----------------------------------------- #

@views.route('/', methods=["GET"])
def home():
    # redirecionar para página de voto, a verificação do token é feita lá
    return redirect(url_for("views.votar"))

@views.route('/votar',methods=["GET", "POST"])
def votar():
    current_poll = None
    user_voted = False
    try:
        # se token estiver inválido, redirecionar para login
        token = None
        try:
            token = session["token"]
            if not check_login(token):
                return redirect(url_for("auth.login"))
        except KeyError:
            return redirect(url_for("auth.login"))
        
        # PRG: obter resultado de post, se existir

        # obter a proposta atual
        current_poll = get_current_poll()
        if current_poll is not None:
            user_voted = already_voted(token, current_poll.id)
        
        if request.method == "POST":
            error = None

            vote = None
            for vote_name in VOTOS:
                if vote_name in request.form:
                    vote = vote_name
                    break
            
            poll_id = request.form["proposta"]
            # se não houver voto, avisar com erro
            if not vote:
                error = "Voto é obrigatório!"
            # elif already_voted(token, poll_id):
            #     error = "Já votaste nesta proposta!"
            else:
                try:
                    vote_with_token(token, vote, poll_id)
                    flash("Votaste com sucesso!", 'success')
                except PollError as e:
                    # voteWithToken devolve erros dependendo de varias coisas, meter em mensagem de erro
                    error = str(e)

            if error:
                flash(error, 'danger')
            
            return redirect(url_for("views.votar"))
        
    except OperationalError:
        # base de dados deu o prego
        flash("Ocorreu um erro ao ligar à base de dados. Não devia acontecer, oops!", 'danger')
    
    return render_template("views/votar.html", poll=current_poll, already_voted=user_voted)

@views.route('/historico',methods=["GET"])
def historico():
    all_poll_results = None
    try:
        # se token estiver inválido, redirecionar para login
        try:
            token = session["token"]
            if not check_login(token):
                return redirect(url_for("auth.login"))
        except KeyError:
            return redirect(url_for("auth.login"))

        # obter todas as propostas
        all_poll_results = get_all_polls_and_results()
        
    except OperationalError:
        # base de dados deu o prego
        flash("Ocorreu um erro ao ligar à base de dados. Não devia acontecer, oops!", 'danger')

    return render_template("views/historico.html", poll_results=all_poll_results)
