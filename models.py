from app import db, app
from flask_login import UserMixin

class User(db.Model):
    """User table """
    user_id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    access_level = db.Column(db.String(100), nullable=False)

    def __init__(self,email, password, access_level="user"):
        # Validate email
        if not isinstance(email, str):
            raise TypeError("Email must be a string")

        # Validate password
        if not isinstance(password, str):
            raise TypeError("Password must be a string")

        # Validate access level
        allowed_access_levels = ["user", "admin"]
        if access_level not in allowed_access_levels:
            raise ValueError("Access level must be 'user' or 'admin'")

        self.email = email
        self.password = password
        self.access_level = access_level

    def get_id(self):
        return self.user_id

class Product(db.Model):
    """Product table"""
    product_id = db.Column(db.Integer, primary_key=True)

    product = db.Column(db.String(100))
    stock = db.Column(db.Integer)
    category = db.Column(db.String(100))
    required_level = db.Column(db.Integer)

    def __init__(self, product, stock, category, required_level):
        #validate product
        if not isinstance(product, str):
            raise TypeError("Product must be a string")

        #validate stock
        if not isinstance(stock, int):
            raise TypeError("Stock must be an integer")

        #validate category
        allowed_category = ["food", "hygiene"]
        if category not in allowed_category:
            raise ValueError("Category must be 'food' or 'hygiene'")

        #validate required_level
        if not isinstance(required_level, int):
            raise TypeError("Required level must be an integer")

        self.product = product
        self.stock = stock
        self.category = category
        self.required_level = required_level

#Instructions to create db
#Run docker compose file
#Run create_db file
#Run models file
with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.add(User(email="admin@admin.com", password="admin123!", access_level="admin"))
    db.session.commit()

