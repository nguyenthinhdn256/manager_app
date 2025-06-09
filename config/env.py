# Cấu hình kết nối DB, môi trường, v.v.
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class"""
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration - HARDCODED SQLite for now
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./database.db'  # Force SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # JWT configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 86400))  # 24 hours
    JWT_ALGORITHM = 'HS256'
    
    # CORS configuration
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # Server configuration
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Logging configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
    LOG_TO_FILE = os.environ.get('LOG_TO_FILE', 'False').lower() == 'true'
    
    # Firebase configuration (optional)
    FIREBASE_PROJECT_ID = os.environ.get('FIREBASE_PROJECT_ID')
    FIREBASE_PRIVATE_KEY = os.environ.get('FIREBASE_PRIVATE_KEY')
    FIREBASE_CLIENT_EMAIL = os.environ.get('FIREBASE_CLIENT_EMAIL')
    
    # Rate limiting
    RATE_LIMIT_ENABLED = os.environ.get('RATE_LIMIT_ENABLED', 'True').lower() == 'true'
    RATE_LIMIT_DEFAULT = os.environ.get('RATE_LIMIT_DEFAULT', '100 per hour')
    
    # File upload (nếu cần)
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
    
    # Email configuration (nếu cần)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Sync configuration
    SYNC_BATCH_SIZE = int(os.environ.get('SYNC_BATCH_SIZE', 100))
    SYNC_TIMEOUT = int(os.environ.get('SYNC_TIMEOUT', 30))  # seconds
    
    # Security headers
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'
    }

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    
    # Development specific settings
    SQLALCHEMY_ECHO = True  # Log SQL queries
    LOG_LEVEL = 'DEBUG'
    
    # Relaxed security for development
    CORS_ORIGINS = ['*']
    RATE_LIMIT_ENABLED = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Production specific settings
    SQLALCHEMY_ECHO = False
    LOG_TO_FILE = True
    
    # Stricter security for production
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'https://yourdomain.com').split(',')
    RATE_LIMIT_ENABLED = True
    
    def __init__(self):
        super().__init__()
        # Override with production values only if they exist
        if os.environ.get('SECRET_KEY'):
            self.SECRET_KEY = os.environ.get('SECRET_KEY')
        elif os.environ.get('FLASK_ENV') == 'production':
            raise ValueError("SECRET_KEY environment variable must be set in production")
        
        if os.environ.get('JWT_SECRET_KEY'):
            self.JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
        elif os.environ.get('FLASK_ENV') == 'production':
            raise ValueError("JWT_SECRET_KEY environment variable must be set in production")

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    
    # Use in-memory database for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Disable features that slow down tests
    WTF_CSRF_ENABLED = False
    RATE_LIMIT_ENABLED = False
    
    # Test specific settings
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour for tests

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])

# Current configuration
Config = get_config()

# Validation functions
def validate_config():
    """Validate required configuration"""
    required_vars = []
    
    # Check database
    if not Config.SQLALCHEMY_DATABASE_URI:
        required_vars.append('DATABASE_URL')
    
    # Check JWT secret in production
    if os.environ.get('FLASK_ENV') == 'production':
        if not Config.JWT_SECRET_KEY or Config.JWT_SECRET_KEY == 'jwt-secret-change-in-production':
            required_vars.append('JWT_SECRET_KEY')
        
        if not Config.SECRET_KEY or Config.SECRET_KEY == 'dev-secret-key-change-in-production':
            required_vars.append('SECRET_KEY')
    
    if required_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(required_vars)}")
    
    return True

def get_database_url():
    """Get database URL with fallbacks"""
    # Priority: DATABASE_URL > DB_URI > default SQLite
    return (
        os.environ.get('DATABASE_URL') or 
        os.environ.get('DB_URI') or 
        'sqlite:///database.db'
    )

def is_production():
    """Check if running in production"""
    return os.environ.get('FLASK_ENV') == 'production'

def is_development():
    """Check if running in development"""
    return os.environ.get('FLASK_ENV', 'development') == 'development'

def is_testing():
    """Check if running tests"""
    return os.environ.get('FLASK_ENV') == 'testing'

def get_cors_origins():
    """Get CORS origins as list"""
    origins = os.environ.get('CORS_ORIGINS', '*')
    if origins == '*':
        return ['*']
    return [origin.strip() for origin in origins.split(',')]

def get_log_level():
    """Get logging level"""
    level = os.environ.get('LOG_LEVEL', 'INFO').upper()
    valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    return level if level in valid_levels else 'INFO'

# Environment info
ENV_INFO = {
    'flask_env': os.environ.get('FLASK_ENV', 'development'),
    'debug': Config.DEBUG,
    'testing': getattr(Config, 'TESTING', False),
    'database_type': 'sqlite' if 'sqlite' in Config.SQLALCHEMY_DATABASE_URI else 'other',
    'cors_origins': len(Config.CORS_ORIGINS),
    'rate_limit_enabled': Config.RATE_LIMIT_ENABLED,
    'log_to_file': Config.LOG_TO_FILE,
    'firebase_enabled': bool(Config.FIREBASE_PROJECT_ID)
}

def print_config_info():
    """Print configuration info for debugging"""
    print("=" * 50)
    print("BACKEND CONFIGURATION")
    print("=" * 50)
    for key, value in ENV_INFO.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    print("=" * 50)

# Auto validate on import (except in testing)
if not is_testing():
    try:
        validate_config()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        if is_production():
            raise