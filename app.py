from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)





@app.route('/')
def index():
    return render_template('main/index.html')

# import blueprints
from admin.views import admin_blueprint
from database.views import database_blueprint
from users.views import users_blueprint

# register blueprints with app
app.register_blueprint(admin_blueprint)
app.register_blueprint(database_blueprint)
app.register_blueprint(users_blueprint)


if __name__ == "__main__":
    app.run()