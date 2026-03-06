import pandas as pd
from flask import Blueprint, request, send_file
from datetime import date
from io import BytesIO
from app.models import (
    Empreendimento, Imovel, Valores,
    Bairro, Construtora, Posicao, Equipamento
)
from app.extensions import db

export_bp = Blueprint("export", __name__)

@export_bp.route("/exportar_excel")
def exportar_excel():

    mes = int(request.args.get("mes"))
    ano = int(request.args.get("ano"))

    mes_ref = date(ano, mes, 1)

    dados = (
        db.session.query(

            # EMPREENDIMENTO
            Empreendimento.nome_empreendimento,
            Construtora.nome_construtora,
            Bairro.nome_bairro,
            Empreendimento.endereco,
            Empreendimento.distancia_mar,
            Empreendimento.data_entrega,
            Empreendimento.qtd_elevadores,

            # EQUIPAMENTOS
            Equipamento.piscina,
            Equipamento.coworking,
            Equipamento.lavanderia,
            Equipamento.restaurante_bar,
            Equipamento.academia,
            Equipamento.pet_playground,
            Equipamento.salao_festas,
            Equipamento.sauna,
            Equipamento.minimarket,

            # IMOVEL
            Imovel.pavimento,
            Imovel.apartamento,
            Imovel.qtd_quartos,
            Posicao.nome_posicao,
            Imovel.area_interna,
            Imovel.area_externa,
            Imovel.vagas,
            Imovel.bwc,

            # VALORES
            Valores.valor_total,
            Valores.status,
            Valores.mes_referencia

        )

        .join(Imovel, Imovel.id_empreendimento == Empreendimento.id_empreendimento)
        .join(Valores, Valores.id_imovel == Imovel.id_imovel)
        .join(Posicao, Posicao.id_posicao == Imovel.id_posicao)
        .join(Construtora, Construtora.id_construtora == Empreendimento.id_construtora)
        .join(Bairro, Bairro.id_bairro == Empreendimento.id_bairro)
        .outerjoin(Equipamento, Equipamento.id_empreendimento == Empreendimento.id_empreendimento)
        .filter(Valores.mes_referencia == mes_ref)
        .order_by(Empreendimento.nome_empreendimento, Imovel.pavimento, Imovel.apartamento)

        .all()
    )

    df = pd.DataFrame(dados)

    df.columns = [
        "empreendimento",
        "construtora",
        "bairro",
        "endereco",
        "distancia_mar",
        "data_entrega",
        "qtd_elevadores",

        "piscina",
        "coworking",
        "lavanderia",
        "restaurante_bar",
        "academia",
        "pet_playground",
        "salao_festas",
        "sauna",
        "minimarket",

        "pavimento",
        "apartamento",
        "qtd_quartos",
        "posicao",
        "area_interna",
        "area_externa",
        "vagas",
        "bwc",

        "valor_total",
        "status",
        "mes_referencia"
    ]

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="dados")

    output.seek(0)

    nome = f"base_imoveis_{ano}_{mes:02d}.xlsx"

    return send_file(
        output,
        download_name=nome,
        as_attachment=True,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

