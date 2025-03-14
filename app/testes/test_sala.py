import unittest
from app import create_app, db
from app.models.sala import Sala

class SalaTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            # Criando uma sala de teste
            sala = Sala(nome='Sala 101', capacidade=30, disponivel=True)
            db.session.add(sala)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_listar_salas(self):
        response = self.client.get('/salas/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_reservar_sala(self):
        # Tenta reservar a sala com id 1
        response = self.client.post('/salas/1/reservar')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('reservada', data['message'])

if __name__ == '__main__':
    unittest.main()
