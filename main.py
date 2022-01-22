from website import start_server

app = start_server()
app.app_context().push()

# finalizar a ligação da db, e criar tabelas todas
import models
models.db.create_all()
models.db.session.commit()

# start_user_service()
# start_proposta_service()

if __name__ == '__main__':
    app.run(debug=True)
