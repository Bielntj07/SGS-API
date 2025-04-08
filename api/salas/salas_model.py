from config import db
from datetime import datetime
from sqlalchemy import and_

class Sala(db.Model):
    __tablename__ = "salas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    capacidade = db.Column(db.Integer, nullable=False)
    status_sala = db.Column(db.Boolean, nullable=False, default=True)
    turma = db.Column(db.String(100), nullable=True)
    data = db.Column(db.Date, nullable=True)
    hora_inicio = db.Column(db.Time, nullable=True)
    hora_termino = db.Column(db.Time, nullable=True)

    def __init__(self, nome, capacidade):
        self.nome = nome
        self.capacidade = capacidade
        self.status_sala = True
        self.turma = None
        self.data = None
        self.hora_inicio = None
        self.hora_termino = None

    def to_dict(self):
        disponibilidade = "Disponivel" if self.status_sala else "Indisponivel"
        return {
            'id': self.id,
            'nome': self.nome,
            'capacidade': self.capacidade,
            'status_sala': disponibilidade,
            'turma': self.turma,
            'data': self.data.strftime("%Y-%m-%d") if self.data else None,
            'hora_inicio': self.hora_inicio.strftime("%H:%M") if self.hora_inicio else None,
            'hora_termino': self.hora_termino.strftime("%H:%M") if self.hora_termino else None
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


def reservar_sala(sala_id, dados):
    sala = Sala.query.get(sala_id)
    if not sala:
        raise SalaNaoEncontrada(f'Sala com ID {sala_id} não encontrada.')

    # Converte os dados de horário
    data_reserva = datetime.strptime(dados['data'], "%Y-%m-%d").date()
    hora_inicio_reserva = datetime.strptime(dados['hora_inicio'], "%H:%M").time()
    hora_termino_reserva = datetime.strptime(dados['hora_termino'], "%H:%M").time()

    # Verifica se há conflito de horário com outras reservas
    conflito = Sala.query.filter(
        Sala.id == sala_id,
        Sala.status_sala == False,  # Apenas se estiver ocupada
        Sala.data == data_reserva,
        and_(
            Sala.hora_inicio < hora_termino_reserva,
            Sala.hora_termino > hora_inicio_reserva
        )
    ).first()

    if conflito:
        return {'message': 'Sala já está reservada nesse horário'}, 400

    # Reserva a sala
    sala.status_sala = False
    sala.turma = dados['turma']
    sala.data = data_reserva
    sala.hora_inicio = hora_inicio_reserva
    sala.hora_termino = hora_termino_reserva

    db.session.commit()
    return {'message': 'Sala reservada com sucesso!'}, 200


def cancelar_reserva(sala_id):
    sala = Sala.query.get(sala_id)
    if not sala:
        raise SalaNaoEncontrada(f'sala com ID {sala_id} não encontrada.')

    if not sala.status_sala:
        sala.status_sala = True
        sala.turma = None
        sala.data = None
        sala.hora_inicio = None
        sala.hora_termino = None
        
        db.session.commit()
        return {'message': 'Reserva cancelada com sucesso!'}, 200
    else:
        return {'message': 'Sala não está reservada.'}, 400

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
