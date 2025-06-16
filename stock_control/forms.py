from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, IntegerField, DecimalField, HiddenField, FieldList, FormField
from wtforms.validators import InputRequired, Email, EqualTo, NumberRange

#Forms do flask-wtf
class LoginForm(FlaskForm):
    email_address = EmailField('Email', validators=[InputRequired(), Email("Por favor insira um email válido")])
    password = PasswordField('Senha', validators=[InputRequired()])
    submit = SubmitField('Logar')

class RegisterForm(FlaskForm):
    email_address = EmailField('Endereco de email', validators=[InputRequired('Por favor insira um email.'), Email("Por favor insira um email válido")])
    password = PasswordField('Senha', validators=[InputRequired(), EqualTo('password_confirmation', message='As senhas não coincidem')])
    password_confirmation = PasswordField('Confirme a senha', validators=[InputRequired()])
    name = StringField('Nome', validators=[InputRequired()])
    submit = SubmitField('Submeter')

class ProductForm(FlaskForm):
    id = HiddenField('id')
    product_name = StringField('Nome do Produto', validators=[InputRequired()])
    quantity = IntegerField('Quantidade', validators=[InputRequired(), NumberRange(min=1)])
    price = DecimalField('Preço (R$)', validators=[InputRequired(), NumberRange(min=0)])

class ProductsForm(FlaskForm):
    products = FieldList(FormField(ProductForm), min_entries=1)