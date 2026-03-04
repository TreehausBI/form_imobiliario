from datetime import date
from sqlalchemy import func, and_
from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms.valores import ValoresImovelForm
from app.models import Imovel, Valores, Empreendimento, Construtora
from ..extensions import db

valores_bp = Blueprint("valores", __name__)

@valores_bp.route("/valores/<int:id_imovel>", methods=["GET", "POST"])
def atualizar_valor(id_imovel):

    imovel = Imovel.query.get_or_404(id_imovel)
    form = ValoresImovelForm()

    # status dinâmico
    status_db = {s for (s,) in db.session.query(Valores.status).distinct() if s}
    if not status_db:
        status_db = {"Disponível"}

    form.status.choices = [(s, s) for s in sorted(status_db)]

    if form.validate_on_submit():

        mes = form.mes_referencia.data.replace(day=1)

        valor_existente = Valores.query.filter_by(
            id_imovel=id_imovel,
            mes_referencia=mes
        ).first()

        if valor_existente:
            valor_existente.valor_total = form.valor_total.data
            valor_existente.status = form.status.data
        else:
            novo = Valores(
                id_imovel=id_imovel,
                mes_referencia=mes,
                valor_total=form.valor_total.data,
                status=form.status.data
            )
            db.session.add(novo)

        print("Mes no banco:", valor_existente)
        print("Mes enviado:", mes)

        db.session.commit()

        flash("Valor atualizado com sucesso", "success")

        # Redireciona para a própria página de valores
        return redirect(url_for("valores.atualizar_valor", id_imovel=id_imovel))

    # AQUI ESTÁ O QUE FALTAVA
    historico = (
        Valores.query
        .filter_by(id_imovel=id_imovel)
        .order_by(Valores.mes_referencia.desc())
        .all()
    )

    return render_template(
        "valores.html",
        form=form,
        imovel=imovel,
        historico=historico
    )

@valores_bp.route("/valores/pendencias")
def pendencias_mes():

    inicio_mes = date.today().replace(day=1)
    pendentes = []

    # 🔥 Carrega tudo em uma tacada só
    empreendimentos = (
        Empreendimento.query
        .options(
            joinedload(Empreendimento.imoveis)
            .joinedload(Imovel.valores)
        )
        .all()
    )

    for emp in empreendimentos:

        precisa_atualizar = False
        ultima_data_emp = None

        for imovel in emp.imoveis:

            if not imovel.valores:
                precisa_atualizar = True
                break

            # pega último valor em memória
            ultimo_valor = max(
                imovel.valores,
                key=lambda v: v.mes_referencia
            )

            if not ultima_data_emp or ultimo_valor.mes_referencia > ultima_data_emp:
                ultima_data_emp = ultimo_valor.mes_referencia

            if ultimo_valor.status in ["Lançamento", "Disponível"]:
                if ultimo_valor.mes_referencia < inicio_mes:
                    precisa_atualizar = True
                    break

        if precisa_atualizar:
            pendentes.append({
                "nome_empreendimento": emp.nome_empreendimento,
                "nome_construtora": emp.construtora.nome_construtora,
                "ultima_atualizacao": ultima_data_emp
            })

    return render_template(
        "pendencias.html",
        pendentes=pendentes,
        mes=inicio_mes
    )

@valores_bp.route("/valores/<int:id>/editar", methods=["GET", "POST"])
def editar_valor(id):

    valor = Valores.query.get_or_404(id)
    form = ValoresImovelForm(obj=valor)

    status_db = {s for (s,) in db.session.query(Valores.status).distinct() if s}
    if not status_db:
        status_db = {"Disponível"}

    form.status.choices = [(s, s) for s in sorted(status_db)]

    if form.validate_on_submit():

        valor.mes_referencia = form.mes_referencia.data.replace(day=1)
        valor.valor_total = form.valor_total.data
        valor.status = form.status.data

        db.session.commit()

        flash("Valor atualizado com sucesso", "success")

        return redirect(
            url_for("valores.atualizar_valor", id_imovel=valor.id_imovel)
        )
    imovel = valor.imovel

    historico = (
        Valores.query
        .filter_by(id_imovel=valor.id_imovel)
        .order_by(Valores.mes_referencia.desc())
        .all()
    )

    return render_template(
        "valores.html",
        form=form,
        imovel=imovel,
        historico=historico,
        modo="editar"
    )





