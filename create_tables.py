"""File to reset the database and add a default admin """
from app import db,app,User

with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.add(User(email="admin@admin.com", password="Admin123!", access_level="admin"))
    db.session.commit()
