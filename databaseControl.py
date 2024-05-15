# Used below as reference for whats possible
# https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-select.html

from models import Product

# FR11
def get_required_stock():
    pass
    # connect to server
    # create cursor
    #
    # form query;
    # from Products select all Product names where stock < required level
    # execute query
    #
    # create returnable variable (list / 2D array might work)
    # close cursor
    # close connection
    # return variable

#FR8
def get_all_products():
    pass
    # connect to server
    # create cursor
    #
    # form query:
    # from Products select all ID, name, stock, required_level
    # execute query
    #
    # create returnable variable (list / 2D array)
    # close cursor
    # close connection
    # return variable


#FR15
def query_products(SearchString):
    results = Product.query.filter(Product.product.icontains(SearchString))\
        .order_by(Product.product.asc())
    print(results)

    return results


#FR9
def add_product(Product, Stock, Category, Required_Level):
    pass
    # check passed datatypes
    #
    # connect to server
    # create cursor
    #
    # create add_product query
    # create data_product list
    # https: // dev.mysql.com / doc / connector - python / en / connector - python - example - cursor - transaction.html
    #
    # execute using cursor
    #
    # commit with connection
    # close cursor
    # close connection


#FR10
def adjust_stock(product_id, mode):
    pass
    # mode is 0 (increase) or 1 (decrease)
    # check id and mode are int

#FR17
def change_order_level(ProductID, NewNumber):
    pass
    # check ProductID and NewNumber are ints
    # connect to server
    # create cursor
    #
    # form query
    # update products stock==NewNumber where ProductID = ProductID
    #
    # execute query
    #
    # try commit with cursur
    # else close cursor, connection and return false
    #
    # close cursor
    # close connection
    # return true

#FR5
def delete_product(ProductID):
    pass
    # check ProductID is int
    # connect to server
    # create cursor
    #
    # form query
    # delete from Product where ID = ProductID
    #
    # execute query
    #
    # try commit with cursor
    # else close cursor, connection and return false
    #
    # close cursor
    # close connection
    # return true

#FR4
def get_all_users():
    pass
    # connect to server
    # create cursor
    #
    # form query:
    # from Users select all ID, Email, access level
    # execute query
    #
    # create returnable variable (list / 2D array)
    # close cursor
    # close connection
    # return variable

#FR2,7
def change_password(ID, CurrentPassword, NewPassword):
    pass
    # (Both passwords should already be encrypted)
    # connect to server
    # create cursor
    #
    # bool = verify_password(ID, CurrentPassword)
    #
    # if !bool
    #    close cursor
    #    close connection
    #    return false
    #
    # form query
    # update products password
    #
    # commit with cursor
    # close cursor
    # close connection
    # return true

#FR1,3
def add_staff(Email, Password, AccessLevel):
    pass
    # Check email is string, Access level is bool (1=Admin, 2=Staff)
    # Password should be encrypted by this stage
    #
    # connect to server
    # create cursor
    #
    # create add_user query (AccessLevel decides admin/staff)
    # create data_user list
    # https: // dev.mysql.com / doc / connector - python / en / connector - python - example - cursor - transaction.html
    #
    # execute using cursor
    #
    # commit with connection
    # close cursor
    # close connection

#FR4
def delete_staff(UserID):
    pass
    # check UserID is int
    # connect to server
    # create cursor
    #
    # form query
    # delete from User where ID = ProductID
    #
    # execute query
    #
    # try commit with cursor
    # else close cursor, connection and return false
    #
    # close cursor
    # close connection
    # return true

#FR12
def verify_password(UserID, test_password):
    pass
    # check UserID is int
    # password should be encrypted
    #
    # connect to server
    # create cursor
    #
    # form query
    # select password from Users where ID = UserID
    #
    # execute query
    #
    # close cursor
    # close connection
    #
    # return test_password = cursor.password
