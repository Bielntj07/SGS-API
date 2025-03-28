from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from .admin_model import AdministradorNaoEncontrado, listar_administradores, administrador_por_id, adicionar_administrador, atualizar_administrador, excluir_administrador,excluir_todos_administradores
from config import db

administradores_blueprint = Blueprint('administradores', __name__)


@administradores_blueprint.route('/administradores', methods=['GET'])
def get_administradores():
    administradores = listar_administradores()
    return jsonify(administradores)

@administradores_blueprint.route('/administradores/<int:id_administrador>', methods=['GET'])
def get_administrador(id_administrador):
    try:
        administrador = administrador_por_id(id_administrador)
        return jsonify(administrador)
    except AdministradorNaoEncontrado:
        return jsonify({'message': 'administrador não encontrado'}), 404


@administradores_blueprint.route('/administradores', methods=['POST'])
def create_administrador():
    dados = request.json
    adicionar_administrador(dados)
    return jsonify(dados), 200


@administradores_blueprint.route('/administradores/<int:id_administrador>', methods=['PUT'])
def update_administrador(id_administrador):
    dados = request.json
    try:
        administrador = administrador_por_id(id_administrador)
        if not administrador:
            return jsonify({'message': 'administrador não encontrado'}), 404
        atualizar_administrador(id_administrador, dados)
        return jsonify(dados), 200
    except AdministradorNaoEncontrado:
        return jsonify({'message': 'administrador não encontrado'}), 404

@administradores_blueprint.route('/administradores/<int:id_administrador>', methods=['DELETE'])
def delete_administrador(id_administrador):
    try:
        excluir_administrador(id_administrador)
        return jsonify({'message': 'administrador excluído com sucesso '}), 200
    except AdministradorNaoEncontrado:
        return jsonify({'message': 'administrador não encontrado'}), 404

@administradores_blueprint.route('/administradores/deleteall', methods=['DELETE'])
def delete_all_administradores():
    try:
        excluir_todos_administradores()
        return jsonify({'message': 'Todos os administradores foram excluídos com sucesso'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
