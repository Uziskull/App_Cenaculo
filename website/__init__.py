from flask import Flask

def start_server():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'mama que é de uva'

    from .views import views
    from .auth import auth
    from .api import api

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(api, url_prefix='/api')

    return app