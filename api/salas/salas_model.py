from config import db
from datetime import datetime
from sqlalchemy import and_

class Sala(db.Model):
    __tablename__ = "salas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    capacidade = db.Column(db.Integer, nullable=False)
    andar = db.Column(db.String(100), nullable=False)
    laboratorio = db.Column(db.Boolean, nullable=False)

    def __init__(self, nome, capacidade, andar, laboratorio):
        self.nome = nome
        self.capacidade = capacidade
        self.andar = andar
        self.laboratorio = laboratorio

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'capacidade': self.capacidade,
            'andar': self.andar,
            'laboratorio': self.laboratorio,
        }

class SalaNaoEncontrada(Exception):
    pass


def sala_por_id(sala_id: int) -> dict:
    """Retorna os dados de uma sala com base no seu ID."""
    sala = Sala.query.get(sala_id)
    if not sala:
        raise SalaNaoEncontrada(f'Sala com ID {sala_id} não encontrada.')
    return sala.to_dict()


def listar_salas() -> list:
    """Retorna todas as salas cadastradas no sistema."""
    salas = Sala.query.all()
    return [sala.to_dict() for sala in salas]


def adicionar_sala(sala_dados):
    nova_sala = Sala(
        nome=sala_dados['nome'],
        capacidade=sala_dados['capacidade'],
        andar=sala_dados['andar'],
        laboratorio=sala_dados['laboratorio']
    )

    db.session.add(nova_sala)
    db.session.commit()
    return {'message': 'sala criada com sucesso!'}, 201 


def atualizar_sala(sala_id: int, novos_dados: dict) -> None:
    """Atualiza os dados de uma sala existente."""
    sala = Sala.query.get(sala_id)

    if not sala:
        raise SalaNaoEncontrada(f'Sala com ID {sala_id} não encontrada.')

    for key, value in novos_dados.items():
        setattr(sala, key, value)

    db.session.commit()

def excluir_sala(sala_id: int) -> None:
    """Exclui uma sala do sistema."""
    sala = Sala.query.get(sala_id)
    if not sala:
        raise SalaNaoEncontrada(f'Sala com ID {sala_id} não encontrada.')
    db.session.delete(sala)
    db.session.commit()


def excluir_todas_salas() -> None:
    """Exclui todas as salas cadastradas no sistema."""
    salas = Sala.query.all()
    if not salas:
        raise SalaNaoEncontrada("Não há salas para excluir.")

    for sala in salas:
        db.session.delete(sala)
    db.session.commit()
