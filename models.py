from app import db,app


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    access_level = db.Column(db.String(100), nullable=False)

    def __init__(self,email, password, access_level="user"):
        self.email = email
        self.password = password
        self.access_level = access_level


class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)

    product = db.Column(db.String(100))
    stock = db.Column(db.Integer)
    category = db.Column(db.String(100))
    required_level = db.Column(db.Integer)

    def __init__(self, product, stock, category, required_level):
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
    #db.session.add(User(email="admin@admin.com", password="admin123!", access_level="admin"))
    db.session.add(Product(product="Bread Loaf", stock=20, category="Food", required_level=10))
    db.session.add(Product(product="Bread Roll", stock=10, category="Food", required_level=0))
    db.session.add(Product(product="Tomato Soup", stock=20, category="Food", required_level=40))
    db.session.add(Product(product="Mushroom Soup", stock=3, category="Food", required_level=5))
    db.session.commit()

