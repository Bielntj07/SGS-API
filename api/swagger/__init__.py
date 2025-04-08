from flask_restx import Api

api = Api(
    version="1.0",
    title = "SGS - Documentação da API do Sistema de Gerenciamento de Salas",
    description = "Esta documentação detalha os endpoints da API do SGS, permitindo o gerenciamento de Alunos, Professores, Turmas, Salas e Administradores.",
    doc="/docs",
    mask_swagger=False,  
    prefix="/api"
)
