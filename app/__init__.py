    import os
    from flask import Flask
    from flask_swagger_ui import get_swaggerui_blueprint
    from flask_pymongo import PyMongo
    from dotenv import load_dotenv

    # Carrega as variáveis do arquivo .env
    load_dotenv()

    mongo = PyMongo()

    def create_app(config_filename=None):
        app = Flask(__name__)
        
        # Configurações utilizando variáveis de ambiente
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
        app.config['MONGO_URI'] = os.getenv('MONGO_URI')

        # Inicializa o PyMongo
        mongo.init_app(app)
        
        # Configuração do Swagger
        SWAGGER_URL = '/swagger'
        API_URL = '/static/swagger.yaml'
        swaggerui_bp = get_swaggerui_blueprint(
            SWAGGER_URL,
            API_URL,
            config={'app_name': "SGS API"}
        )
        app.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)
        
        # Registro dos blueprints
        from app.routes import main_bp
        app.register_blueprint(main_bp, url_prefix='/api')
        
        return app

    if __name__ == '__main__':
        app = create_app()
        app.run(debug=True)