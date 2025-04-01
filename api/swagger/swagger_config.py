from . import api
from swagger.namespaces.alunos_namespace import alunos_ns
from swagger.namespaces.professor_namespace import professores_ns
from swagger.namespaces.turmas_namespace import turmas_ns
from swagger.namespaces.salas_namespace import salas_ns
from swagger.namespaces.admin_namespace import admin_ns

def configure_swagger(app):
    api.init_app(app)
    api.add_namespace(alunos_ns, path="/alunos")
    api.add_namespace(professores_ns, path="/professores")
    api.add_namespace(turmas_ns, path="/turmas")
    api.add_namespace(salas_ns, path="/salas")
    api.add_namespace(admin_ns, path="/administradores")
    api.mask_swagger = False
