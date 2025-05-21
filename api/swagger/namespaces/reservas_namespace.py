from flask_restx import Namespace, Resource, fields
from salas.reservas_service import listar_reservas_sala, cancelar_reserva, buscar_reserva_por_id

reservas_ns = Namespace("reservas", description="Reservas de Salas")

reserva_output_model = reservas_ns.model("ReservaOutput", {
    "id": fields.Integer(),
    "sala_id": fields.Integer(),
    "turma": fields.String(),
    "data": fields.String(),
    "hora_inicio": fields.String(),
    "hora_termino": fields.String(),
})

@reservas_ns.route("/salas/<int:sala_id>/reservas")
class ReservasSalaResource(Resource):
    @reservas_ns.marshal_list_with(reserva_output_model)
    def get(self, sala_id):
        """Lista todas as reservas de uma sala"""
        return listar_reservas_sala(sala_id)

@reservas_ns.route("/<int:reserva_id>")
class ReservaIdResource(Resource):
    @reservas_ns.marshal_with(reserva_output_model)
    @reservas_ns.response(404, "Reserva não encontrada")
    def get(self, reserva_id):
        """Consulta uma reserva específica pelo ID"""
        reserva = buscar_reserva_por_id(reserva_id)
        if reserva:
            return reserva, 200
        else:
            return {"message": "Reserva não encontrada"}, 404

    @reservas_ns.expect(reservas_ns.model("ReservaEditInput", {
        "turma": fields.String(required=False),
        "professor": fields.String(required=False),
        "data": fields.String(required=False, example="2025-05-22"),
        "hora_inicio": fields.String(required=False, example="10:00"),
        "hora_termino": fields.String(required=False, example="12:00"),
    }))
    @reservas_ns.marshal_with(reserva_output_model)
    @reservas_ns.response(200, "Reserva atualizada com sucesso")
    @reservas_ns.response(404, "Reserva não encontrada")
    def put(self, reserva_id):
        """Edita uma reserva existente"""
        from salas.reservas_service import editar_reserva
        dados = reservas_ns.payload
        reserva = editar_reserva(reserva_id, dados)
        if reserva:
            return reserva, 200
        else:
            return {"message": "Reserva não encontrada"}, 404

@reservas_ns.route("/<int:reserva_id>/cancelar")
class CancelarReservaResource(Resource):
    @reservas_ns.response(200, "Reserva cancelada com sucesso")
    @reservas_ns.response(404, "Reserva não encontrada")
    def delete(self, reserva_id):
        """Cancela uma reserva específica pelo ID"""
        resultado = cancelar_reserva(reserva_id)
        if resultado:
            return {"message": "Reserva cancelada com sucesso"}, 200
        else:
            return {"message": "Reserva não encontrada"}, 404
