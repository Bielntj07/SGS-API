from swagger.swagger_config import configure_swagger
from config import app,db
from admin.admin_routes import administradores_blueprint
from salas.salas_routes import salas_blueprint
from salas.reservas_routes import reservas_blueprint
from alunos.alunos_routes import alunos_blueprint
from turmas.turmas_routes import turmas_blueprint
from professor.professor_routes import professores_blueprint

app.register_blueprint(alunos_blueprint, url_prefix='/api')
app.register_blueprint(turmas_blueprint, url_prefix='/api')
app.register_blueprint(professores_blueprint, url_prefix='/api')
app.register_blueprint(administradores_blueprint, url_prefix='/api')
app.register_blueprint(salas_blueprint, url_prefix='/api')
app.register_blueprint(reservas_blueprint, url_prefix='/api')

configure_swagger(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
  app.run(host=app.config["HOST"], port = app.config['PORT'],debug=app.config['DEBUG'] )