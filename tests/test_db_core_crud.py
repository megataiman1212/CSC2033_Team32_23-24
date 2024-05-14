def add_products(db_instance_empty, session,stocked_food_product, unstocked_food_product):
    # Adds the two pre-made products to a temporary session in the db
    db_instance_empty.create_product(product=stocked_food_product, session=session)
    db_instance_empty.create_product(product=unstocked_food_product, session=session)


def test_get_required_stock(db_instance_empty, session, stocked_food_product, unstocked_food_product):

    add_products(db_instance_empty, session, stocked_food_product, unstocked_food_product)
    test_stock = db_instance_empty.get_required_stock()

    #check list is only one item (as only one fits paramater
    assert len(test_stock) == 1
    assert test_stock[0].product ==  unstocked_food_product.product

def test_get_all_product(db_instance_empty, session, stocked_food_product, unstocked_food_product):
    add_products(db_instance_empty, session, stocked_food_product, unstocked_food_product)

    test_product = db_instance_empty.get_all_products()

    #checls list is length 2 and has both products
    assert len(test_product) == 2
    assert test_product[0].product == stocked_food_product.product
    assert test_product[1].product == unstocked_food_product.product


# Tests by adding a product and then searching for it
def test_query_products(db_instance_empty, session, stocked_food_product, unstocked_food_product):

    add_products(db_instance_empty, session, stocked_food_product, unstocked_food_product)

    # Runs the query_product function and stores result in a list
    test_stocked_food_product = db_instance_empty.query_products(search_string=stocked_food_product.product)
    test_unstocked_food_product = db_instance_empty.query_products(search_string=unstocked_food_product.product)

    # Checks the found items match the added items (probably only need to check one
    assert test_stocked_food_product[0].stock == stocked_food_product.stock
    assert test_stocked_food_product[0].product == stocked_food_product.product
    assert test_stocked_food_product[0].category == stocked_food_product.category
    assert test_stocked_food_product[0].required_level == stocked_food_product.required_level
    assert test_stocked_food_product[0].product_id == stocked_food_product.product_id
    assert test_unstocked_food_product[0].product == unstocked_food_product.product

def test_adjust_stock(db_instance_empty, session, stocked_food_product, unstocked_food_product):
    add_products(db_instance_empty, session, stocked_food_product, unstocked_food_product)

    # increase stock
    db_instance_empty.adjust_stock(session=session, product_id=stocked_food_product.product_id, mode=True)
    db_instance_empty.adjust_stock(session=session, product_id=unstocked_food_product.product_id, mode=False)

    # searches for stocks
    increase_stock = db_instance_empty.query_products(search_string=stocked_food_product.product)
    decrease_stock = db_instance_empty.query_products(search_string=unstocked_food_product.product)

    # check increased has increased stock by one
    assert increase_stock[0].stock == (stocked_food_product.stock + 1)
    assert decrease_stock[0].stock == (unstocked_food_product.stock - 1)


def test_change_stock_level(db_instance_empty, session, stocked_food_product, unstocked_food_product):
    add_products(db_instance_empty, session, stocked_food_product, unstocked_food_product)

    # Change order level
    db_instance_empty.change_stock_level(session=session, product_id=stocked_food_product.product_id, new_stock=100)

    # searches for stocks
    change_stock = db_instance_empty.query_products(search_string=stocked_food_product.product)
    same_stock = db_instance_empty.query_products(search_string=unstocked_food_product.product)

    # Check order level as changed
    assert change_stock[0].stock == 100
    assert same_stock[0].stock == unstocked_food_product.stock


def test_delete_product(db_instance_empty, session, stocked_food_product, unstocked_food_product):
    add_products(db_instance_empty, session, stocked_food_product, unstocked_food_product)

    # Delete a product
    db_instance_empty.delete_product(session=session, product_id=stocked_food_product.product_id)

    # Get all products
    all_product = db_instance_empty.get_all_products()

    # Test product has been deleted
    assert len(all_product) == 1
    assert all_product[0].product == unstocked_food_product.product



