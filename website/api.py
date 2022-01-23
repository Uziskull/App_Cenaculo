from flask import Blueprint, request, current_app
from controllers import VoteController, UserController

api = Blueprint('api', __name__)

@api.route('/propostas', methods=["GET"])
def api_ver_votos():
    return VoteController.get_all_polls_and_results(), 200

@api.route('/propostas', methods=["POST"])
def api_criar_proposta():
    try:
        body = request.get_json()
        new_poll = VoteController.create_poll(body["description"])
        return new_poll, 201
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

# ---------------------------------

@api.route('/utilizadores', methods=["GET"])
def api_ver_utilizadores():
    return UserController.get_all_users(), 200

@api.route('/utilizadores', methods=["POST"])
def api_adicionar_utilizadores():
    try:
        body = request.get_json()
        if not isinstance(body, list) \
            or not all([isinstance(obj, str) for obj in body]):
            return "Não é lista de strings", 400
            
        UserController.insert_multiple_users(body)
        return "", 200
    except Exception as e:
        return str(e), 404

@api.route('/utilizadores/<user_token>', methods=["DELETE"])
def api_apagar_utilizador(user_token):
    try:
        UserController.remove_user(user_token)
        return "", 204
    except Exception as e:
        return str(e), 404

###################################
# validação
###################################

@api.before_request
def check_auth():
    if 'Informacao-Dramatica' not in request.headers \
        or request.headers['Informacao-Dramatica'] != current_app.config['SECRET_KEY']:
        return "querias", 418