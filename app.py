from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from users.forms import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRETKEY'

csrf = CSRFProtect(app)

#Connect to MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Team32@localhost/Inventory'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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


if __name__ == "__main__":
    app.run()
