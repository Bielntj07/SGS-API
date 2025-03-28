from config import db

class Administrador(db.Model):
    __tablename__ = 'administradores'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def __init__(self, nome, email):
        self.nome = nome
        self.email = email

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
        }

class AdministradorNaoEncontrado(Exception):
    pass

def administrador_por_id(administrador_id):
    administrador = Administrador.query.get(administrador_id)
    if not administrador:
        raise AdministradorNaoEncontrado(f'administrador com ID {administrador_id} não encontrado.')
    return administrador.to_dict()


def listar_administradores():
    administradores = Administrador.query.all()
    return [administrador.to_dict() for administrador in administradores]

def adicionar_administrador(administrador_dados):
    novo_administrador = Administrador(
        nome=administrador_dados['nome'],
        email=administrador_dados['email']
    )
    db.session.add(novo_administrador)
    db.session.commit()

def atualizar_administrador(administrador_id, novos_dados):
    administrador = Administrador.query.get(administrador_id)
    if not administrador:
        raise AdministradorNaoEncontrado(f'administrador com ID {administrador_id} não encontrado.')

    administrador.nome = novos_dados['nome']
    administrador.email = novos_dados['email']

    db.session.commit()

def excluir_administrador(administrador_id):
    administrador = Administrador.query.get(administrador_id)
    if not administrador:
        raise AdministradorNaoEncontrado(f'administrador com ID {administrador_id} não encontrado.')

    db.session.delete(administrador)
    db.session.commit()

def excluir_todos_administradores():
    administradores = Administrador.query.all()
    for administrador in administradores:
        db.session.delete(administrador)
    db.session.commit()