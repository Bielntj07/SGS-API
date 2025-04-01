from flask_restx import Namespace, Resource, fields
from alunos.alunos_model import listar_alunos, adicionar_aluno, aluno_por_id, atualizar_aluno, excluir_aluno

alunos_ns = Namespace("alunos", description="Operações relacionadas aos alunos")

aluno_model = alunos_ns.model("Aluno", {
    "nome": fields.String(required=True, description="Nome do aluno"),
    "email": fields.String(required=True, description="Email do aluno"),
    "turma_id": fields.Integer(required=True, description="ID da turma associada"),
})

aluno_output_model = alunos_ns.model("AlunoOutput", {
    "id": fields.Integer(description="ID do aluno"),
    "nome": fields.String(description="Nome do aluno"),
    "email": fields.String(description="Email do aluno"),
    "turma_id": fields.Integer(description="ID da turma associada"),
})

@alunos_ns.route("/")
class AlunosResource(Resource):
    @alunos_ns.marshal_list_with(aluno_output_model)
    def get(self):
        """Lista todos os alunos"""
        return listar_alunos()

    @alunos_ns.expect(aluno_model)
    @alunos_ns.response(201, "Aluno adicionado com sucesso!")
    @alunos_ns.response(404, "Turma não existe")
    def post(self):
        """Cria um novo aluno"""
        data = alunos_ns.payload
        response, status_code = adicionar_aluno(data)
        return response, status_code

@alunos_ns.route("/<int:id_aluno>")
class AlunoIdResource(Resource):
    @alunos_ns.marshal_with(aluno_output_model)
    @alunos_ns.response(404, "Aluno não encontrado")
    def get(self, id_aluno):
        """Obtém um aluno pelo ID"""
        return aluno_por_id(id_aluno)

    @alunos_ns.expect(aluno_model)
    @alunos_ns.response(200, "Aluno atualizado com sucesso!")
    @alunos_ns.response(404, "Aluno não encontrado")
    def put(self, id_aluno):
        """Atualiza um aluno pelo ID"""
        data = alunos_ns.payload
        atualizar_aluno(id_aluno, data)
        return {"message": "Aluno atualizado com sucesso!"}, 200

    @alunos_ns.response(200, "Aluno excluído com sucesso!")
    @alunos_ns.response(404, "Aluno não encontrado")
    def delete(self, id_aluno):
        """Exclui um aluno pelo ID"""
        excluir_aluno(id_aluno)
        return {"message": "Aluno excluído com sucesso!"}, 200
