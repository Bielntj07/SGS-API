from flask_restx import Namespace, Resource, fields
from professor.professor_model import listar_professores, adicionar_professor, professor_por_id, atualizar_professor, excluir_professor

professores_ns = Namespace("professores", description="Operações relacionadas aos professores")

professor_model = professores_ns.model("Professor", {
    "nome": fields.String(required=True, description="Nome do professor"),
    "email": fields.String(required=True, description="Email do professor"),
})

professor_output_model = professores_ns.model("ProfessorOutput", {
    "id": fields.Integer(description="ID do professor"),
    "nome": fields.String(description="Nome do professor"),
    "email": fields.String(description="Email do professor"),
})

@professores_ns.route("/")
class ProfessoresResource(Resource):
    @professores_ns.marshal_list_with(professor_output_model)
    def get(self):
        """Lista todos os professores"""
        return listar_professores()

    @professores_ns.expect(professor_model)
    @professores_ns.response(201, "Professor adicionado com sucesso!")
    def post(self):
        """Cria um novo professor"""
        data = professores_ns.payload
        adicionar_professor(data)
        return {"message": "Professor adicionado com sucesso!"}, 201

@professores_ns.route("/<int:professor_id>")
class ProfessorIdResource(Resource):
    @professores_ns.marshal_with(professor_output_model)
    @professores_ns.response(404, "Professor não encontrado")
    def get(self, professor_id):
        """Obtém um professor pelo ID"""
        return professor_por_id(professor_id)

    @professores_ns.expect(professor_model)
    @professores_ns.response(200, "Professor atualizado com sucesso!")
    @professores_ns.response(404, "Professor não encontrado")
    def put(self, professor_id):
        """Atualiza um professor pelo ID"""
        data = professores_ns.payload
        atualizar_professor(professor_id, data)
        return {"message": "Professor atualizado com sucesso!"}, 200

    @professores_ns.response(200, "Professor excluído com sucesso!")
    @professores_ns.response(404, "Professor não encontrado")
    def delete(self, professor_id):
        """Exclui um professor pelo ID"""
        excluir_professor(professor_id)
        return {"message": "Professor excluído com sucesso!"}, 200
