from website import start_server
from flask import render_template
import sys

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

DEBUG_FLAG_OFF = "debug=false"
if __name__ == '__main__':
    debug = True
    for arg in sys.argv:
        if arg.lower() == DEBUG_FLAG_OFF:
            debug = False
            break
    
    if debug:
        app.run(host="0.0.0.0", port=7777, debug=True, use_reloader=True)
    else:
        app.run(debug=False, use_reloader=False)
