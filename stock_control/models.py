from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_login import UserMixin
from typing import List

#Flask-SQLAlchemy
class Base(DeclarativeBase):
  pass

class User(UserMixin, Base):
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

class Product(Base):
    ''' Classe que representa um produto no sistema '''
    __tablename__ = 'products_table'  # Nome da tabela
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String(50))
    quantity: Mapped[int]
    price: Mapped[float]

    # Mapeia usuario que criou o produto
    user: Mapped["User"] = relationship(back_populates="products")
    user_id: Mapped[int] = mapped_column(ForeignKey("users_table.id"))

