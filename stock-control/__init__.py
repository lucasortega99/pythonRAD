import os
from flask import Flask


def create_app(test_config=None):
    # Cria e configura o app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db',
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    )

    # Verifica se a pasta de instância existe, se não, cria
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Importa o db e inicializa
    from .models import db
    db.init_app(app)
    with app.app_context():
        db.create_all()
        
    # Importa o flask-login e inicializa
    from .models import login_manager
    login_manager.init_app(app)
    login_manager.login_view = '/auth/login'
        
    # Registra o bcrypt para hashing de senhas
    from .models import bcrypt
    bcrypt.init_app(app)
        
    # Importa as blueprints e registra
    from . import auth
    from . import stock_control

    app.register_blueprint(auth.bp)
    app.register_blueprint(stock_control.bp)

    # make url_for('index') == url_for('blog.index')
    app.add_url_rule("/", endpoint="stock_control.index")

    return app