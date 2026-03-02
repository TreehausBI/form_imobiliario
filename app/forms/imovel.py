from flask_wtf import FlaskForm
from wtforms import (
    StringField, SelectField, IntegerField,
    BooleanField, DateField, SubmitField, FloatField
)
from wtforms.validators import DataRequired, Optional, Length

class ImovelForm(FlaskForm):
    empreendimento = SelectField(
        "Empreendimento",
        coerce=int,
        validators=[DataRequired()]
    )

    pavimento = IntegerField("Pavimento", validators=[Optional()])
    apartamento = StringField("Apartamento", validators=[DataRequired(), Length(max=20)])
    qtd_quartos = SelectField(
        "Quantidade de Quartos",
        choices=[
            ("Studio", "Studio"),
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),
            ("5", "5"),
            ("6", "6"),
            ("7", "7"),
            ("8+", "8+")
        ],
        validators=[DataRequired()]
    )

    posicao = SelectField(
        "Posição",
        coerce=int,
        validators=[DataRequired()]
    )

    area_interna = FloatField("Área Interna (m²)", validators=[Optional()])
    area_externa = FloatField("Área Externa (m²)", validators=[Optional()])
    vagas = SelectField(
        "Quantidade de Vagas",
        choices=[
            ("Rotativo", "Rotativo"),
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),
            ("5", "5"),
            ("6+", "6+")
        ],
        validators=[DataRequired()]
    )

    bwc = IntegerField("BWC", validators=[Optional()])
    unidades_por_pavimento = IntegerField("Unidades por Pavimento", validators=[Optional()])
    submit = SubmitField("Salvar Imóvel")