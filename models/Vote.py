from uuid import uuid4

class Vote():
    def __init__(self, description):
        self.id = str(uuid4())
        self.description = description
