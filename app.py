from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from users.forms import LoginForm



app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRETKEY'

csrf = CSRFProtect(app)

#Connect to MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Team32@localhost/Inventory'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Initalise login manager
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.init_app(app)

from models import User
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def index():
    return render_template('main/index.html')
@app.route('/login')
def login():
    form = LoginForm()
    return render_template('users/login.html', form = LoginForm())

@app.route('/database')
def database():
    return render_template('database/database.html')

@app.route('/admin')
def admin():
    return render_template('admin/admin.html')


from users.views import users_blueprint
from admin.views import admin_blueprint
from database.views import database_blueprint

app.register_blueprint(users_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint((database_blueprint))

if __name__ == "__main__":
    app.run()
