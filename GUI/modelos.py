class Proposta:
    id = None
    description = None
    order = None
    votos = None

    def __init__(self, id, description, order, votos):
        self.id = id
        self.description = description
        self.order = order
        self.votos = votos

class Utilizador:
    token = None
    email = None

    def __init__(self, token, email):
        self.token = token
        self.email = email
