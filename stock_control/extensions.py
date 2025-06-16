from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf import CSRFProtect

from .models import User

db = SQLAlchemy()

#Flask-Login
login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one_or_none()

#Flask-Bcrypt
bcrypt = Bcrypt()

# CSRF protection
csrf = CSRFProtect()

