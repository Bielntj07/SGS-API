from flask_restx import Namespace, Resource, fields
from turmas.turmas_model import listar_turmas, adicionar_turma, turma_por_id, atualizar_turma, excluir_turma

turmas_ns = Namespace("turmas", description="Operações relacionadas às turmas")

turma_model = turmas_ns.model("Turma", {
    "nome": fields.String(required=True, description="Nome da turma"),
})

turma_output_model = turmas_ns.model("TurmaOutput", {
    "id": fields.Integer(description="ID da turma"),
    "nome": fields.String(description="Nome da turma"),
})

@turmas_ns.route("/")
class TurmasResource(Resource):
    @turmas_ns.marshal_list_with(turma_output_model)
    def get(self):
        """Lista todas as turmas"""
        return listar_turmas()

    @turmas_ns.expect(turma_model)
    @turmas_ns.response(201, "Turma criada com sucesso!")
    def post(self):
        """Cria uma nova turma"""
        data = turmas_ns.payload
        return adicionar_turma(data)

@turmas_ns.route("/<int:turma_id>")
class TurmaIdResource(Resource):
    @turmas_ns.marshal_with(turma_output_model)
    @turmas_ns.response(404, "Turma não encontrada")
    def get(self, turma_id):
        """Obtém uma turma pelo ID"""
        return turma_por_id(turma_id)

    @turmas_ns.expect(turma_model)
    @turmas_ns.response(200, "Turma atualizada com sucesso!")
    @turmas_ns.response(404, "Turma não encontrada")
    def put(self, turma_id):
        """Atualiza uma turma pelo ID"""
        data = turmas_ns.payload
        atualizar_turma(turma_id, data)
        return {"message": "Turma atualizada com sucesso!"}, 200

    @turmas_ns.response(200, "Turma excluída com sucesso!")
    @turmas_ns.response(404, "Turma não encontrada")
    def delete(self, turma_id):
        """Exclui uma turma pelo ID"""
        excluir_turma(turma_id)
        return {"message": "Turma excluída com sucesso!"}, 200
