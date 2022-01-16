from website import start_server
from controllers.UserController import start_service as start_user_service
from controllers.VoteController import start_service as start_proposta_service
import threading


app = start_server()
start_user_service()
start_proposta_service()

def main():
    # criar thread para lidar com servidor
    t_server = threading.Thread(name="Servidor Cenáculo", target = (lambda: app.run(debug=True, use_reloader=False)))
    t_server.setDaemon(True) # se o GUI desligar, o server também é interrompido
    t_server.start()

    # TODO: começar gui
    # gui.start()

if __name__ == '__main__':
    main()