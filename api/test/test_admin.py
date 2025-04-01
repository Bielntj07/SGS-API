import unittest
from config import db, app
from admin.admin_model import Administrador, AdministradorNaoEncontrado, listar_administradores, adicionar_administrador, atualizar_administrador, excluir_administrador, excluir_todos_administradores

class TestAdministrador(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        with app.app_context():
            db.create_all()

    def setUp(self):
        with app.app_context():
            db.session.query(Administrador).delete()
            db.session.commit()
    
    def test_adicionar_administrador(self):
        with app.app_context():
            dados = {'nome': 'Teste', 'email': 'teste@email.com'}
            adicionar_administrador(dados)
            resultado = listar_administradores()
            self.assertEqual(len(resultado), 1)
            self.assertEqual(resultado[0]['nome'], 'Teste')
    
    def test_listar_administradores(self):
        with app.app_context():
            adicionar_administrador({'nome': 'Teste 1', 'email': 'teste1@email.com'})
            adicionar_administrador({'nome': 'Teste 2', 'email': 'teste2@email.com'})
            resultado = listar_administradores()
            self.assertEqual(len(resultado), 2)
    
    def test_atualizar_administrador(self):
        with app.app_context():
            adicionar_administrador({'nome': 'Antigo', 'email': 'antigo@email.com'})
            admin = Administrador.query.first()
            atualizar_administrador(admin.id, {'nome': 'Novo', 'email': 'novo@email.com'})
            atualizado = Administrador.query.get(admin.id)
            self.assertEqual(atualizado.nome, 'Novo')
    
    def test_excluir_administrador(self):
        with app.app_context():
            adicionar_administrador({'nome': 'Excluir', 'email': 'excluir@email.com'})
            admin = Administrador.query.first()
            excluir_administrador(admin.id)
            self.assertIsNone(Administrador.query.get(admin.id))
    
    def test_excluir_todos_administradores(self):
        with app.app_context():
            adicionar_administrador({'nome': 'Admin 1', 'email': 'admin1@email.com'})
            adicionar_administrador({'nome': 'Admin 2', 'email': 'admin2@email.com'})
            excluir_todos_administradores()
            self.assertEqual(len(listar_administradores()), 0)
    
    def test_administrador_nao_encontrado(self):
        with app.app_context():
            with self.assertRaises(AdministradorNaoEncontrado):
                excluir_administrador(9999)

if __name__ == '__main__':
    unittest.main()
