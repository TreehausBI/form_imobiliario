from flask_sqlalchemy import SQLAlchemy
from datetime import date
from .extensions import db

class Construtora(db.Model):
    __tablename__ = 'construtora'
    id_construtora = db.Column(db.Integer, primary_key=True)
    nome_construtora = db.Column(db.String(255), unique=True, nullable=False)
    
    # Relacionamento para acessar empreendimentos a partir da construtora
    empreendimentos = db.relationship('Empreendimento', backref='construtora', lazy=True)

class Bairro(db.Model):
    __tablename__ = 'bairro'
    id_bairro = db.Column(db.Integer, primary_key=True)
    nome_bairro = db.Column(db.String(255), unique=True, nullable=False)
    
    empreendimentos = db.relationship('Empreendimento', backref='bairro', lazy=True)

class Posicao(db.Model):
    __tablename__ = 'posicao'
    id_posicao = db.Column(db.Integer, primary_key=True)
    nome_posicao = db.Column(db.String(100), unique=True, nullable=False)
    
    imoveis = db.relationship('Imovel', backref='posicao', lazy=True)

# --- Tabelas Principais ---

class Empreendimento(db.Model):
    __tablename__ = 'empreendimento'
    id_empreendimento = db.Column(db.Integer, primary_key=True)
    nome_empreendimento = db.Column(db.String(255), nullable=False)
    id_construtora = db.Column(db.Integer, db.ForeignKey('construtora.id_construtora'), nullable=False)
    id_bairro = db.Column(db.Integer, db.ForeignKey('bairro.id_bairro'), nullable=False)
    distancia_mar = db.Column(db.Numeric)
    inicio_vendas = db.Column(db.Date)
    quadra = db.Column(db.Integer)
    lote = db.Column(db.Integer)
    endereco = db.Column(db.String(255), nullable=False)
    id_cartografica = db.Column(db.Integer)
    data_entrega = db.Column(db.Date)
    distancia_ao_empreendimento = db.Column(db.Numeric) 
    qtd_elevadores = db.Column(db.Integer)
    contato = db.Column(db.Text)

    # Relacionamentos
    equipamento = db.relationship('Equipamento', backref='empreendimento', uselist=False)
    imoveis = db.relationship('Imovel', backref='empreendimento', lazy=True)
    condicoes_pagamento = db.relationship('CondicaoPagamento', backref='empreendimento', lazy=True)

class Equipamento(db.Model):
    __tablename__ = 'equipamento'
    id_equipamento = db.Column(db.Integer, primary_key=True)
    id_empreendimento = db.Column(db.Integer, db.ForeignKey('empreendimento.id_empreendimento'), unique=True)
    piscina = db.Column(db.Integer, default=0, nullable=False)
    coworking = db.Column(db.Integer, default=0, nullable=False)
    lavanderia = db.Column(db.Integer, default=0, nullable=False)
    restaurante_bar = db.Column(db.Integer, default=0, nullable=False)
    academia = db.Column(db.Integer, default=0, nullable=False)
    pet_playground = db.Column(db.Integer, default=0, nullable=False)
    salao_festas = db.Column(db.Integer, default=0, nullable=False)
    sauna = db.Column(db.Integer, default=0, nullable=False)
    minimarket = db.Column(db.Integer, default=0, nullable=False)

class CondicaoPagamento(db.Model):
    __tablename__ = 'condicao_pagamento'
    id_condicao = db.Column(db.Integer, primary_key=True)
    id_empreendimento = db.Column(db.Integer, db.ForeignKey('empreendimento.id_empreendimento'), nullable=False)
    sinal = db.Column(db.String(255))
    mensais = db.Column(db.String(255))
    ordem = db.Column(db.Integer)  
    intercaladas = db.Column(db.String(255))
    habite_se = db.Column(db.String(255)) 

    __table_args__ = (
        db.UniqueConstraint(
            'id_empreendimento',
            'ordem',
            name='uq_condicao_empreendimento_ordem'
        ),
    )

class Imovel(db.Model):
    __tablename__ = 'imovel'
    id_imovel = db.Column(db.Integer, primary_key=True)
    id_empreendimento = db.Column(db.Integer, db.ForeignKey('empreendimento.id_empreendimento'))
    pavimento = db.Column(db.String(50))
    apartamento = db.Column(db.String(50))
    qtd_quartos = db.Column(db.String(50))
    id_posicao = db.Column(db.Integer, db.ForeignKey('posicao.id_posicao'))
    area_interna = db.Column(db.Numeric(10, 2))
    area_externa = db.Column(db.Numeric(10, 2))
    vagas = db.Column(db.String(50))
    bwc = db.Column(db.Integer)
    unidades_por_pavimento = db.Column(db.Integer)

    valores = db.relationship(
    "Valores",
    backref="imovel",
    cascade="all, delete"
)

class Valores(db.Model):
    __tablename__ = 'valores'
    id_valor = db.Column(db.Integer, primary_key=True)
    id_imovel = db.Column(db.Integer, db.ForeignKey('imovel.id_imovel'))
    mes_referencia = db.Column(db.Date)
    valor_total = db.Column(db.Numeric(12, 2))
    status = db.Column(db.String(50))
    atualizado_em = db.Column(db.Date, default=date.today)

    __table_args__ = (
        db.UniqueConstraint(
            'id_imovel', 
            'mes_referencia', 
            name='uq_valor_imovel_mes'
        ),
    )
    