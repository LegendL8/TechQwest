from app import create_app
from models import db, User

def create_admin_user(username, email, password):
    app = create_app()
    with app.app_context():
        # Check if admin already exists
        if User.query.filter_by(username=username).first():
            print("Admin user already exists")
            return
        
        # Create new admin user
        admin = User(username=username, email=email, is_admin=True)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully")

if __name__ == "__main__":
    create_admin_user("admin", "admin@example.com", "adminpass123")
