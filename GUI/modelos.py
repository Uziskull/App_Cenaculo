ESTADOS_PROPOSTA = ["Aprovada", "Reprovada", "2ª Volta"]
ESTADOS_PROPOSTA_CORES = ["#00ff00", "#ff0000", "#aaaaaa"]

class Proposta:
    id = None
    description = None
    order = None
    votos = None
    status = None

    def __init__(self, id, description, order, votos, status):
        self.id = id
        self.description = description
        self.order = order
        self.votos = votos
        self.status = status

class Utilizador:
    token = None
    email = None

    def __init__(self, token, email):
        self.token = token
        self.email = email
