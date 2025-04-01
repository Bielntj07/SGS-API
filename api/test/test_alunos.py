import unittest
from config import db, app
from alunos.alunos_model import Aluno, adicionar_aluno, listar_alunos, aluno_por_id, atualizar_aluno, excluir_aluno, AlunoNaoEncontrado
from turmas.turmas_model import Turma

class TestAlunoModel(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.app_context = app.app_context()
        cls.app_context.push()
        db.create_all()
    
    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()
    
    def setUp(self):
        self.turma = Turma(nome="Turma Teste")
        db.session.add(self.turma)
        db.session.commit()
    
    def tearDown(self):
        db.session.query(Aluno).delete()
        db.session.query(Turma).delete()
        db.session.commit()
    
    def test_adicionar_aluno(self):
        dados_aluno = {"nome": "João", "email": "joao@email.com", "turma_id": self.turma.id}
        response, status_code = adicionar_aluno(dados_aluno)
        self.assertEqual(status_code, 201)
        self.assertEqual(response["message"], "Aluno adicionado com sucesso!")
    
    def test_listar_alunos(self):
        adicionar_aluno({"nome": "Maria", "email": "maria@email.com", "turma_id": self.turma.id})
        alunos = listar_alunos()
        self.assertGreater(len(alunos), 0)
    
    def test_aluno_por_id(self):
        adicionar_aluno({"nome": "Carlos", "email": "carlos@email.com", "turma_id": self.turma.id})
        aluno = Aluno.query.first()
        aluno_dict = aluno_por_id(aluno.id)
        self.assertEqual(aluno_dict["nome"], "Carlos")
    
    def test_atualizar_aluno(self):
        adicionar_aluno({"nome": "Ana", "email": "ana@email.com", "turma_id": self.turma.id})
        aluno = Aluno.query.first()
        response = atualizar_aluno(aluno.id, {"nome": "Ana Souza", "email": "ana_souza@email.com", "turma_id": self.turma.id})
        self.assertEqual(response["message"], "Aluno atualizado com sucesso!")
    
    def test_excluir_aluno(self):
        adicionar_aluno({"nome": "Bruno", "email": "bruno@email.com", "turma_id": self.turma.id})
        aluno = Aluno.query.first()
        response = excluir_aluno(aluno.id)
        self.assertEqual(response["message"], "Aluno excluído com sucesso!")
    
    def test_aluno_nao_encontrado(self):
        with self.assertRaises(AlunoNaoEncontrado):
            aluno_por_id(999)

if __name__ == "__main__":
    unittest.main()
