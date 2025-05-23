from .reservas_model import Reserva
from config import db
from datetime import datetime
from sqlalchemy import and_

class ReservaConflito(Exception):
    pass

def reservar_sala(sala_id, dados):
    data_reserva = datetime.strptime(dados['data'], "%Y-%m-%d").date()
    hora_inicio_reserva = datetime.strptime(dados['hora_inicio'], "%H:%M").time()
    hora_termino_reserva = datetime.strptime(dados['hora_termino'], "%H:%M").time()

    conflito = Reserva.query.filter(
        Reserva.sala_id == sala_id,
        Reserva.data == data_reserva,
        and_(
            Reserva.hora_inicio < hora_termino_reserva,
            Reserva.hora_termino > hora_inicio_reserva
        )
    ).first()

    if conflito:
        raise ReservaConflito('Sala já está reservada nesse horário')

    reserva = Reserva(
        sala_id=sala_id,
        turma=dados.get('turma'),
        professor=dados.get('professor'),
        data=data_reserva,
        hora_inicio=hora_inicio_reserva,
        hora_termino=hora_termino_reserva
    )
    db.session.add(reserva)
    db.session.commit()
    return reserva

def listar_reservas_sala(sala_id):
    reservas = Reserva.query.filter_by(sala_id=sala_id).all()
    return [r.to_dict() for r in reservas]

def cancelar_reserva(reserva_id):
    reserva = Reserva.query.get(reserva_id)
    if not reserva:
        return None
    db.session.delete(reserva)
    db.session.commit()
    return True

def editar_reserva(reserva_id, novos_dados):
    reserva = Reserva.query.get(reserva_id)
    if not reserva:
        return None
    # Atualiza apenas os campos fornecidos
    if 'turma' in novos_dados:
        reserva.turma = novos_dados['turma']
    if 'professor' in novos_dados:
        reserva.professor = novos_dados['professor']
    if 'data' in novos_dados:
        reserva.data = datetime.strptime(novos_dados['data'], "%Y-%m-%d").date()
    if 'hora_inicio' in novos_dados:
        reserva.hora_inicio = datetime.strptime(novos_dados['hora_inicio'], "%H:%M").time()
    if 'hora_termino' in novos_dados:
        reserva.hora_termino = datetime.strptime(novos_dados['hora_termino'], "%H:%M").time()
    db.session.commit()
    return reserva

def buscar_reserva_por_id(reserva_id):
    reserva = Reserva.query.get(reserva_id)
    return reserva.to_dict() if reserva else None
