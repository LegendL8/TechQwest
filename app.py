import os
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from models import db, User
from scheduler import init_scheduler

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Security configurations
    app.secret_key = os.environ.get("FLASK_SECRET_KEY") or os.urandom(24)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    
    # Security headers
    Talisman(app, 
             content_security_policy={
                'default-src': "'self'",
                'script-src': ["'self'", "'unsafe-inline'", "cdn.jsdelivr.net"],
                'style-src': ["'self'", "'unsafe-inline'", "cdn.replit.com"],
                'img-src': ["'self'", "data:", "cdn.replit.com"],
                'font-src': ["'self'", "cdn.replit.com"]
             },
             force_https=False)  # Set to True in production
    
    # Rate limiting
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    
    # Session configuration
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = "info"
    
    from routes import auth, admin, questions, analytics
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(questions.bp)
    app.register_blueprint(analytics.bp)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    with app.app_context():
        db.create_all()
        
        # Create default categories if they don't exist
        from models import Category
        default_categories = ['Programming', 'Networking', 'Security', 'DevOps', 'Databases']
        for category_name in default_categories:
            if not Category.query.filter_by(name=category_name).first():
                db.session.add(Category(name=category_name))
        db.session.commit()

        # Initialize the scheduler
        scheduler = init_scheduler(app)
        app.scheduler = scheduler

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
