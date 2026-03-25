from flask import Blueprint, jsonify, Response
import pandas as pd
from app import db 

api_bp = Blueprint("api", __name__)

@api_bp.route("/base_analitica")
def get_base():

    query = """
    SELECT *
    FROM base_analitica
    """

    df = pd.read_sql(query, db.engine)

    return df.to_json(orient="records")


@api_bp.route("/empreendimentos")
def get_empreendimentos():

    query = """
    SELECT
        id_empreendimento,
        nome_empreendimento,
        endereco
    FROM empreendimento
    """

    df = pd.read_sql(query, db.engine)

    return df.to_json(orient="records")

@api_bp.route("/base_analitica_csv")
def get_base_csv():

    def generate():
        for chunk in pd.read_sql(
            "SELECT * FROM base_analitica",
            db.engine,
            chunksize=5000
        ):
            yield chunk.to_csv(index=False, header=False)

    return Response(generate(), mimetype="text/csv")