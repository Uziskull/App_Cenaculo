import os, sys
from flask import Flask
from models import db
from controllers.VoteController import VOTOS

def start_server():
    app = Flask(__name__)

    # inserir opções de voto como variável global
    app.jinja_env.globals["OPCOES_VOTO"] = VOTOS

    try:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    except KeyError:
        try:
            db_url_prefix = 'DATABASE_URL='
            app.config['SQLALCHEMY_DATABASE_URI'] = [arg[len(db_url_prefix):] for arg in sys.argv if arg.startswith(db_url_prefix)][0]
        except IndexError:
            #print("Defina 'DATABASE_URL' nas variáveis de ambiente (ou nos argumentos de execução) com o URI do PostgreSQL!")
            #sys.exit(1)
            print("A correr com base de dados em memória")
            app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'mama que eh de uva'

    db.init_app(app)

    from .views import views
    from .auth import auth
    from .api import api

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(api, url_prefix='/api')

    return app