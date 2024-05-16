from app import app, db
from models import User, Product

with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.add(User(email="admin@admin.com", password="admin123!", access_level="admin"))
    db.session.add(Product(product="Bread Loaf", stock=20, category="food", required_level=10))
    db.session.add(Product(product="Bread Roll", stock=10, category="food", required_level=0))
    db.session.add(Product(product="Tomato Soup", stock=20, category="food", required_level=40))
    db.session.add(Product(product="Mushroom Soup", stock=3, category="food", required_level=5))
    db.session.commit()