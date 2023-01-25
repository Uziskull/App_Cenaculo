import os, sys
from flask import Flask
from models import db
from controllers.VoteController import VOTOS, ESTADOS

def start_server():
    app = Flask(__name__)

    # inserir opções de voto e estados de proposta como variáveis globais
    app.jinja_env.globals["OPCOES_VOTO"] = VOTOS
    app.jinja_env.globals["ESTADOS_PROPOSTA"] = ESTADOS

    try:
        #db_url = "postgresql:" + ":".join(os.environ['DATABASE_URL'].split(":")[1:])
        db_url = os.environ['DATABASE_URL'] + "&sslrootcert=cockroachlabs-cluster.crt"
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    except KeyError:
        try:
            db_url_prefix = 'DATABASE_URL='
            db_url = [arg[len(db_url_prefix):] for arg in sys.argv if arg.startswith(db_url_prefix)][0]
            db_url = "postgresql:" + ":".join(db_url.split(":")[1:])
            app.config['SQLALCHEMY_DATABASE_URI'] = db_url
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