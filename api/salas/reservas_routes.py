from flask import Blueprint, request, jsonify
from .reservas_service import reservar_sala, listar_reservas_sala, ReservaConflito, cancelar_reserva, buscar_reserva_por_id

reservas_blueprint = Blueprint('reservas', __name__)

@reservas_blueprint.route('/salas/<int:id_sala>/reservas', methods=['GET'])
def get_reservas(id_sala):
    reservas = listar_reservas_sala(id_sala)
    return jsonify(reservas)

@reservas_blueprint.route('/salas/<int:id_sala>/reservar', methods=['POST'])
def reservar(id_sala):
    dados = request.json
    try:
        reserva = reservar_sala(id_sala, dados)
        return jsonify(reserva.to_dict()), 201
    except ReservaConflito:
        return jsonify({'message': 'Já existe uma reserva para a sala, data e horário definidos.'}), 400

@reservas_blueprint.route('/reservas/<int:reserva_id>', methods=['GET'])
def get_reserva(reserva_id):
    reserva = buscar_reserva_por_id(reserva_id)
    if reserva:
        return jsonify(reserva), 200
    else:
        return jsonify({'message': 'Reserva não encontrada'}), 404

@reservas_blueprint.route('/reservas/<int:reserva_id>', methods=['PUT'])
def editar_reserva(reserva_id):
    from .reservas_service import editar_reserva
    dados = request.json
    reserva = editar_reserva(reserva_id, dados)
    if reserva:
        return jsonify(reserva.to_dict()), 200
    else:
        return jsonify({'message': 'Reserva não encontrada'}), 404

@reservas_blueprint.route('/reservas/<int:reserva_id>/cancelar', methods=['DELETE'])
def cancelar(reserva_id):
    resultado = cancelar_reserva(reserva_id)
    if resultado:
        return jsonify({'message': 'Reserva cancelada com sucesso'}), 200
    else:
        return jsonify({'message': 'Reserva não encontrada'}), 404
