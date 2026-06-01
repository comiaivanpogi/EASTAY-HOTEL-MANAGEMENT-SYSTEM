from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__, static_folder='../static', template_folder='../templates')
    CORS(app)
    
    app.config['SECRET_KEY'] = 'your-super-secret-jwt-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    bcrypt.init_app(app)
    
    from app.routes.auth import auth_bp
    from app.routes.rooms import rooms_bp
    from app.routes.bookings import bookings_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(rooms_bp, url_prefix='/api/rooms')
    app.register_blueprint(bookings_bp, url_prefix='/api/bookings')
    
    from flask import send_from_directory
    @app.route('/')
    def index():
        return send_from_directory('../templates', 'index.html')
        
    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory('../static', path)
    
    return app

