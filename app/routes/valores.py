from datetime import date
from sqlalchemy import func
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

        db.session.commit()

        flash("Valor atualizado com sucesso", "success")

        # 🔥 Redireciona para a própria página de valores
        return redirect(url_for("valores.atualizar_valor", id_imovel=id_imovel))

    # ✅ AQUI ESTÁ O QUE FALTAVA
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

    pendentes = (
        db.session.query(
            Empreendimento.id_empreendimento,
            Empreendimento.nome_empreendimento,
            Construtora.nome_construtora,
            func.count(Imovel.id_imovel).label("qtd_imoveis"),
            func.max(Valores.mes_referencia).label("ultima_atualizacao")
        )
        .join(Construtora)
        .join(Imovel)
        .outerjoin(Valores)
        .group_by(
            Empreendimento.id_empreendimento,
            Empreendimento.nome_empreendimento,
            Construtora.nome_construtora
        )
        .having(
            func.coalesce(func.max(Valores.mes_referencia), date(1900, 1, 1))
            < inicio_mes
        )
        .order_by(Empreendimento.nome_empreendimento)
        .all()
    )

    return render_template(
        "pendencias.html",   # <-- nome do seu novo html
        pendentes=pendentes,
        mes=inicio_mes
    )

@valores_bp.route("/valores/<int:id>/editar", methods=["GET", "POST"])
def editar_valor(id):

    valor = Valores.query.get_or_404(id)
    form = ValoresImovelForm(obj=valor)

    status_db = {s for (s,) in db.session.query(Valores.status).distinct() if s}
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





