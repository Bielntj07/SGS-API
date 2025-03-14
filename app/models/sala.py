from app import db

class Sala(db.Model):
    __tablename__ = 'salas'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    capacidade = db.Column(db.Integer, nullable=False)
    disponivel = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f"<Sala {self.nome}>"