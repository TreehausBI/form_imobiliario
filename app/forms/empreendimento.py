from flask_wtf import FlaskForm
from wtforms import (
    StringField, SelectField, IntegerField, DateField, SubmitField, FloatField
)
from wtforms.validators import DataRequired, Optional, Length, NumberRange

class EmpreendimentoForm(FlaskForm):
    nome_empreendimento = StringField(
        "Nome do Empreendimento",
        validators=[DataRequired(), Length(max=150)]
    )

    construtora = SelectField(
        "Construtora",
        coerce=lambda x: int(x) if x else None,
        validators=[Optional()]
    )

    nova_construtora = StringField("Nova construtora", validators=[Optional()])
    bairro = SelectField("Bairro", coerce=int, validators=[DataRequired()])
    endereco = StringField("Endereço", validators=[Optional()])
    lote = IntegerField("Lote", validators=[Optional()])
    quadra = IntegerField("Quadra", validators=[Optional()])
    id_cartografica = IntegerField("Identificação Cartográfica", validators=[Optional()])
    distancia_mar = FloatField("Distância ao Mar (m)", validators=[Optional()])
    distancia_ao_empreendimento = FloatField("Distância ao Empreendimento (m)", validators=[Optional()])
    inicio_vendas = DateField("Início das Vendas", validators=[Optional()])
    data_entrega = DateField("Data da Entrega", validators=[Optional()])
    qtd_elevadores = IntegerField("Quantidade de Elevadores", validators=[Optional()])
    contato = StringField("Contato", validators=[Optional(), Length(max=255)])

    # Equipamentos
    piscina = IntegerField("Piscinas", default=0, validators=[Optional(), NumberRange(min=0)])
    coworking = IntegerField("Coworkings", default=0, validators=[Optional(), NumberRange(min=0)])
    lavanderia = IntegerField("Lavanderias", default=0, validators=[Optional(), NumberRange(min=0)])
    restaurante_bar = IntegerField("Restaurante / Bar", default=0, validators=[Optional(), NumberRange(min=0)])
    academia = IntegerField("Academia", default=0, validators=[Optional(), NumberRange(min=0)])
    pet_playground = IntegerField("Pet / Playground", default=0, validators=[Optional(), NumberRange(min=0)])
    salao_festas = IntegerField("Salão de Festas", default=0, validators=[Optional(), NumberRange(min=0)])
    sauna = IntegerField("Sauna", default=0, validators=[Optional(), NumberRange(min=0)])
    minimarket = IntegerField("Mini Market", default=0, validators=[Optional(), NumberRange(min=0)])

    # Condicao Pagamento
    # Condição 1 (obrigatória)
    sinal_1 = StringField("Sinal - Opção 1 (%)", validators=[Optional()])
    mensais_1 = StringField("Mensais - Opção 1", validators=[DataRequired()])
    intercaladas_1 = StringField("Intercaladas - Opção 1", validators=[DataRequired()])
    habite_se_1 = StringField("Habite-se - Opção 1 (%)", validators=[Optional()])

    # Condição 2 (opcional)
    sinal_2 = StringField("Sinal - Opção 2 (%)", validators=[Optional()])
    mensais_2 = StringField("Mensais - Opção 2", validators=[Optional()])
    intercaladas_2 = StringField("Intercaladas - Opção 2", validators=[Optional()])
    habite_se_2 = StringField("Habite-se - Opção 2 (%)", validators=[Optional()])

    submit = SubmitField("Salvar Empreendimento")

    def validate(self, extra_validators=None):
        if not super().validate(extra_validators):
            return False

        construtora_val = self.construtora.data
        nova_val = self.nova_construtora.data.strip() if self.nova_construtora.data else None

        if not construtora_val and not nova_val:
            self.construtora.errors.append(
                "Selecione uma construtora ou cadastre uma nova."
            )
            return False

        return True


        return True