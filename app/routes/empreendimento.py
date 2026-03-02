from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms.empreendimento import EmpreendimentoForm
from app.models import Empreendimento, Construtora, Bairro, Equipamento, CondicaoPagamento, Imovel, Valores
from ..extensions import db

empreendimento_bp = Blueprint("empreendimento", __name__)

@empreendimento_bp.route("/empreendimento", methods=["GET", "POST"])
def cadastro_empreendimento():
    form = EmpreendimentoForm()

    form.construtora.choices = [("", "Selecione uma construtora")] + [
        (c.id_construtora, c.nome_construtora)
        for c in Construtora.query.order_by(Construtora.nome_construtora)
    ]

    form.bairro.choices = [
        (b.id_bairro, b.nome_bairro)
        for b in Bairro.query.order_by(Bairro.nome_bairro)
    ]

    if form.validate_on_submit():

        # 1️. Construtora
        if form.nova_construtora.data:
            nova = Construtora(
                nome_construtora=form.nova_construtora.data.strip(),
            )
            db.session.add(nova)
            db.session.flush()
            id_construtora = nova.id_construtora
        else:
            id_construtora = form.construtora.data

        # 2️. Empreendimento
        emp = Empreendimento(
            nome_empreendimento=form.nome_empreendimento.data,
            id_construtora=id_construtora,
            id_bairro=form.bairro.data,
            endereco=form.endereco.data,
            lote=form.lote.data,
            quadra=form.quadra.data,
            id_cartografica=form.id_cartografica.data,
            distancia_mar=form.distancia_mar.data,
            distancia_ao_empreendimento=form.distancia_ao_empreendimento.data,
            inicio_vendas=form.inicio_vendas.data,
            data_entrega=form.data_entrega.data,
            qtd_elevadores=form.qtd_elevadores.data,
            contato=form.contato.data
        )
        db.session.add(emp)
        db.session.flush()  # 🔑 gera emp.id_empreendimento

        # 3️. Equipamentos
        equip = Equipamento(
            id_empreendimento=emp.id_empreendimento,
            piscina=form.piscina.data,
            coworking=form.coworking.data,
            lavanderia=form.lavanderia.data,
            restaurante_bar=form.restaurante_bar.data,
            academia=form.academia.data,
            pet_playground=form.pet_playground.data,
            salao_festas=form.salao_festas.data,
            sauna=form.sauna.data,
            minimarket=form.minimarket.data
        )
        db.session.add(equip)

        # 4️. Condição de pagamento – Opção 1 (obrigatória)
        cond1 = CondicaoPagamento(
            id_empreendimento=emp.id_empreendimento,
            ordem=1,
            sinal=form.sinal_1.data,
            mensais=form.mensais_1.data,
            intercaladas=form.intercaladas_1.data,
            habite_se=form.habite_se_1.data
        )
        db.session.add(cond1)

        # 5️. Condição de pagamento – Opção 2 (opcional)
        if form.mensais_2.data:
            cond2 = CondicaoPagamento(
                id_empreendimento=emp.id_empreendimento,
                ordem=2,
                sinal=form.sinal_2.data,
                mensais=form.mensais_2.data,
                intercaladas=form.intercaladas_2.data,
                habite_se=form.habite_se_2.data
            )
            db.session.add(cond2)

        db.session.commit()

        flash("Empreendimento cadastrado com sucesso", "success")
        return redirect(url_for("empreendimento.cadastro_empreendimento"))
    
    print(form.errors)

    return render_template("empreendimento.html", form=form)


@empreendimento_bp.route("/empreendimentos")
def lista_empreendimentos():
    empreendimentos = (
        db.session.query(
            Empreendimento,
            db.func.count(Imovel.id_imovel).label("qtd_imoveis"),
            db.func.max(Valores.mes_referencia).label("ultimo_mes")
        )
        .select_from(Empreendimento)
        .outerjoin(
            Imovel,
            Imovel.id_empreendimento == Empreendimento.id_empreendimento
        )
        .outerjoin(
            Valores,
            Valores.id_imovel == Imovel.id_imovel
        )
        .group_by(Empreendimento.id_empreendimento)
        .order_by(Empreendimento.nome_empreendimento)
        .all()
    )

    return render_template(
        "empreendimento_view.html",
        empreendimentos=empreendimentos
    )

