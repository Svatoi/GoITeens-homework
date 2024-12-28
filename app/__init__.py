from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from werkzeug.exceptions import HTTPException

db = SQLAlchemy()
    
def create_app():
    from .views import main_bp, auth_bp

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Gwak_db.db'

    #Setup extensions
    db.init_app(app)

    # Register bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    @app.errorhandler(HTTPException)
    def handle_http_error(exc):
        return render_template("error.html", error=exc), exc.code
    
    return app