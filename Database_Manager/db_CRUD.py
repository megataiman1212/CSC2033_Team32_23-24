
from models import Product, User
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

    #FR9
    @staticmethod
    def add_product(session, product, stock, category, required_level):
        session.add(Product(product, stock, category, required_level))
        session.commit()

    #FR10
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
    @staticmethod
    def delete_product(session, product_id):
        session.delete(Product.query.get(product_id))
        session.commit()

    #FR4
    @staticmethod
    def get_all_users():
        return User.query.all()

    #FR2,7
    @staticmethod
    def change_password(session, user_id, current_password, new_password):
        user = User.query.get(user_id)
        if user.password == current_password:
            user.password = new_password
            session.commit()
        else:
            raise ValueError("Password does not match")

    #FR1,3#
    @staticmethod
    def add_staff(session, email, password, access_level):
        if access_level != ("user" or "admin"):
            raise ValueError("Access level must be user or admin")
        session.add(User(email, password, access_level))
        session.commit()

    #FR4
    @staticmethod
    def delete_staff(session, user_id):
        session.delete(User.query.get(user_id))
        session.commit()

    #FR12
    @staticmethod
    def verify_password(user_id, test_password):
        user = User.query.get(user_id)
        return user.password == test_password
