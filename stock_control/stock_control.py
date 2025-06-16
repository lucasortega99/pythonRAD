from flask import Blueprint, request, redirect, render_template, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import select

from .models import User, Product
from .forms import ProductsForm
from .extensions import db

bp = Blueprint("stock_control", __name__, url_prefix='/stock_control')

# Página inicial
@bp.route('/')
@login_required
def index():
    return render_template('stock_control/index.html')

@bp.route('/stock', methods=['GET', 'POST'])
@login_required
def stock():
    stmt = select(Product).where(Product.user_id == current_user.id)
    products = db.session.scalars(stmt).all()
    data = {"products": products}
    print(data)
    form = ProductsForm(data=data)
    return render_template('stock_control/stock.html', form=form)

@bp.route('/save_product', methods=['POST'])
@login_required
def save_product():
    product_added = False
    product_updated = False
    stmt = select(Product).where(Product.user_id == current_user.id)
    products = db.session.scalars(stmt).all()
    data = {"products": products}
    form = ProductsForm(data=data)

    if form.validate_on_submit():
        for user_product in form.products:
            if user_product.form.id.data:
                stmt = select(Product).where(Product.id == user_product.form.id.data)
                up = db.session.execute(stmt).scalar()

                up.product_name = user_product.product_name.data
                up.quantity = user_product.quantity.data
                up.price = user_product.price.data
                product_updated = True

            else:
                up = Product(
                    product_name=user_product.product_name.data,
                    quantity=user_product.quantity.data,
                    price=user_product.price.data,
                    user_id=current_user.id
                )
                product_added = True

                db.session.add(up)

        db.session.commit()

        stmt = select(Product).where(Product.user_id == current_user.id)
        products = db.session.scalars(stmt).all()
        data = {"products": products}
        form = ProductsForm(data=data)

        return render_template("stock_control/products_form.html", form=form, product_added=product_added, product_updated=product_updated)

    else:
        print('Error1')
        print(form.errors)

@bp.route('/add_product')
@login_required
def add_product():
    stmt = select(Product).where(Product.user_id == current_user.id)
    products = db.session.scalars(stmt).all()
    data = {"products": products}
    form = ProductsForm(data=data)
    print(data)
    form.products.append_entry()
    return render_template("stock_control/products_form.html", form=form)

@bp.route('/delete_product/<int:id>', methods=["DELETE", "POST"])
@login_required
def delete_product(id=None):
    print("Deleting product with id:", id)
    if id:
        stmt = select(Product).where(Product.id == id)
        up = db.session.execute(stmt).scalar()
        db.session.delete(up)
        db.session.commit()
        print("Product deleted")

    stmt = select(Product).where(Product.user_id == current_user.id)
    products = db.session.scalars(stmt).all()
    data = {"products": products}
    form = ProductsForm(data=data)

    return render_template("stock_control/products_form.html", form=form, product_deleted=True)

@bp.route('/category', methods=['GET', 'POST'])
@login_required
def category():

    flash("This feature is not implemented yet.", "info")
    return redirect(url_for('stock_control.index'))

