import os
from dotenv import load_dotenv

load_dotenv()
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()
limiter = Limiter(key_func=get_remote_address, default_limits=['200 per day', '50 per hour'])


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///meditrack.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', '587'))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['APP_NAME'] = os.getenv('APP_NAME', 'MediTrack')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'

    from . import models
    from .routes.main import main_bp
    from .routes.auth import auth_bp
    from .routes.assets import assets_bp
    from .routes.maintenance import maintenance_bp
    from .routes.inventory import inventory_bp
    from .routes.procurement import procurement_bp
    from .routes.compliance import compliance_bp
    from .routes.reports import reports_bp
    from .routes.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(assets_bp, url_prefix='/assets')
    app.register_blueprint(maintenance_bp, url_prefix='/maintenance')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(procurement_bp, url_prefix='/procurement')
    app.register_blueprint(compliance_bp, url_prefix='/compliance')
    app.register_blueprint(reports_bp, url_prefix='/reports')
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.context_processor
    def inject_globals():
        return {'app_name': app.config['APP_NAME']}

    with app.app_context():
        db.create_all()
        from .seed import bootstrap_defaults
        bootstrap_defaults()

    return app
