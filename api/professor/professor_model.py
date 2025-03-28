from config import db

class Professor(db.Model):
    __tablename__ = 'professor'

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

class ProfessorNaoEncontrado(Exception):
    pass

def professor_por_id(professor_id):
    professor = Professor.query.get(professor_id)
    if not professor:
        raise ProfessorNaoEncontrado(f'Professor com ID {professor_id} não encontrado.')
    return professor.to_dict()


def listar_professores():
    professores = Professor.query.all()
    return [professor.to_dict() for professor in professores]

def adicionar_professor(professor_dados):
    novo_professor = Professor(
        nome=professor_dados['nome'],
        email=professor_dados['email']
    )
    db.session.add(novo_professor)
    db.session.commit()

def atualizar_professor(professor_id, novos_dados):
    professor = Professor.query.get(professor_id)
    if not professor:
        raise ProfessorNaoEncontrado(f'Professor com ID {professor_id} não encontrado.')

    professor.nome = novos_dados['nome']
    professor.email = novos_dados['email']
    
    db.session.commit()


def excluir_professor(professor_id):
    professor = Professor.query.get(professor_id)
    if not professor:
        raise ProfessorNaoEncontrado(f'Professor com ID {professor_id} não encontrado.')

    db.session.delete(professor)
    db.session.commit()

def excluir_todos_professores():
    professores = Professor.query.all()
    for professor in professores:
        db.session.delete(professor)
    db.session.commit()