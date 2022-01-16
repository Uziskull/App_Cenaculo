from uuid import uuid4

class User():
    def __init__(self, email):
        self.email = email
        self.token = str(uuid4())
