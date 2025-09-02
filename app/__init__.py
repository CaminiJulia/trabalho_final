# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    """Fábrica de aplicação."""
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///produtos.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = False
    
    db.init_app(app)

    # Importa o Blueprint do arquivo de rotas
    from .routes import main_bp
    # Registra o Blueprint na aplicação
    app.register_blueprint(main_bp)

    # Importa os modelos para que o SQLAlchemy os reconheça
    from . import models

    with app.app_context():
        db.create_all()
    
    return app