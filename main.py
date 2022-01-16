from website import start_server
from controllers.UserController import start_service as start_user_service
from controllers.VoteController import start_service as start_proposta_service
#import threading

app = start_server()
start_user_service()
start_proposta_service()

if __name__ == '__main__':
    app.run(debug=True)