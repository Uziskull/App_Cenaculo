from flask import Blueprint, request, current_app, jsonify
import sqlalchemy
from controllers import VoteController, UserController
from models import as_dict
from psycopg2.errors import UniqueViolation

api = Blueprint('api', __name__)

@api.route('/propostas', methods=["GET"])
def api_ver_propostas():
    result = VoteController.get_all_polls()
    return jsonify(as_dict(result)), 200

@api.route('/propostas/votos', methods=["GET"])
def api_ver_votos():
    result = VoteController.get_all_polls_and_results()
    return jsonify(as_dict(result)), 200
    # return [
    #     {
    #         "id": result[i].poll.id,
    #         "description": result[i].poll.description,
    #         "order": i+1,
    #         ##"votos": {
    #         "sim": result[i].sim,
    #         "nao": result[i].nao,
    #         "abster": result[i].abster
    #         ##}
    #     }
    #     for i in range(len(result))], 200

@api.route('/propostas/ativa', methods=["GET"])
def api_ver_proposta_ativa():
    poll = VoteController.get_current_poll()
    if poll is None:
        return "", 204
    return jsonify(as_dict(poll)), 200

@api.route('/propostas', methods=["POST"])
def api_criar_proposta():
    try:
        body = request.get_json()
        count = VoteController.count_polls()
        new_poll = VoteController.create_poll(count + 1, body["description"])
        return jsonify(as_dict(new_poll)), 201
    except UniqueViolation as e:
        return "Já existe uma proposta com essa descrição!", 404
    except Exception as e:
        return str(e), 404

@api.route('/propostas/<poll_id>/votos', methods=["GET"])
def api_ver_votos_proposta(poll_id):
    try:
        votes = VoteController.get_votes_for(poll_id)
        return jsonify(as_dict(votes)), 200
    except Exception as e:
        return str(e), 404

@api.route('/propostas/<poll_id>', methods=["PATCH"])
def api_alterar_proposta(poll_id):
    try:
        body = request.get_json()
        if "description" in body:
            VoteController.edit_poll(poll_id, body["description"])
        
        if "order" in body:
            VoteController.order_poll(poll_id, body["order"])
        
        return "", 200
    except Exception as e:
        return str(e), 404

@api.route('/propostas/<poll_id>', methods=["DELETE"])
def api_apagar_proposta(poll_id):
    try:
        VoteController.delete_poll(poll_id)
        return "", 204
    except Exception as e:
        return str(e), 404

@api.route('/propostas/<poll_id>/abrir', methods=["POST"])
def api_abrir_votos(poll_id):
    try:
        VoteController.open_poll(poll_id)
        return "", 200
    except Exception as e:
        return str(e), 404

@api.route('/propostas/<poll_id>/fechar', methods=["POST"])
def api_fechar_votos(poll_id):
    try:
        VoteController.close_poll(poll_id)
        return "", 200
    except Exception as e:
        return str(e), 404

# ---------------------------------

@api.route('/utilizadores', methods=["GET"])
def api_ver_utilizadores():
    return jsonify(as_dict(UserController.get_all_users())), 200

@api.route('/utilizadores', methods=["POST"])
def api_adicionar_utilizadores():
    try:
        body = request.get_json()
        if not isinstance(body, list) \
            or not all(isinstance(obj, str) for obj in body):
            return "Não é lista de strings", 400
            
        UserController.insert_multiple_users(body)
        return "", 200
    except Exception as e:
        return str(e), 404

@api.route('/utilizadores/<user_token>', methods=["DELETE"])
def api_apagar_utilizador(user_token):
    try:
        UserController.delete_user(user_token)
        return "", 204
    except Exception as e:
        return str(e), 404

###################################
# validação
###################################

@api.before_request
def check_auth():
    #print(request.headers)
    if 'Informacao-Dramatica' not in request.headers \
        or request.headers['Informacao-Dramatica'] != current_app.config['SECRET_KEY']:
        return "querias", 418
