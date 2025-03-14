from flask import Blueprint, jsonify, request
from app.controllers.sala_controller import get_salas, reservar_sala

sala_bp = Blueprint('sala_bp', __name__)

@sala_bp.route('/', methods=['GET'])
def listar_salas():
    """Endpoint para listar todas as salas."""
    salas = get_salas()
    salas_data = [{"id": sala.id, "nome": sala.nome, "capacidade": sala.capacidade, "disponivel": sala.disponivel} for sala in salas]
    return jsonify(salas_data)

@sala_bp.route('/<int:sala_id>/reservar', methods=['POST'])
def reservar(sala_id):
    """Endpoint para reservar uma sala."""
    sala = reservar_sala(sala_id)
    if sala:
        return jsonify({"message": f"Sala {sala.nome} reservada com sucesso."}), 200
    return jsonify({"message": "Sala não disponível ou não encontrada."}), 404
