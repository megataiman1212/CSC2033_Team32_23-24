from flask import request, flash, redirect, url_for
from Database_Manager.db_crud import DbManager
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from database.forms import ProductForm, RequiredStockForm

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
        db = DbManager()
        results = db.get_all_products()

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


@database_blueprint.route('/<int:product_id>/<int:current_level>/change_reorder_level', methods=['GET', 'POST'])
def change_reorder_level(product_id, current_level):
    if current_user.access_level != 'admin':
        flash("You do not have permission to register a new admin!")
        return redirect(url_for('admin.admin'))
    form = RequiredStockForm()

    if form.validate_on_submit():
        Db = DbManager()
        Db.change_stock_required_level(product_id, form.new_level.data)
        return render_template("database/database.html")

    return render_template('database/change_reorder_level.html', form=form, current_level=current_level)


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
    if current_user.access_level != 'admin':
        flash("You do not have permission to register a new admin!")
        return redirect(url_for('admin.admin'))
    Db = DbManager()
    Db.delete_product(product_id)

    search_string = request.args.get("search_string")

    if search_string:
        results = DbManager.query_products(search_string)

    else:
        results = []

    return render_template("database/database.html", results=results)