@empreendimento_bp.route("/empreendimentos/<int:id>/imoveis")
def imoveis_por_empreendimento(id):
    mes = request.args.get("mes")
    if mes:
        mes = date.fromisoformat(mes)

    empreendimento = Empreendimento.query.get_or_404(id)

    if mes:
        dados = (
            db.session.query(Imovel, Valores)
            .outerjoin(
                Valores,
                (Imovel.id_imovel == Valores.id_imovel) &
                (Valores.mes_referencia == mes)
            )
            .filter(Imovel.id_empreendimento == id)
            .all()
        )
    else:
        sub = (
            db.session.query(
                Valores.id_imovel,
                db.func.max(Valores.mes_referencia).label("max_mes")
            )
            .group_by(Valores.id_imovel)
            .subquery()
        )

        dados = (
            db.session.query(Imovel, Valores)
            .outerjoin(sub, Imovel.id_imovel == sub.c.id_imovel)
            .outerjoin(
                Valores,
                (Valores.id_imovel == sub.c.id_imovel) &
                (Valores.mes_referencia == sub.c.max_mes)
            )
            .filter(Imovel.id_empreendimento == id)
            .all()
        )

    return render_template(
        "empreendimento_view_imovel.html",
        empreendimento=empreendimento,
        dados=dados
    )

@empreendimento_bp.route("/empreendimentos/<int:id>/editar", methods=["GET", "POST"])
def editar_empreendimento(id):

    emp = Empreendimento.query.get_or_404(id)
    form = EmpreendimentoForm(obj=emp)

    # choices (igual no cadastro)
    form.construtora.choices = [("", "Selecione uma construtora")] + [
        (c.id_construtora, c.nome_construtora)
        for c in Construtora.query.order_by(Construtora.nome_construtora)
    ]

    form.bairro.choices = [
        (b.id_bairro, b.nome_bairro)
        for b in Bairro.query.order_by(Bairro.nome_bairro)
    ]

    # carregar equipamentos
    equip = Equipamento.query.filter_by(id_empreendimento=id).first()
    condicoes = CondicaoPagamento.query.filter_by(id_empreendimento=id).order_by(CondicaoPagamento.ordem).all()

    if request.method == "GET":
        if equip:
            form.piscina.data = equip.piscina
            form.coworking.data = equip.coworking
            form.lavanderia.data = equip.lavanderia
            form.restaurante_bar.data = equip.restaurante_bar
            form.academia.data = equip.academia
            form.pet_playground.data = equip.pet_playground
            form.salao_festas.data = equip.salao_festas
            form.sauna.data = equip.sauna
            form.minimarket.data = equip.minimarket

        if condicoes:
            c1 = condicoes[0]
            form.sinal_1.data = c1.sinal
            form.mensais_1.data = c1.mensais
            form.intercaladas_1.data = c1.intercaladas
            form.habite_se_1.data = c1.habite_se

            if len(condicoes) > 1:
                c2 = condicoes[1]
                form.sinal_2.data = c2.sinal
                form.mensais_2.data = c2.mensais
                form.intercaladas_2.data = c2.intercaladas
                form.habite_se_2.data = c2.habite_se

    if form.validate_on_submit():

        emp.nome_empreendimento = form.nome_empreendimento.data
        emp.id_construtora = form.construtora.data
        emp.id_bairro = form.bairro.data
        emp.endereco = form.endereco.data
        emp.lote = form.lote.data
        emp.quadra = form.quadra.data
        emp.id_cartografica = form.id_cartografica.data
        emp.distancia_mar = form.distancia_mar.data
        emp.distancia_ao_empreendimento = form.distancia_ao_empreendimento.data
        emp.inicio_vendas = form.inicio_vendas.data
        emp.data_entrega = form.data_entrega.data
        emp.qtd_elevadores = form.qtd_elevadores.data
        emp.contato = form.contato.data

        # atualizar equipamentos
        if equip:
            equip.piscina = form.piscina.data
            equip.coworking = form.coworking.data
            equip.lavanderia = form.lavanderia.data
            equip.restaurante_bar = form.restaurante_bar.data
            equip.academia = form.academia.data
            equip.pet_playground = form.pet_playground.data
            equip.salao_festas = form.salao_festas.data
            equip.sauna = form.sauna.data
            equip.minimarket = form.minimarket.data

        # atualizar condição 1
        if condicoes:
            condicoes[0].sinal = form.sinal_1.data
            condicoes[0].mensais = form.mensais_1.data
            condicoes[0].intercaladas = form.intercaladas_1.data
            condicoes[0].habite_se = form.habite_se_1.data

            if len(condicoes) > 1:
                condicoes[1].sinal = form.sinal_2.data
                condicoes[1].mensais = form.mensais_2.data
                condicoes[1].intercaladas = form.intercaladas_2.data
                condicoes[1].habite_se = form.habite_se_2.data

        db.session.commit()

        flash("Empreendimento atualizado com sucesso", "success")
        return redirect(url_for("empreendimento.lista_empreendimentos"))

    return render_template(
        "empreendimento.html",
        form=form,
        modo="editar"
    )



