"""
Flask Application Entry Point
Main application initialization and configuration
"""

import logging
import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO

from config import get_config

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def create_app(config=None):
    """
    Application factory function
    
    Args:
        config: Configuration object or environment string
        
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    if config is None:
        config = get_config(os.getenv('FLASK_ENV', 'development'))
    elif isinstance(config, str):
        config = get_config(config)
    
    app.config.from_object(config)
    
    # Initialize extensions
    CORS(app, origins=config.CORS_ORIGINS)
    socketio = SocketIO(app, cors_allowed_origins=config.SOCKETIO_CORS_ALLOWED_ORIGINS)
    
    logger.info(f"Flask app initialized with config: {config.__class__.__name__}")
    
    # Register Blueprint placeholder for future routes
    # These will be populated in Phase 3+
    # from routes import products_bp, stores_bp, inventory_bp, employees_bp
    # app.register_blueprint(products_bp, url_prefix=f'{config.API_PREFIX}/products')
    # app.register_blueprint(stores_bp, url_prefix=f'{config.API_PREFIX}/stores')
    # app.register_blueprint(inventory_bp, url_prefix=f'{config.API_PREFIX}/inventory')
    # app.register_blueprint(employees_bp, url_prefix=f'{config.API_PREFIX}/employees')
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        """
        Health check endpoint for monitoring
        
        Returns:
            JSON response with health status
        """
        return jsonify({
            'status': 'healthy',
            'service': 'fiware-smart-store-backend',
            'version': '1.0.0',
            'environment': app.config['FLASK_ENV']
        }), 200
    
    # API version endpoint
    @app.route('/api/version', methods=['GET'])
    def api_version():
        """
        API version endpoint
        
        Returns:
            JSON response with API version info
        """
        return jsonify({
            'api_version': 'v1',
            'backend_version': '1.0.0',
            'orion_url': app.config['ORION_URL']
        }), 200
    
    # Socket.IO event handlers
    @socketio.on('connect')
    def handle_connect():
        """Socket.IO connection handler"""
        logger.info("Client connected")
        return True
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Socket.IO disconnection handler"""
        logger.info("Client disconnected")
    
    return app, socketio


if __name__ == '__main__':
    app, socketio = create_app()
    
    # Get configuration
    config = get_config(os.getenv('FLASK_ENV', 'development'))
    
    logger.info(f"Starting Flask app on port {config.FLASK_PORT}")
    logger.info(f"Orion URL: {config.ORION_URL}")
    logger.info(f"MongoDB URL: {config.MONGODB_URL}")
    
    # Run the application
    socketio.run(
        app,
        host='0.0.0.0',
        port=config.FLASK_PORT,
        debug=config.FLASK_DEBUG
    )
