from flask import Blueprint, render_template, request, redirect
from database.forms import SearchForm
import databaseControl

database_blueprint = Blueprint('database', __name__, template_folder='templates')


@database_blueprint.route('/database', methods=['GET', 'POST'])
def database():
    products = databaseControl.get_all_products()

    return render_template('database/database.html', products=products)


@database_blueprint.route('/database.query', methods=['GET', 'POST'])
def query():
    form = SearchForm()

    if form.validate_on_submit():
        search_string = form.search.data

        products = databaseControl.query_products(search_string)

        render_template('database/database.html', products=products)

    # if string is invalid, full table is displayed
    return database()
