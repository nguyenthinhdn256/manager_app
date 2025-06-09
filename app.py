# File chính khởi tạo app
from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager

# Import config
from config.env import Config
from config.db import db, init_db

# Import routes
from routes.sync import sync_bp
from routes.user import user_bp
from routes.data import data_bp

# Import middlewares
from middlewares.error_handler import register_error_handlers

# Import utils
from utils.logger import logger

def create_app():
    """Tạo và cấu hình Flask app"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Initialize extensions
    CORS(app, origins=app.config['CORS_ORIGINS'])
    db.init_app(app)
    jwt = JWTManager(app)
    
    # Initialize SocketIO with threading mode (compatible with Python 3.13)
    socketio = SocketIO(
        app, 
        cors_allowed_origins="*",
        async_mode='threading'  # Changed from 'eventlet' to 'threading'
    )
    
    # Initialize database
    with app.app_context():
        init_db()
    
    # Register blueprints (routes)
    app.register_blueprint(sync_bp, url_prefix='/api/sync')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(data_bp, url_prefix='/api/data')
    
    # Health check endpoint
    @app.route('/')
    def health_check():
        return jsonify({
            'message': 'Backend API is running',
            'status': 'OK',
            'framework': 'Flask + Python'
        })
    
    # Socket.IO events
    @socketio.on('connect')
    def handle_connect():
        logger.info(f'Client connected')
    
    @socketio.on('disconnect')
    def handle_disconnect():
        logger.info(f'Client disconnected')
    
    # Register error handlers
    register_error_handlers(app)
    
    # Store socketio instance in app for use in other modules
    app.socketio = socketio
    
    return app, socketio

# Create app instance
app, socketio = create_app()