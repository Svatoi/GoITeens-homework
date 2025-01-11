import os
from flask import Flask, render_template
# LoginManager - для працювання з користувачами а саме запис їх сеансів
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# HTTPException - для опрацювання HTTP-помилок включно статус-коди 4xx та 5xx
from werkzeug.exceptions import HTTPException

login_manager = LoginManager()
db = SQLAlchemy()
    
def create_app(environment="development"):
    from config import config
    from .views import main_bp, auth_bp, blog_bp, user_bp
    from .models import User, AnonymousUser

    app = Flask(__name__)

    env = os.getenv("FLASK_ENV", environment)
    app.config.from_object(config[env])
    config[env].configure(app)

    #Setup extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)
    app.register_blueprint(user_bp)

    @login_manager.user_loader
    def get_user(id):
        return User.query.get(int(id))
    
    login_manager.login_view = 'auth.signin'
    login_manager.login_message_category = 'info'
    login_manager.anonymous_user = AnonymousUser

    @app.errorhandler(HTTPException)
    def handle_http_error(exc):
        return render_template("error.html", error=exc), exc.code
    
    return app