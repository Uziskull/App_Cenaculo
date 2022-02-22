from website import start_server
from flask import render_template

app = start_server()

#######################################
# apanhar erros
#######################################

@app.errorhandler(404)
def not_found(error):
    return render_template('erro.html'), 404

@app.errorhandler(500)
def not_found(error):
    return render_template('erro.html'), 500

#######################################
# base de dados
#######################################

app.app_context().push()

# finalizar a ligação da db, e criar tabelas todas
import models
models.db.create_all()
models.db.session.commit()


if __name__ == '__main__':
    app.run(debug=True, port=7777)
