from app import create_app
from models import db, Category

def update_categories():
    app = create_app()
    with app.app_context():
        # List of technical categories
        categories = [
            'Help Desk',
            'Programming',
            'Data Structures',
            'Networking',
            'Security',
            'DevOps',
            'Databases',
            'Cloud Computing',
            'System Administration',
            'Software Engineering'
        ]
        
        # Add categories if they don't exist
        for category_name in categories:
            if not Category.query.filter_by(name=category_name).first():
                db.session.add(Category(name=category_name))
        
        db.session.commit()
        print("Categories updated successfully")

if __name__ == "__main__":
    update_categories()
