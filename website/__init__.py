import os, sys
from flask import Flask
from models import db

def start_server():
    app = Flask(__name__)

    try:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    except KeyError:
        try:
            app.config['SQLALCHEMY_DATABASE_URI'] = [arg for arg in sys.argv if arg.startswith('DATABASE_URL')][0]
        except IndexError:
            print("Defina 'DATABASE_URL' nas variáveis de ambiente (ou nos argumentos de execução) com o URI do PostgreSQL!")
            sys.exit(1)
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'mama que é de uva'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .api import api

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(api, url_prefix='/api')

    return app