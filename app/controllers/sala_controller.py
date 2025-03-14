from app.models.sala import Sala
from app import db

def get_salas():
    """Retorna todas as salas cadastradas."""
    return Sala.query.all()

def get_sala_by_id(sala_id):
    """Retorna uma sala específica pelo ID."""
    return Sala.query.get(sala_id)

def reservar_sala(sala_id):
    """Exemplo de função para reservar uma sala"""
    sala = get_sala_by_id(sala_id)
    if sala and sala.disponivel:
        sala.disponivel = False
        db.session.commit()
        return sala
    return None
