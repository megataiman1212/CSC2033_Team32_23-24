from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/database')
def database():
    return render_template('database.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

