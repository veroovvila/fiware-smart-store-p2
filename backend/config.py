"""
Backend Configuration Module
Central configuration management for all backend services
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration class"""
    
    # Flask Configuration
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    
    # FIWARE Orion Configuration
    ORION_URL = os.getenv('ORION_URL', 'http://localhost:1026')
    ORION_VERSION = os.getenv('ORION_VERSION', '2.0')
    
    # MongoDB Configuration
    MONGODB_URL = os.getenv('MONGODB_URL', 'mongodb://localhost:27017')
    MONGO_ROOT_USER = os.getenv('MONGO_ROOT_USER', 'admin')
    MONGO_ROOT_PASSWORD = os.getenv('MONGO_ROOT_PASSWORD', 'password')
    MONGO_DB = os.getenv('MONGO_DB', 'fiware_smart_store')
    
    # API Configuration
    API_PREFIX = '/api/v1'
    JSON_SORT_KEYS = False
    
    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:8080').split(',')
    
    # Security
    JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key-change-in-production')
    SESSION_SECRET = os.getenv('SESSION_SECRET', 'your-session-key-change-in-production')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
    
    # External APIs
    WEATHER_API_URL = os.getenv('WEATHER_API_URL', 'https://openweathermap.org/data/2.5/weather')
    TWITTER_API_URL = os.getenv('TWITTER_API_URL', 'https://api.twitter.com/2')
    
    # Socket.IO Configuration
    SOCKETIO_CORS_ALLOWED_ORIGINS = CORS_ORIGINS
    SOCKETIO_ASYNC_MODE = 'threading'


class DevelopmentConfig(Config):
    """Development environment configuration"""
    FLASK_DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing environment configuration"""
    TESTING = True
    FLASK_DEBUG = True
    MONGODB_DB = 'fiware_smart_store_test'


class ProductionConfig(Config):
    """Production environment configuration"""
    FLASK_DEBUG = False
    TESTING = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    """Get configuration object based on environment"""
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
