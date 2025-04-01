from flask_restx import Api

api = Api(
    version="1.0",
    title="Documentação do SGS - Sistema de Gerenciamento de Salas",
    description="Documentação da API para Alunos, Professores, Turmas, Salas e Administradores",
    doc="/docs",
    mask_swagger=False,  
    prefix="/api"
)
