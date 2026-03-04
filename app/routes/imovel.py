from flask import Blueprint, render_template, render_template, redirect, url_for, flash
from app.forms.imovel import ImovelForm
from app.models import Imovel, Empreendimento, Posicao, Valores
from ..extensions import db
from datetime import date

imovel_bp = Blueprint("imovel", __name__)

@imovel_bp.route("/imovel", methods=["GET", "POST"])
def cadastro_imovel():
    form = ImovelForm()

    form.empreendimento.choices = [
        (e.id_empreendimento, e.nome_empreendimento)
        for e in Empreendimento.query.order_by(Empreendimento.nome_empreendimento)
    ]

    form.posicao.choices = [
        (p.id_posicao, p.nome_posicao)
        for p in Posicao.query.order_by(Posicao.nome_posicao)
    ]

    if form.validate_on_submit():
        imovel = Imovel(
            id_empreendimento=form.empreendimento.data,
            apartamento=form.apartamento.data,
            pavimento=form.pavimento.data,
            qtd_quartos=form.qtd_quartos.data,
            id_posicao=form.posicao.data,
            area_interna=form.area_interna.data,
            area_externa=form.area_externa.data,
            vagas=form.vagas.data,
            bwc=form.bwc.data,
            unidades_por_pavimento=form.unidades_por_pavimento.data
        )
        db.session.add(imovel)
        db.session.commit()

        flash("Imóvel cadastrado com sucesso", "success")
        return redirect(url_for("imovel.cadastro_imovel"))

    return render_template("imovel.html", form=form)

@imovel_bp.route("/imoveis/<int:id>/editar", methods=["GET", "POST"])
def editar_imovel(id):

    imovel = Imovel.query.get_or_404(id)
    form = ImovelForm(obj=imovel)

    # preencher choices (igual cadastro)
    form.empreendimento.choices = [
        (e.id_empreendimento, e.nome_empreendimento)
        for e in Empreendimento.query.order_by(Empreendimento.nome_empreendimento)
    ]

    form.posicao.choices = [
        (p.id_posicao, p.nome_posicao)
        for p in Posicao.query.order_by(Posicao.nome_posicao)
    ]

    if form.validate_on_submit():

        imovel.id_empreendimento = form.empreendimento.data
        imovel.apartamento = form.apartamento.data
        imovel.pavimento = form.pavimento.data
        imovel.qtd_quartos = form.qtd_quartos.data
        imovel.id_posicao = form.posicao.data
        imovel.area_interna = form.area_interna.data
        imovel.area_externa = form.area_externa.data
        imovel.vagas = form.vagas.data
        imovel.bwc = form.bwc.data
        imovel.unidades_por_pavimento = form.unidades_por_pavimento.data

        db.session.commit()

        flash("Imóvel atualizado com sucesso", "success")

        return redirect(
            url_for(
                "empreendimento.imoveis_por_empreendimento",
                id=imovel.id_empreendimento
            )
        )

    return render_template(
        "imovel.html",
        form=form,
        modo="editar"
    )

@imovel_bp.route("/imovel/<int:id>/vendido")
def marcar_imovel_vendido(id):

    imovel = Imovel.query.get_or_404(id)
    inicio_mes = date.today().replace(day=1)

    # verifica se já existe valor no mês atual
    valor_mes = Valores.query.filter_by(
        id_imovel=id,
        mes_referencia=inicio_mes
    ).first()

    if not valor_mes:
        novo = Valores(
            id_imovel=id,
            mes_referencia=inicio_mes,
            valor_total=0,
            status="Vendida"
        )
        db.session.add(novo)
    else:
        valor_mes.valor_total = 0
        valor_mes.status = "Vendida"

    db.session.commit()

    flash("Imóvel marcado como vendido no mês atual.", "success")

    return redirect(
        url_for(
            "empreendimento.imoveis_por_empreendimento",
            id=imovel.id_empreendimento
        )
    )
