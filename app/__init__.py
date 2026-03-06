from flask import Flask
from .extensions import db
from .config import config

def create_app(config_name="default"):
    app = Flask(__name__)

    # 🔹 1. carregar config PRIMEIRO
    app.config.from_object(config[config_name])

    # (opcional, só pra debug — pode remover depois)
    print("DB URI:", app.config.get("SQLALCHEMY_DATABASE_URI"))

    # 🔹 2. inicializar extensões DEPOIS da config
    db.init_app(app)

    from .extensions import migrate
    migrate.init_app(app, db)

    from .routes.empreendimento import empreendimento_bp
    from .routes.imovel import imovel_bp
    from .routes.valores import valores_bp
    from .routes.main import main
    from .routes.exportacao import export_bp

    app.register_blueprint(empreendimento_bp)
    app.register_blueprint(imovel_bp)
    app.register_blueprint(valores_bp)
    app.register_blueprint(main)
    app.register_blueprint(export_bp)

    return app
