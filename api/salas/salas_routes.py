from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from .salas_model import SalaNaoEncontrada, listar_salas, sala_por_id, adicionar_sala, atualizar_sala, reservar_sala, excluir_sala, excluir_todas_salas, cancelar_reserva
from config import db

salas_blueprint = Blueprint('salas', __name__)

@salas_blueprint.route('/salas', methods=['GET'])
def get_salas():
    salas = listar_salas()
    return jsonify(salas)

@salas_blueprint.route('/salas/<int:id_sala>', methods=['GET'])
def get_sala(id_sala):
    try:
        sala = sala_por_id(id_sala)
        return jsonify({'sala': sala})
    except SalaNaoEncontrada:
        return jsonify({'message': 'sala não encontrada'}), 404


@salas_blueprint.route('/salas', methods=['POST'])
def create_sala():
    dados = request.json
    response, status_code = adicionar_sala(dados)
    return jsonify(response), status_code 


@salas_blueprint.route('/salas/<int:id_sala>', methods=['PUT'])
def update_sala(id_sala):
    dados = request.json
    try:
        sala = sala_por_id(id_sala)
        if not sala:
            return jsonify({'message': 'sala não encontrada'}), 404
        atualizar_sala(id_sala, dados)
        return jsonify(dados), 200  

    except SalaNaoEncontrada:
        return jsonify({'message': 'sala não encontrada'}), 404

@salas_blueprint.route('/salas/reservar/<int:id_sala>', methods=['PUT'])
def reserva_sala(id_sala):
    dados = request.json
    try:
        sala = sala_por_id(id_sala)
        if not sala:
            return jsonify({'message': 'sala não encontrada'}), 404
        reservar_sala(id_sala, dados)
        return jsonify(dados), 200  

    except SalaNaoEncontrada:
        return jsonify({'message': 'sala não encontrada'}), 404

@salas_blueprint.route('/salas/cancelar/<int:id_sala>', methods=['DELETE'])
def cancela_reserva(id_sala):
    try:
        sala = sala_por_id(id_sala)
        if not sala:
            return jsonify({'message': 'sala não encontrada'}), 404
        cancelar_reserva(id_sala)
        return 200  

    except SalaNaoEncontrada:
        return jsonify({'message': 'sala não encontrada'}), 404

@salas_blueprint.route('/salas/delete/<int:id_sala>', methods=['DELETE'])
def delete_sala(id_sala):
    try:
        print(id_sala)
        excluir_sala(id_sala)
        return jsonify({'message': 'sala excluída com sucesso'}), 200
    except SalaNaoEncontrada:
        return jsonify({'message': 'sala não encontrada'}), 404

@salas_blueprint.route('/salas/deleteall', methods=['DELETE'])
def delete_all_salas():
    try:
        excluir_todas_salas()
        return jsonify({'message': 'Todas as salas foram excluídas com sucesso'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500