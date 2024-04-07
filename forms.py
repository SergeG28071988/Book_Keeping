from flask_wtf import FlaskForm
from wtforms import StringField, DateField, DecimalField, SubmitField
from wtforms.validators import DataRequired

class BookForm(FlaskForm):
    author = StringField('Автор', validators=[DataRequired()])
    title = StringField('Название', validators=[DataRequired()])
    genre = StringField('Жанр', validators=[DataRequired()])
    date_received = DateField('Дата поступления', format='%Y-%m-%d', validators=[DataRequired()])
    price = DecimalField('Цена', validators=[DataRequired()])

