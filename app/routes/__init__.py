from .main import main
from .imovel import imovel_bp
from .valores import valores_bp
from .empreendimento import empreendimento_bp

def init_app(app):
    app.register_blueprint(main)
    app.register_blueprint(empreendimento_bp)
    app.register_blueprint(imovel_bp)
    app.register_blueprint(valores_bp)
    app.register(api_bp)