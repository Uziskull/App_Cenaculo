from flask import Blueprint, request, session

api = Blueprint('api', __name__)

@api.route('votos', methods=["POST"])
def api_ver_votos():
    # TODO: listar votos para proposta atual, ou passar um voto especifico pelo path
    pass