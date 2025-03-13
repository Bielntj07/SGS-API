import unittest
from app import create_app, db
from app.models import Sala, Reserva
from datetime import datetime

class TestModels(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Executado uma vez antes de todos os testes"""
        cls.app = create_app()
        cls.client = cls.app.test_client()

        # Usando o contexto de app para interações com o banco de dados
        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Executado uma vez depois de todos os testes"""
        with cls.app.app_context():
            db.drop_all()  # Limpeza após os testes

    def test_criar_sala(self):
        """Testa a criação de uma sala"""
        sala = Sala(nome="Sala 101", capacidade=30)
        sala.save()

        # Verifica se a sala foi salva corretamente
        self.assertIsNotNone(sala.id)
        self.assertEqual(sala.nome, "Sala 101")
        self.assertEqual(sala.capacidade, 30)

    def test_criar_reserva(self):
        """Testa a criação de uma reserva"""
        sala = Sala(nome="Sala 101", capacidade=30)
        sala.save()

        reserva = Reserva(sala=sala, usuario_id=1, horario_inicio=datetime.now(), horario_fim=datetime.now())
        reserva.save()

        # Verifica se a reserva foi salva corretamente
        self.assertIsNotNone(reserva.id)
        self.assertEqual(reserva.sala.id, sala.id)
        self.assertEqual(reserva.usuario_id, 1)
        self.assertEqual(reserva.status, "Confirmado")

if __name__ == '__main__':
    unittest.main()