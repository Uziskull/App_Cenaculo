

# ----------------------------------------- #
# Erros
# ----------------------------------------- #

class VoteError(Exception):
    pass

class DuplicateVoteError(VoteError):
    def __init__(self):
        super().__init__("Já votaste nesta proposta!")

class VotingClosedError(VoteError):
    def __init__(self):
        super().__init__("A votação para esta proposta já acabou!")

class NonexistantVotingError(VoteError):
    def __init__(self):
        super().__init__("Esta votação não existe!")

class BadVoteError(VoteError):
    def __init__(self, voto):
        super().__init__("Tipo de voto inválido: {}".format(voto))

# ----------------------------------------- #

VOTOS = ["SIM", "NAO", "ABSTER"]

# ----------------------------------------- #

def start_service():
    # TODO: iniciar listas de propostas, etc etc
    pass

def voteWithToken(token, vote, poll_id):
    # TODO: o utilizador com este token vota com este voto nesta proposta, se existir
    pass

def alreadyVoted(token, poll_id):
    # TODO: procurar em proposta ativa se utilizador com este token já votou
    pass

def get_current_poll():
    # TODO: ir buscar a proposta definida pela variável `current_poll_id` à lista de propostas
    pass

def get_all_polls():
    # TODO: devolver a lista de propostas
    pass