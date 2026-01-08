from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    with app.app_context():
        from app.routes.auth_routes import auth_bp
        app.register_blueprint(auth_bp)
        
        from app.routes.admin_routes import admin_bp
        app.register_blueprint(admin_bp)

        from app.routes.front_desk import front_desk_bp
        app.register_blueprint(front_desk_bp)
        
        from app.routes.guest_api import guest_api_bp
        app.register_blueprint(guest_api_bp)

        from app.routes.report_routes import report_bp
        app.register_blueprint(report_bp)

        # THIS IS THE MISSING LINE CAUSING THE CRASH
        return app