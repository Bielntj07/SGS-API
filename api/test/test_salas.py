import unittest
from config import db, app
from salas.salas_model import Sala, sala_por_id, listar_salas, adicionar_sala, atualizar_sala, reservar_sala, excluir_sala, excluir_todas_salas, SalaNaoEncontrada

class TestSala(unittest.TestCase):
    
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_adicionar_sala(self):
        response, status_code = adicionar_sala({"nome": "Sala A", "capacidade": 30})
        self.assertEqual(status_code, 201)
        self.assertEqual(response["message"], "sala criada com sucesso!")
    
    def test_listar_salas(self):
        adicionar_sala({"nome": "Sala A", "capacidade": 30})
        salas = listar_salas()
        self.assertEqual(len(salas), 1)
        self.assertEqual(salas[0]['nome'], "Sala A")
    
    def test_sala_por_id(self):
        adicionar_sala({"nome": "Sala B", "capacidade": 40})
        sala = Sala.query.first()
        result = sala_por_id(sala.id)
        self.assertEqual(result['nome'], "Sala B")
    
    def test_atualizar_sala(self):
        adicionar_sala({"nome": "Sala C", "capacidade": 25})
        sala = Sala.query.first()
        atualizar_sala(sala.id, {"nome": "Sala C Atualizada"})
        sala_atualizada = Sala.query.get(sala.id)
        self.assertEqual(sala_atualizada.nome, "Sala C Atualizada")
    
    def test_reservar_sala(self):
        adicionar_sala({"nome": "Sala D", "capacidade": 35})
        sala = Sala.query.first()
        response, status_code = reservar_sala(sala.id, {"turma": "Turma 1", "data": "2025-04-01", "hora_inicio": "08:00", "hora_termino": "10:00"})
        self.assertEqual(status_code, 200)
        self.assertEqual(response["message"], "sala reservada com sucesso!")
    
    def test_excluir_sala(self):
        adicionar_sala({"nome": "Sala E", "capacidade": 20})
        sala = Sala.query.first()
        excluir_sala(sala.id)
        self.assertIsNone(Sala.query.get(sala.id))
    
    def test_excluir_todas_salas(self):
        adicionar_sala({"nome": "Sala F", "capacidade": 45})
        excluir_todas_salas()
        self.assertEqual(len(Sala.query.all()), 0)
    
    def test_sala_nao_encontrada(self):
        with self.assertRaises(SalaNaoEncontrada):
            sala_por_id(9999)

if __name__ == "__main__":
    unittest.main()
