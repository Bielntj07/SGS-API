from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializa a extensão do banco de dados
    db.init_app(app)
    
    # Importa e registra os blueprints
    from app.routes.sala_routes import sala_bp
    app.register_blueprint(sala_bp, url_prefix='/salas')
    
    return app