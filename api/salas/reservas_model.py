from config import db
from datetime import datetime

class Reserva(db.Model):
    __tablename__ = "reservas"
    id = db.Column(db.Integer, primary_key=True)
    sala_id = db.Column(db.Integer, db.ForeignKey('salas.id'), nullable=False)
    turma = db.Column(db.String(100), nullable=True)
    data = db.Column(db.Date, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_termino = db.Column(db.Time, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'sala_id': self.sala_id,
            'turma': self.turma,
            'data': self.data.strftime("%Y-%m-%d"),
            'hora_inicio': self.hora_inicio.strftime("%H:%M"),
            'hora_termino': self.hora_termino.strftime("%H:%M"),
        }
