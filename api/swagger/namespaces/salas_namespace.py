from flask_restx import Namespace, Resource, fields
from salas.salas_model import listar_salas, adicionar_sala, sala_por_id, atualizar_sala, reservar_sala, excluir_sala

salas_ns = Namespace("salas", description="Operações relacionadas às salas")

sala_model = salas_ns.model("Sala", {
    "nome": fields.String(required=True, description="Nome da sala"),
    "capacidade": fields.Integer(required=True, description="Capacidade da sala"),
})

sala_output_model = salas_ns.model("SalaOutput", {
    "id": fields.Integer(description="ID da sala"),
    "nome": fields.String(description="Nome da sala"),
    "capacidade": fields.Integer(description="Capacidade da sala"),
    "status_sala": fields.String(description="Disponibilidade da sala"),
})

reserva_model = salas_ns.model("ReservaSala", {
    "turma": fields.String(required=True, description="Turma que utilizará a sala"),
    "data": fields.String(required=True, description="Data da reserva (YYYY-MM-DD)"),
    "hora_inicio": fields.String(required=True, description="Horário de início da reserva (HH:MM:SS)"),
    "hora_termino": fields.String(required=True, description="Horário de término da reserva (HH:MM:SS)"),
})

@salas_ns.route("/")
class SalasResource(Resource):
    @salas_ns.marshal_list_with(sala_output_model)
    def get(self):
        """Lista todas as salas"""
        return listar_salas()

    @salas_ns.expect(sala_model)
    @salas_ns.response(201, "Sala criada com sucesso!")
    def post(self):
        """Cria uma nova sala"""
        data = salas_ns.payload
        return adicionar_sala(data)

@salas_ns.route("/<int:sala_id>")
class SalaIdResource(Resource):
    @salas_ns.marshal_with(sala_output_model)
    @salas_ns.response(404, "Sala não encontrada")
    def get(self, sala_id):
        """Obtém uma sala pelo ID"""
        return sala_por_id(sala_id)

    @salas_ns.expect(sala_model)
    @salas_ns.response(200, "Sala atualizada com sucesso!")
    @salas_ns.response(404, "Sala não encontrada")
    def put(self, sala_id):
        """Atualiza uma sala pelo ID"""
        data = salas_ns.payload
        atualizar_sala(sala_id, data)
        return {"message": "Sala atualizada com sucesso!"}, 200

    @salas_ns.response(200, "Sala excluída com sucesso!")
    @salas_ns.response(404, "Sala não encontrada")
    def delete(self, sala_id):
        """Exclui uma sala pelo ID"""
        excluir_sala(sala_id)
        return {"message": "Sala excluída com sucesso!"}, 200

@salas_ns.route("/<int:sala_id>/reservar")
class SalaReservaResource(Resource):
    @salas_ns.expect(reserva_model)
    @salas_ns.response(200, "Sala reservada com sucesso!")
    @salas_ns.response(400, "Sala indisponível")
    @salas_ns.response(404, "Sala não encontrada")
    def post(self, sala_id):
        """Reserva uma sala"""
        data = salas_ns.payload
        return reservar_sala(sala_id, data)
