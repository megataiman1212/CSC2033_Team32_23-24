from app import db,app
from models import Product
from sqlmodel import Session
from models import Product
from sqlmodel import Session
from sqlalchemy import create_engine



class DB_Manager():
    def __init__(self):
        # Define the database URI
        db_uri = 'mysql+pymysql://root:Team32@localhost/Inventory'

        # Create the engine (used for CRUD)
        engine = create_engine(db_uri, echo=True)
        self.engine = engine

    def create_product(self, product: Product, session: Session) -> None:
        """
        Create a task in the database

        Args:
            product (Product): The product to create
            Session (Session): The database session

        Returns:
            int: The ID of the created task
        """
        # Write to database
        session.add(product)
        session.commit()

    def delete_all_products(self, session):

        try:
            session.query(Product).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()



    # FR11
    def get_required_stock(self, session: Session):
        # Returns list of Product objects
        stock = Product.query.filter(Product.stock < Product.required_level).all()
        return stock

    #FR8
    def get_all_products(self):
        # Returns list of all product Objects
        stock = Product.query.all()
        return stock

    #FR15
    def query_products(self, search_string):
        # Returns any products that contain the substring search_string not case dependant
        if not isinstance(search_string, str):
            raise TypeError("SearchString must be a string")
        stock = Product.query.all()
        searched_stock = []
        for i in stock:
            if search_string.upper() in i.product.upper():
                searched_stock.append(i)
        return searched_stock

    #
    # #FR9
    # def add_product(Product, Stock, Category, Required_Level):
    #     # check passed datatypes
    #     #
    #     # connect to server
    #     # create cursor
    #     #
    #     # create add_product query
    #     # create data_product list
    #     # https: // dev.mysql.com / doc / connector - python / en / connector - python - example - cursor - transaction.html
    #     #
    #     # execute using cursor
    #     #
    #     # commit with connection
    #     # close cursor
    #     # close connection
    #
    # #FR10
    # def adjust_stock(ProductID, mode)
    #     # mode is true (increase) or false (decrease)
    #     # check ProductID is int
    #     #
    #     # connect to server
    #     # create cursor
    #     #
    #     # form query
    #     # from Products get Stock where ID = Product ID
    #     #
    #     # if product returned and mode
    #     # form query
    #     # update products Stock+1 where ID = Product ID
    #     #
    #     # id product returned and !mode and stock!=0
    #     # form query
    #     # update products Stock-1 where ID = Product ID
    #     #
    #     # execute query
    #     #
    #     # commit with cursor
    #     #
    #     # close cursor
    #     # close connection
    #     # return true if successful
    #     # return false if not
    #
    # #FR17
    # def change_order_level(ProductID, NewNumber):
    #     # check ProductID and NewNumber are ints
    #     # connect to server
    #     # create cursor
    #     #
    #     # form query
    #     # update products stock==NewNumber where ProductID = ProductID
    #     #
    #     # execute query
    #     #
    #     # try commit with cursur
    #     # else close cursor, connection and return false
    #     #
    #     # close cursor
    #     # close connection
    #     # return true
    #
    # #FR5
    # def delete_product(ProductID):
    #     # check ProductID is int
    #     # connect to server
    #     # create cursor
    #     #
    #     # form query
    #     # delete from Product where ID = ProductID
    #     #
    #     # execute query
    #     #
    #     # try commit with cursor
    #     # else close cursor, connection and return false
    #     #
    #     # close cursor
    #     # close connection
    #     # return true
    #
    # #FR4
    # def get_all_users():
    #     # connect to server
    #     # create cursor
    #     #
    #     # form query:
    #     # from Users select all ID, Email, access level
    #     # execute query
    #     #
    #     # create returnable variable (list / 2D array)
    #     # close cursor
    #     # close connection
    #     # return variable
    #
    # #FR2,7
    # def change_password(ID, CurrentPassword, NewPassword):
    #     # (Both passwords should already be encrypted)
    #     # connect to server
    #     # create cursor
    #     #
    #     # bool = verify_password(ID, CurrentPassword)
    #     #
    #     # if !bool
    #     #    close cursor
    #     #    close connection
    #     #    return false
    #     #
    #     # form query
    #     # update products password
    #     #
    #     # commit with cursor
    #     # close cursor
    #     # close connection
    #     # return true
    #
    # #FR1,3
    # def add_staff(Email, Password, AccessLevel)
    #     # Check email is string, Access level is bool (1=Admin, 2=Staff)
    #     # Password should be encrypted by this stage
    #     #
    #     # connect to server
    #     # create cursor
    #     #
    #     # create add_user query (AccessLevel decides admin/staff)
    #     # create data_user list
    #     # https: // dev.mysql.com / doc / connector - python / en / connector - python - example - cursor - transaction.html
    #     #
    #     # execute using cursor
    #     #
    #     # commit with connection
    #     # close cursor
    #     # close connection
    #
    # #FR4
    # def delete_staff(UserID);
    #     # check UserID is int
    #     # connect to server
    #     # create cursor
    #     #
    #     # form query
    #     # delete from User where ID = ProductID
    #     #
    #     # execute query
    #     #
    #     # try commit with cursor
    #     # else close cursor, connection and return false
    #     #
    #     # close cursor
    #     # close connection
    #     # return true
    #
    # #FR12
    # def verify_password(UserID, test_password):
    #     # check UserID is int
    #     # password should be encrypted
    #     #
    #     # connect to server
    #     # create cursor
    #     #
    #     # form query
    #     # select password from Users where ID = UserID
    #     #
    #     # execute query
    #     #
    #     # close cursur
    #     # close connection
    #     #
    #     # return test_password = cursor.password




