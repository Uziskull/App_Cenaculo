from models.Vote import Vote

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
# Variáveis
# ----------------------------------------- #

VOTOS = ["SIM", "NAO", "ABSTER"]



# ----------------------------------------- #
# WebApp
# ----------------------------------------- #

def start_service():
    # TODO: iniciar listas de propostas, etc etc
    pass

def vote_with_token(token, vote, poll: Vote):
    # TODO: o utilizador com este token vota com este voto nesta proposta, se existir
    pass

def already_voted(token, poll: Vote):
    # TODO: procurar em proposta ativa se utilizador com este token já votou
    pass

def get_current_poll():
    # TODO: ir buscar a proposta definida pela variável `current_poll_id` à lista de propostas
    pass

def get_all_polls():
    # TODO: devolver a lista de propostas
    pass

# ----------------------------------------- #
# GUI
# ----------------------------------------- #

def create_vote(description):
    # TODO: criar proposta e adicionar à lista, no final
    pass

def order_vote_list(vote_index, direction):
    # TODO: se não houver votação em progresso, movimentar proposta na lista conforme a `direction` (-1 para subir, 1 para descer), caso já não esteja no início/fim
    pass

def edit_vote(vote_index, new_description):
    # TODO: alterar descrição de proposta selecionada
    pass
