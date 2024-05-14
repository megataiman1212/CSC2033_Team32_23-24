
from models import Product
from sqlmodel import Session
from sqlalchemy import create_engine


class DbManager():
    def __init__(self):
        # Define the database URI
        db_uri = 'mysql+pymysql://root:Team32@localhost/Inventory'

        # Create the engine (used for CRUD)
        engine = create_engine(db_uri, echo=True)
        self.engine = engine

    @staticmethod
    def create_product(product: Product, session: Session) -> None:
        """
        Create a task in the database

        Args:
            product (Product): The product to create
            session (Session): The database session

        Returns:
            int: The ID of the created task
        """
        # Write to database
        session.add(product)
        session.commit()

    @staticmethod
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
    @staticmethod
    def get_required_stock(session: Session):
        # Returns list of Product objects
        stock = Product.query.filter(Product.stock < Product.required_level).all()
        return stock

    #FR8
    @staticmethod
    def get_all_products():
        # Returns list of all product Objects
        stock = Product.query.all()
        return stock

    #FR15
    @staticmethod
    def query_products(search_string):
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
    @staticmethod
    def adjust_stock(session, product_id, mode):
        # need to add type checking
        product_to_edit = Product.query.get(product_id)
        if mode:
            product_to_edit.stock += 1
        else:
            product_to_edit.stock -= 1
        session.commit()


    #FR17
    @staticmethod
    def change_order_level(self,session, product_id, new_stock):
        # check ProductID and NewNumber are ints
        product = Product.query.get(product_id)
        product.stock = new_stock
        session.commit()

    #FR5
    # @staticmethod
    # def delete_product(self,ProductID):
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
