from config import db

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
    # id_responsavel = db.Column(db.Integer, db.ForeignKey('responsaveis.id'), nullable=True) # precisa fazer

    def __init__(self, nome, capacidade):
      self.nome = nome
      self.capacidade = capacidade
      self.status_sala = True
      self.turma = None
      self.data = None
      self.hora_inicio = None
      self.hora_termino = None
      # self.id_responsavel = None

    def to_dict(self):
      if self.status_sala:
        disponibilidade = "Disponível"
      else:
        disponibilidade = "Indisponível"
        
      return {
        'id': self.id,
        'nome': self.nome,
        'capacidade': self.capacidade,
        'status_sala': disponibilidade
      }
class SalaNaoEncontrada(Exception):
  pass

def sala_por_id(sala_id):
  sala = Sala.query.get(sala_id)
  if not sala:
    raise SalaNaoEncontrada(f'sala com ID {sala_id} não encontrada.')
  return sala.to_dict()

def listar_salas():
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


def atualizar_sala(sala_id, novos_dados):
  sala = Sala.query.get(sala_id)

  if not sala:
    raise SalaNaoEncontrada(f'sala com ID {sala_id} não encontrada.')

  sala.nome = novos_dados['nome']

  db.session.commit()

def reservar_sala(sala_id, dados):
  sala = Sala.query.get(sala_id)
  if not sala:
    raise SalaNaoEncontrada(f'sala com ID {sala_id} não encontrada.')
  if sala.status_sala:
    sala.status_sala = False
    sala.turma = dados['turma']
    sala.data = dados['data']
    sala.hora_inicio = dados['hora_inicio']
    sala.hora_termino = dados['hora_termino']
    # sala.id_responsavel = dados['id_responsavel']
    db.session.commit()
    return {'message': 'sala reservada com sucesso!'}, 200
  else:
    return {'message': 'sala indisponível'}, 400
    

def excluir_sala(sala_id):
  sala = Sala.query.get(sala_id)
  if not sala:
    raise SalaNaoEncontrada(f'sala com ID {sala_id} não encontrada.')
  db.session.delete(sala)
  db.session.commit()

def excluir_todas_salas():
    salas = Sala.query.all()
    if not salas:
        raise SalaNaoEncontrada("Não há salas para excluir.") 

    for sala in salas:
        db.session.delete(sala)
    db.session.commit()