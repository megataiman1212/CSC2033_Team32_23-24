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

# Initialise login manager
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    from models import User
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

# error 400 bad request handling
@app.errorhandler(400)
def bad_request_error(error):
    return render_template('Error400.html', error_code = 400, error_name = 'Bad Request'), 400

# error 403 forbidden handling
@app.errorhandler(403)
def forbidden_error(error):
    return render_template('Error403.html', error_code = 403, error_name = 'Forbidden'), 403

# error 404 not found handling
@app.errorhandler(404)
def not_found_error(error):
    return render_template('Error404.html', error_code = 404, error_name = 'Not Found'), 404

# error 500 internal server handling
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('Error500.html', error_code = 500, error_name = 'Internal Server Error'), 500

if __name__ == "__main__":
    app.run()
