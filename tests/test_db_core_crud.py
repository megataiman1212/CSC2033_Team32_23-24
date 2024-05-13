




# Tests by adding a product and then searching for it
def test_query_products(db_instance_empty, session, stocked_food_product, unstocked_food_product):

    # Adds the two pre-made products to a temporary session in the db
    db_instance_empty.create_product(product=stocked_food_product, session=session)
    db_instance_empty.create_product(product=unstocked_food_product, session=session)

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
