from flask_wtf import FlaskForm
from wtforms import (
    StringField, SelectField, IntegerField,
    BooleanField, DateField, SubmitField, DecimalField
)
from wtforms.validators import DataRequired, Optional, Length, InputRequired

class ValoresImovelForm(FlaskForm):

    mes_referencia = DateField(
        "Mês de Referência",
        format="%Y-%m-%d",
        validators=[DataRequired()]
    )

    valor_total = DecimalField(
        "Valor Total (R$)",
        places=2,
        validators=[InputRequired()]
    )

    status = SelectField(
        "Status",
        validators=[DataRequired()]
    )

    submit = SubmitField("Registrar Valor")