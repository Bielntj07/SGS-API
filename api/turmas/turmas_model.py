from config import db

class Turma(db.Model):
    __tablename__ = "turmas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)  
    alunos = db.relationship("Aluno", back_populates="turma", lazy=True)

    def __init__(self, nome):
      self.nome = nome

    def to_dict(self):
      return {
        'id': self.id,
        'nome': self.nome,
      }
class TurmaNaoEncontrado(Exception):
  pass

def turma_por_id(turma_id):
  turma = Turma.query.get(turma_id)
  if not turma:
    raise TurmaNaoEncontrado(f'Turma com ID {turma_id} não encontrada.')
  return turma.to_dict()

def listar_turmas():
  turmas = Turma.query.all()
  return [turma.to_dict() for turma in turmas]

def adicionar_turma(turma_dados):
  nova_turma = Turma(
    nome=turma_dados['nome']
  )

  db.session.add(nova_turma)
  db.session.commit()
  return {'message': 'Turma criada com sucesso!'}, 201


def atualizar_turma(turma_id, novos_dados):
  turma = Turma.query.get(turma_id)

  if not turma:
    raise TurmaNaoEncontrado(f'Turma com ID {turma_id} não encontrada.')

  turma.nome = novos_dados['nome']

  db.session.commit()

def excluir_turma(turma_id):
  turma = Turma.query.get(turma_id)
  if not turma:
    raise TurmaNaoEncontrado(f'Turma com ID {turma_id} não encontrada.')
  db.session.delete(turma)
  db.session.commit()

def excluir_todas_turmas():
    turmas = Turma.query.all()
    if not turmas:
        raise TurmaNaoEncontrado("Não há turmas para excluir.") 

    for turma in turmas:
        db.session.delete(turma)
    db.session.commit()