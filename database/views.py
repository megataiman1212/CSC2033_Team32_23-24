from flask import request
from Database_Manager.db_crud import DbManager
from flask import Blueprint, render_template
from flask_login import login_required
from database.forms import ProductForm

database_blueprint = Blueprint('database', __name__, template_folder='templates')


@database_blueprint.route('/database', methods=['GET', 'POST'])
@login_required
def database():
    return render_template('database/database.html')


@database_blueprint.route('/query', methods=['GET', 'POST'])
def query():
    search_string = request.args.get("search_string")

    if search_string:
        results = DbManager.query_products(search_string)
    else:

        results = []

    return render_template("database/query_results.html", results=results)


@database_blueprint.route('/<int:product_id>/<int:mode>/adjust_stock', methods=['GET', 'POST'])
def adjust_stock(product_id, mode):
    Db = DbManager()
    Db.adjust_stock(product_id, mode)

    search_string = request.args.get("search_string")

    if search_string:
        results = DbManager.query_products(search_string)
    else:

        results = []

    return render_template("database/database.html", results=results)


@database_blueprint.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()

    if form.validate_on_submit():
        Db = DbManager()
        Db.add_product(form.name.data,
                       form.stock.data,
                       form.category.data,
                       form.required_stock.data)
        return render_template("database/database.html")

    return render_template('database/add_product.html', form=form)


@database_blueprint.route('/<int:product_id>/delete_product', methods=['GET', 'POST'])
def delete_product(product_id):
    Db = DbManager()
    Db.delete_product(product_id)

    search_string = request.args.get("search_string")

    if search_string:
        results = DbManager.query_products(search_string)

    else:
        results = []

    return render_template("database/database.html", results=results)

