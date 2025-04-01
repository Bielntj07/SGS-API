import unittest
from config import db, app
from turmas.turmas_model import Turma, TurmaNaoEncontrado, turma_por_id, listar_turmas, adicionar_turma, atualizar_turma, excluir_turma, excluir_todas_turmas

class TestTurma(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_adicionar_turma(self):
        response, status_code = adicionar_turma({'nome': 'Turma 1'})
        self.assertEqual(status_code, 201)
        self.assertEqual(response['message'], 'Turma criada com sucesso!')

    def test_listar_turmas(self):
        adicionar_turma({'nome': 'Turma 1'})
        adicionar_turma({'nome': 'Turma 2'})
        turmas = listar_turmas()
        self.assertEqual(len(turmas), 2)

    def test_turma_por_id(self):
        adicionar_turma({'nome': 'Turma 1'})
        turma = Turma.query.first()
        resultado = turma_por_id(turma.id)
        self.assertEqual(resultado['nome'], 'Turma 1')

    def test_atualizar_turma(self):
        adicionar_turma({'nome': 'Turma 1'})
        turma = Turma.query.first()
        atualizar_turma(turma.id, {'nome': 'Turma Atualizada'})
        turma_atualizada = Turma.query.get(turma.id)
        self.assertEqual(turma_atualizada.nome, 'Turma Atualizada')

    def test_excluir_turma(self):
        adicionar_turma({'nome': 'Turma 1'})
        turma = Turma.query.first()
        excluir_turma(turma.id)
        self.assertIsNone(Turma.query.get(turma.id))

    def test_excluir_todas_turmas(self):
        adicionar_turma({'nome': 'Turma 1'})
        adicionar_turma({'nome': 'Turma 2'})
        excluir_todas_turmas()
        self.assertEqual(len(Turma.query.all()), 0)

    def test_turma_nao_encontrada(self):
        with self.assertRaises(TurmaNaoEncontrado):
            turma_por_id(999)

if __name__ == '__main__':
    unittest.main()
