from turmas.turmas_model import Turma
from config import db

class Aluno(db.Model):
  __tablename__ = "alunos"

  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(100),nullable=False)
  turmas = db.relationship("Turma", back_populates="alunos")
  turmas_id = db.Column(db.Integer, db.ForeignKey("turmas.id"), nullable=False)

  def __init__(self, nome, email, turma_id):
    self.nome = nome
    self.email = email
    self.turma_id = turma_id


  def to_dict(self):  
    return {
      'id': self.id, 
      'nome': self.nome, 
      'email': self.email, 
      'turma_id': self.turma_id
    }

class AlunoNaoEncontrado(Exception):
  pass

def aluno_por_id(id_aluno):
  aluno = Aluno.query.get(id_aluno)

  if not aluno:
    raise  AlunoNaoEncontrado(f'Aluno não encontrado com o id {id_aluno}')
  return aluno.to_dict()

def listar_alunos():
  alunos = Aluno.query.all()
  print(alunos)
  return [aluno.to_dict() for aluno in alunos]

def adicionar_aluno(novos_dados):
        turma = Turma.query.get(novos_dados['turma_id'])
        if(turma is None):
            return {"message": "Turma não existe"}, 404

        novo_aluno = Aluno(
            nome=novos_dados['nome'],
            email=novos_dados['email'],
            turma_id=int(novos_dados['turma_id'])
        )

        db.session.add(novo_aluno)
        db.session.commit()
        return {"message": "Aluno adicionado com sucesso!"}, 201



def atualizar_aluno(id_aluno, novos_dados):
  aluno = Aluno.query.get(id_aluno)
  if not aluno:
    raise AlunoNaoEncontrado

  aluno.nome = novos_dados['nome']
  aluno.email = novos_dados['email']
  aluno.turma_id = novos_dados['turma_id']

  db.session.commit()
  return {"message": "Aluno atualizado com sucesso!"}

def excluir_aluno(id_aluno):
  aluno = Aluno.query.get(id_aluno)
  if not aluno:
    raise AlunoNaoEncontrado(f'Aluno não encontrado com o id {id_aluno}')

  db.session.delete(aluno)
  db.session.commit()
  return {"message": "Aluno excluído com sucesso!"}