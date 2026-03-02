from flask_wtf import FlaskForm
from wtforms import (
    StringField, SelectField, IntegerField,
    BooleanField, DateField, SubmitField, FloatField
)
from wtforms.validators import DataRequired, Optional, Length

class ValoresImovelForm(FlaskForm):

    mes_referencia = DateField(
        "Mês de Referência",
        format="%Y-%m-%d",
        validators=[DataRequired()]
    )

    valor_total = FloatField("Valor Total (R$)", validators=[DataRequired()])
    status = SelectField(
        "Status",
        validators=[DataRequired()]
    )

    submit = SubmitField("Registrar Valor")