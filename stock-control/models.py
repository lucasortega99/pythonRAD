from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_login import UserMixin, LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, IntegerField, DecimalField, SelectField
from wtforms.validators import InputRequired, Email, EqualTo, NumberRange
from typing import List


#Flask-SQLAlchemy
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class User(UserMixin, db.Model):
    ''' Classe que representa um usuário no sistema '''
    __tablename__ = 'users_table'  # Nome da tabela
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(unique=True)
    senha: Mapped[str]
    name: Mapped[str]
    
    # Lista de produtos associados a este usuário
    products: Mapped[List["Product"]] = relationship(back_populates="user")
    
    def __repr__(self):
        return f'Users(id: {self.id}, email: {self.email})'

class Product(db.Model):
    ''' Classe que representa um produto no sistema '''
    __tablename__ = 'products_table'  # Nome da tabela
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    quantity: Mapped[int]
    price: Mapped[float]
    
    # Mapeia usuario que criou o produto
    user: Mapped["User"] = relationship(back_populates="products")
    user_id: Mapped[int] = mapped_column(ForeignKey("users_table.id"))
    
#Flask-Login
login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one_or_none()
  
#Flask-Bcrypt
bcrypt = Bcrypt()

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
    name = StringField('Nome do Produto', validators=[InputRequired()])
    quantity = IntegerField('Quantidade', validators=[InputRequired(), NumberRange(min=1)])
    price = DecimalField('Preço (R$)', validators=[InputRequired(), NumberRange(min=0.01)])
    submit = SubmitField('Adicionar Produto')
