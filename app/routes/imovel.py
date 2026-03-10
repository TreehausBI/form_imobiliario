from flask import Blueprint, render_template, render_template, redirect, url_for, flash, request
from app.forms.imovel import ImovelForm
from app.models import Imovel, Empreendimento, Posicao, Valores
from ..extensions import db
from datetime import date
from decimal import Decimal

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

@imovel_bp.route("/imoveis/acao_lote", methods=["POST"])
def acao_em_lote():

    acao = request.form.get("acao")

    vendidos = request.form.getlist("vendidos")
    replicar = request.form.getlist("replicar")
    emp_id = int(request.form.get("empreendimento_id"))
    inicio_mes = date.today().replace(day=1)

    # AUMENTO EM TODOS
    if acao == "aumento":

        aumento = request.form.get("aumento_percentual")

        if aumento:
            aumento = Decimal(aumento) / Decimal(100)

            imoveis = Imovel.query.filter_by(
                id_empreendimento=emp_id
            ).all()

            for imovel in imoveis:

                ultimo = (
                    Valores.query
                    .filter_by(id_imovel=imovel.id_imovel)
                    .order_by(Valores.mes_referencia.desc())
                    .first()
                )

                if not ultimo:
                    continue

                novo_valor = ultimo.valor_total * (1 + aumento)

                existe = Valores.query.filter_by(
                    id_imovel=imovel.id_imovel,
                    mes_referencia=inicio_mes
                ).first()

                if existe:
                    existe.valor_total = novo_valor
                else:
                    novo = Valores(
                        id_imovel=imovel.id_imovel,
                        mes_referencia=inicio_mes,
                        valor_total=novo_valor,
                        status=ultimo.status
                    )
                    db.session.add(novo)

    # SALVAR ALTERAÇÕES
    if acao == "salvar":

        # MARCAR VENDIDOS
        for id in vendidos:
            id = int(id)

            existe = Valores.query.filter_by(
                id_imovel=id,
                mes_referencia=inicio_mes
            ).first()

            if existe:
                existe.valor_total = 0
                existe.status = "Vendida"
            else:
                novo = Valores(
                    id_imovel=id,
                    mes_referencia=inicio_mes,
                    valor_total=0,
                    status="Vendida"
                )
                db.session.add(novo)

        # REPLICAR MES
        for id in replicar:
            id = int(id)

            existe = Valores.query.filter_by(
                id_imovel=id,
                mes_referencia=inicio_mes
            ).first()

            if existe:
                continue

            ultimo = (
                Valores.query
                .filter_by(id_imovel=id)
                .order_by(Valores.mes_referencia.desc())
                .first()
            )

            if ultimo:
                novo = Valores(
                    id_imovel=id,
                    mes_referencia=inicio_mes,
                    valor_total=ultimo.valor_total,
                    status=ultimo.status
                )
                db.session.add(novo)

        # NOVOS VALORES/STATUS
        for key in request.form:
            if key.startswith("novo_valor_"):

                id_imovel = int(key.replace("novo_valor_", ""))

                valor = request.form.get(key)
                status = request.form.get(f"novo_status_{id_imovel}")

                if valor or status:

                    existe = Valores.query.filter_by(
                        id_imovel=id_imovel,
                        mes_referencia=inicio_mes
                    ).first()

                    if existe:
                        if valor:
                            existe.valor_total = valor
                        if status:
                            existe.status = status
                    else:
                        novo = Valores(
                            id_imovel=id_imovel,
                            mes_referencia=inicio_mes,
                            valor_total=valor if valor else None,
                            status=status if status else None
                        )
                        db.session.add(novo)

    db.session.commit()

    flash("Atualização realizada com sucesso.", "success")

    return redirect(request.referrer)
