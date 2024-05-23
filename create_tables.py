from app import db,app,User

#Instructions to create db
#Run docker compose file
#Run create_db file
#Run this file
with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.add(User(email="admin@admin.com", password="admin123!", access_level="admin"))
    db.session.commit()