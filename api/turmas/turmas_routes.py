from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from .turmas_model import TurmaNaoEncontrado, listar_turmas, turma_por_id, adicionar_turma, atualizar_turma, excluir_turma, excluir_todas_turmas
from config import db

turmas_blueprint = Blueprint('turmas', __name__)

@turmas_blueprint.route('/turmas', methods=['GET'])
def get_turmas():
    turmas = listar_turmas()
    return jsonify(turmas)

@turmas_blueprint.route('/turmas/<int:id_turma>', methods=['GET'])
def get_turma(id_turma):
    try:
        turma = turma_por_id(id_turma)
        return jsonify({'turma': turma})
    except TurmaNaoEncontrado:
        return jsonify({'message': 'Turma não encontrada'}), 404


@turmas_blueprint.route('/turmas', methods=['POST'])
def create_turma():
    dados = request.json
    response, status_code = adicionar_turma(dados)
    return jsonify(response), status_code 


@turmas_blueprint.route('/turmas/<int:id_turma>', methods=['PUT'])
def update_turma(id_turma):
    dados = request.json
    try:
        turma = turma_por_id(id_turma)
        if not turma:
            return jsonify({'message': 'Turma não encontrada'}), 404
        atualizar_turma(id_turma, dados)
        return jsonify(dados), 200  

    except TurmaNaoEncontrado:
        return jsonify({'message': 'Turma não encontrada'}), 404

@turmas_blueprint.route('/turmas/delete/<int:id_turma>', methods=['DELETE'])
def delete_turma(id_turma):
    try:
        print(id_turma)
        excluir_turma(id_turma)
        return jsonify({'message': 'Turma excluída com sucesso'}), 200
    except TurmaNaoEncontrado:
        return jsonify({'message': 'Turma não encontrada'}), 404

@turmas_blueprint.route('/turmas/deleteall', methods=['DELETE'])
def delete_all_turmas():
    try:
        excluir_todas_turmas()
        return jsonify({'message': 'Todas as turmas foram excluídas com sucesso'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500