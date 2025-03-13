from flask_mongoengine import MongoEngine
from datetime import datetime

# Inicializando o MongoEngine
db = MongoEngine()

class Sala(db.Document):
    nome = db.StringField(required=True, max_length=100)
    capacidade = db.IntField(required=True)
    reservas = db.ListField(db.ReferenceField('Reserva', reverse_delete_rule=db.PULL))

    def __repr__(self):
        return f'<Sala {self.nome} (Capacidade: {self.capacidade})>'

class Reserva(db.Document):
    sala = db.ReferenceField(Sala, required=True)
    usuario_id = db.IntField(required=True)
    horario_inicio = db.DateTimeField(required=True)
    horario_fim = db.DateTimeField(required=True)
    status = db.StringField(default='Confirmado')  # Confirmado, Cancelado, etc.

    def __repr__(self):
        return f'<Reserva {self.id} - Sala {self.sala.nome}>'
