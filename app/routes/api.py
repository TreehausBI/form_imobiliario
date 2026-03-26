from flask import Blueprint, jsonify, Response
import pandas as pd
from app import db 

api_bp = Blueprint("api", __name__)

@api_bp.route("/fato_valores_csv")
def fato_valores_csv():

    engine = db.engine  

    def generate():
        first = True

        for chunk in pd.read_sql(
            "SELECT * FROM fato_valores",
            engine,  
            chunksize=5000
        ):
            yield chunk.to_csv(index=False, header=first, decimal=".")
            first = False

    return Response(generate(), mimetype="text/csv")

@api_bp.route("/dim_imovel_csv")
def dim_imovel_csv():

    query = """
    SELECT
        i.*,
        p.nome_posicao
    FROM imovel i
    JOIN posicao p ON p.id_posicao = i.id_posicao
    """

    df = pd.read_sql(query, db.engine)

    return Response(df.to_csv(index=False), mimetype="text/csv")

@api_bp.route("/dim_empreendimento_csv")
def dim_empreendimento_csv():

    query = """
    SELECT
        e.*,
        b.nome_bairro,
        c.nome_construtora
    FROM empreendimento e
    JOIN bairro b ON b.id_bairro = e.id_bairro
    JOIN construtora c ON c.id_construtora = e.id_construtora
    """

    df = pd.read_sql(query, db.engine)

    return Response(df.to_csv(index=False), mimetype="text/csv")

@api_bp.route("/dim_equipamento_csv")
def dim_equipamento_csv():

    df = pd.read_sql("SELECT * FROM equipamento", db.engine)

    return Response(df.to_csv(index=False), mimetype="text/csv")