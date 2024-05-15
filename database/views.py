from flask import Blueprint, render_template, request, redirect
from database.forms import SearchForm
import databaseControl
from flask import Blueprint, render_template
from flask_login import login_required, current_user

database_blueprint = Blueprint('database', __name__, template_folder='templates')


@database_blueprint.route('/database')
def database():
    return render_template("database/database.html")


@database_blueprint.route('/query')
def query():
    search_string = request.args.get("search_string")

    if search_string:
        results = databaseControl.query_products(search_string)
    else:

        results = []

    return render_template("database/query_results.html", results=results)


@database_blueprint.route('/<int:product_id>/<int:mode>/adjust_stock')
def adjust_stock(product_id, mode):
    databaseControl.adjust_stock(product_id, mode)
    search_string = request.args.get("search_string")

    if search_string:
        results = databaseControl.query_products(search_string)
    else:

        results = []

    return render_template("database/database.html", results=results)

@database_blueprint.route('/database', methods=['GET', 'POST'])
@login_required
def database():
    return render_template('database/database.html')