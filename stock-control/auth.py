from flask import Blueprint, request, redirect, render_template, url_for, flash
from .models import db, User, bcrypt, RegisterForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user

bp = Blueprint("auth", __name__, url_prefix='/auth')

# Página de login
@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('stock_control.index'))
    if request.method == 'POST':
        if form.validate_on_submit():
            email_address = form.email_address.data
            password = form.password.data
            user = db.session.execute(db.select(User).filter_by(email=email_address)).scalar_one_or_none()
            print(user)
            if user and bcrypt.check_password_hash(user.senha, password):
                login_user(user)
                return redirect(url_for('stock_control.index'))
        flash('Usuário ou senha inválidos', 'danger')
    return render_template('auth/login.html', form=form)

# Página de logout
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# Página de cadastro
@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    
    # Verifica se o usuário já está autenticado
    if current_user.is_authenticated:
        # Se o usuário já estiver autenticado, redireciona para a página inicial
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        if form.validate_on_submit():
            email_address = form.email_address.data
            name = form.name.data
            password = form.password.data

            # Verifica se o nome de usuário já existe
            if db.session.execute(db.select(User).filter_by(email=email_address)).scalar_one_or_none():
                flash('Email já cadastrado', 'danger')
                print('ja cadastrado')
                return redirect(url_for('auth.register'))

            # Criptografando a senha antes de salvar
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(email=email_address, senha=hashed_password, name=name)

            # Adicionando o novo usuário no banco de dados
            db.session.add(new_user)
            db.session.commit()

            flash('Cadastro realizado com sucesso, por favor faça login.', 'success')
            return redirect(url_for('auth.login'))
        flash('Erro ao cadastrar, por favor tente novamente', 'danger')

    return render_template('auth/register.html', form=form)