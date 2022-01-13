from website import startServer
from controllers.UserController import startUserService
from controllers.VoteController import startPropostaService
import threading


app = startServer()
startUserService()
startPropostaService()

def main():
    # criar thread para lidar com servidor
    t_server = threading.Thread(name="Servidor Cenáculo", target = (lambda: app.run(debug=True, use_reloader=False)))
    t_server.setDaemon(True) # se o GUI desligar, o server também é interrompido
    t_server.start()

    # TODO: começar gui
    # gui.start()

if __name__ == '__main__':
    main()