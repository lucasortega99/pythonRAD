from flask import Blueprint, request, redirect, render_template, url_for, flash
from .models import User, db, ProductForm, Product
from flask_login import login_required, current_user

bp = Blueprint("stock_control", __name__, url_prefix='/stock_control')


# Página inicial
@bp.route('/')
@login_required
def index():
    return render_template('stock_control/index.html')

@bp.route('/stock', methods=['GET', 'POST'])
@login_required
def stock():
    form = ProductForm()
    if form.validate_on_submit():
        new_product = Product(
            name=form.name.data,
            quantity=form.quantity.data,
            price=form.price.data,
            user_id=current_user.id
        )
        db.session.add(new_product)
        db.session.commit()
        flash('Produto adicionado com sucesso!', 'success')
        return redirect(url_for('stock_control.stock'))
    stock = db.session.execute(db.select(Product).filter_by(user_id=current_user.id)).scalars().all()
    print(stock)
    return render_template('stock_control/stock.html', form=form, stock=stock)