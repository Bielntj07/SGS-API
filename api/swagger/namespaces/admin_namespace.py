from flask_restx import Namespace, Resource, fields
from admin.admin_model import listar_administradores, adicionar_administrador, administrador_por_id, atualizar_administrador, excluir_administrador

admin_ns = Namespace("administradores", description="Operações relacionadas aos administradores")

administrador_model = admin_ns.model("Administrador", {
    "nome": fields.String(required=True, description="Nome do administrador"),
    "email": fields.String(required=True, description="Email do administrador"),
})

administrador_output_model = admin_ns.model("AdministradorOutput", {
    "id": fields.Integer(description="ID do administrador"),
    "nome": fields.String(description="Nome do administrador"),
    "email": fields.String(description="Email do administrador"),
})

@admin_ns.route("/")
class AdministradoresResource(Resource):
    @admin_ns.marshal_list_with(administrador_output_model)
    def get(self):
        """Lista todos os administradores"""
        return listar_administradores()

    @admin_ns.expect(administrador_model)
    @admin_ns.response(201, "Administrador adicionado com sucesso!")
    def post(self):
        """Cria um novo administrador"""
        data = admin_ns.payload
        adicionar_administrador(data)
        return {"message": "Administrador adicionado com sucesso!"}, 201

@admin_ns.route("/<int:administrador_id>")
class AdministradorIdResource(Resource):
    @admin_ns.marshal_with(administrador_output_model)
    @admin_ns.response(404, "Administrador não encontrado")
    def get(self, administrador_id):
        """Obtém um administrador pelo ID"""
        return administrador_por_id(administrador_id)

    @admin_ns.expect(administrador_model)
    @admin_ns.response(200, "Administrador atualizado com sucesso!")
    @admin_ns.response(404, "Administrador não encontrado")
    def put(self, administrador_id):
        """Atualiza um administrador pelo ID"""
        data = admin_ns.payload
        atualizar_administrador(administrador_id, data)
        return {"message": "Administrador atualizado com sucesso!"}, 200

    @admin_ns.response(200, "Administrador excluído com sucesso!")
    @admin_ns.response(404, "Administrador não encontrado")
    def delete(self, administrador_id):
        """Exclui um administrador pelo ID"""
        excluir_administrador(administrador_id)
        return {"message": "Administrador excluído com sucesso!"}, 200
