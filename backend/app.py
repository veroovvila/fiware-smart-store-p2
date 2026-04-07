"""
Flask Application Entry Point
Main application initialization and configuration
"""

import logging
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO

from config import get_config
from data.import_data import OrionDataImporter
from services.orion_service import OrionService
from services.provider_service import ProviderService
from services.subscription_service import SubscriptionService
from services.notification_service import NotificationService
from routes.products import products_bp
from routes.stores import stores_bp
from routes.employees import employees_bp
from routes.inventory import inventory_bp

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def create_app(config=None):
    """
    Application factory function
    
    Args:
        config: Configuration object or environment string
        
    Returns:
        Tuple of (Flask app, SocketIO instance)
    """
    app = Flask(__name__)
    
    # Load configuration
    if config is None:
        config = get_config(os.getenv('FLASK_ENV', 'development'))
    elif isinstance(config, str):
        config = get_config(config)
    
    app.config.from_object(config)
    
    # Initialize extensions - Allow all origins in development
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    socketio = SocketIO(app, cors_allowed_origins="*")
    
    logger.info(f"Flask app initialized with config: {config.__class__.__name__}")
    
    # Initialize services with Orion URL for HTTP calls
    orion_service = OrionService(config.ORION_URL)
    provider_service = ProviderService()
    subscription_service = SubscriptionService(config.ORION_URL)  # Pass Orion URL
    notification_service = NotificationService(socketio)
    
    # Store services in app context for later use
    app.orion_service = orion_service
    app.provider_service = provider_service
    app.subscription_service = subscription_service
    app.notification_service = notification_service
    
    # Run data import on startup
    with app.app_context():
        try:
            health = orion_service.health_check()
            if health.get('status') == 'healthy':
                logger.info("Orion is healthy, starting data import...")
                importer = OrionDataImporter(config.ORION_URL)
                importer.run(provider_service, subscription_service)
            else:
                logger.warning(f"Orion is not healthy: {health}")
        except Exception as e:
            logger.error(f"Error during data import: {str(e)}")
    
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
    
    # Diagnostic endpoint
    @app.route('/api/v1/diagnostic', methods=['GET'])
    def diagnostic():
        """Check API connectivity"""
        try:
            # Use app context to access orion_service
            health = app.orion_service.health_check()
            
            # Try to get products
            result = app.orion_service.list_entities(entity_type='Product', limit=5)
            
            return jsonify({
                'status': 'ok',
                'orion_health': health,
                'products_query': result,
                'total_found': len(result.get('entities', [])) if result.get('success') else 0,
                'message': 'Diagnostic check performed'
            }), 200
        except Exception as e:
            logger.error(f"Diagnostic error: {str(e)}")
            return jsonify({
                'status': 'error',
                'error': str(e)
            }), 500
    
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
    
    # Notifications endpoint - receives notifications from Orion
    @app.route('/notifications', methods=['POST'])
    def receive_notifications():
        """
        Receive notifications from Orion Context Broker
        Broadcasts via Socket.IO to connected clients
        
        Returns:
            JSON response acknowledging receipt
        """
        try:
            data = request.get_json() or {}
            
            logger.info(f"Received notification from Orion: {data.get('subscriptionId')}")
            
            # Extract relevant data
            subscription_id = data.get('subscriptionId')
            notification_type = 'unknown'
            
            # Determine notification type based on data
            if 'data' in data and isinstance(data['data'], list):
                for entity in data['data']:
                    entity_type = entity.get('type', '')
                    
                    # Price change notification
                    if 'price' in entity and entity_type == 'Product':
                        notification_type = 'price_change'
                        app.notification_service.notify_price_change(
                            entity.get('id'),
                            entity.get('price', {}).get('value'),
                            entity.get('price', {}).get('metadata', {}).get('oldValue')
                        )
                    
                    # Low stock notification
                    elif 'quantity' in entity and entity_type == 'InventoryItem':
                        quantity = entity.get('quantity', {}).get('value')
                        if quantity is not None and quantity < 10:
                            notification_type = 'low_stock'
                            app.notification_service.notify_low_stock(
                                entity.get('productId', {}).get('value'),
                                quantity,
                                10
                            )
                    
                    # Generic broadcast
                    app.notification_service.broadcast('entity_update', {
                        'subscription_id': subscription_id,
                        'entity_id': entity.get('id'),
                        'entity_type': entity_type,
                        'notification_type': notification_type,
                        'data': entity
                    })
            
            return jsonify({
                'success': True,
                'message': 'Notification received',
                'subscription_id': subscription_id
            }), 200
            
        except Exception as e:
            logger.error(f"Error processing notification: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400
    
    # Socket.IO event handlers
    @socketio.on('connect')
    def handle_connect():
        """Socket.IO connection handler"""
        logger.info("Client connected via Socket.IO")
        return True
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Socket.IO disconnection handler"""
        logger.info("Client disconnected from Socket.IO")
    
    # Register API Blueprints
    logger.info("Registering API Blueprints...")
    app.register_blueprint(products_bp)
    app.register_blueprint(stores_bp)
    app.register_blueprint(employees_bp)
    app.register_blueprint(inventory_bp)
    logger.info("API Blueprints registered successfully")
    
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
        debug=config.FLASK_DEBUG,
        allow_unsafe_werkzeug=True
    )
