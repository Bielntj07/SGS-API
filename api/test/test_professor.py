import unittest
from config import db, app
from professor.professor_model import Professor, ProfessorNaoEncontrado, listar_professores, adicionar_professor, atualizar_professor, excluir_professor, professor_por_id

class TestProfessorModel(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_adicionar_professor(self):
        adicionar_professor({'nome': 'Carlos Silva', 'email': 'carlos@email.com'})
        professores = listar_professores()
        self.assertEqual(len(professores), 1)
        self.assertEqual(professores[0]['nome'], 'Carlos Silva')

    def test_listar_professores(self):
        adicionar_professor({'nome': 'Ana Souza', 'email': 'ana@email.com'})
        adicionar_professor({'nome': 'João Lima', 'email': 'joao@email.com'})
        professores = listar_professores()
        self.assertEqual(len(professores), 2)

    def test_professor_por_id(self):
        adicionar_professor({'nome': 'Maria Oliveira', 'email': 'maria@email.com'})
        professor = Professor.query.first()
        encontrado = professor_por_id(professor.id)
        self.assertEqual(encontrado['nome'], 'Maria Oliveira')
    
    def test_atualizar_professor(self):
        adicionar_professor({'nome': 'Pedro Silva', 'email': 'pedro@email.com'})
        professor = Professor.query.first()
        atualizar_professor(professor.id, {'nome': 'Pedro Santos', 'email': 'pedro@email.com'})
        professor_atualizado = Professor.query.get(professor.id)
        self.assertEqual(professor_atualizado.nome, 'Pedro Santos')
    
    def test_excluir_professor(self):
        adicionar_professor({'nome': 'Lucas Martins', 'email': 'lucas@email.com'})
        professor = Professor.query.first()
        excluir_professor(professor.id)
        self.assertEqual(len(listar_professores()), 0)
    
    def test_professor_nao_encontrado(self):
        with self.assertRaises(ProfessorNaoEncontrado):
            professor_por_id(999)

if __name__ == '__main__':
    unittest.main()
