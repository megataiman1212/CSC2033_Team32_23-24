from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

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
    return render_template('users/login.html')

@app.route('/database')
def database():
    return render_template('database/database.html')

@app.route('/admin')
def admin():
    return render_template('admin/admin.html')


if __name__ == "__main__":
    app.run()