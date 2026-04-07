"""
Custom Decorators Module
Decorators for Flask routes and utilities
Phase 2: Error handling and basic decorators
"""

import logging
from functools import wraps
from typing import Callable, Any
from flask import jsonify, request

logger = logging.getLogger(__name__)


def handle_errors(func: Callable) -> Callable:
    """
    Decorator for handling errors in Flask route handlers
    Catches exceptions and returns proper error responses
    
    Usage:
        @app.route('/api/products')
        @handle_errors
        def get_products():
            # Route logic
            pass
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            logger.warning(f"Validation error in {func.__name__}: {str(e)}")
            return jsonify({
                'error': str(e),
                'code': 400,
                'type': 'validation_error'
            }), 400
        except KeyError as e:
            logger.warning(f"Missing required field in {func.__name__}: {str(e)}")
            return jsonify({
                'error': f"Missing required field: {str(e)}",
                'code': 400,
                'type': 'missing_field'
            }), 400
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
            return jsonify({
                'error': 'Internal server error',
                'code': 500,
                'type': 'server_error'
            }), 500
    
    return wrapper


def require_json(func: Callable) -> Callable:
    """
    Decorator to require JSON request content
    
    Usage:
        @app.route('/api/products', methods=['POST'])
        @require_json
        @handle_errors
        def create_product():
            data = request.get_json()
            # Route logic
            pass
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if not request.is_json:
            logger.warning(f"{func.__name__}: Request is not JSON")
            return jsonify({
                'error': 'Request must be JSON',
                'code': 400,
                'type': 'invalid_content_type'
            }), 400
        
        try:
            request.get_json()
        except Exception as e:
            logger.warning(f"{func.__name__}: Invalid JSON: {str(e)}")
            return jsonify({
                'error': 'Invalid JSON format',
                'code': 400,
                'type': 'invalid_json'
            }), 400
        
        return func(*args, **kwargs)
    
    return wrapper


def validate_required_fields(required_fields: list) -> Callable:
    """
    Decorator factory to validate required JSON fields
    
    Usage:
        @app.route('/api/products', methods=['POST'])
        @require_json
        @validate_required_fields(['name', 'price', 'type'])
        @handle_errors
        def create_product():
            data = request.get_json()
            # Route logic
            pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            data = request.get_json() or {}
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                logger.warning(f"{func.__name__}: Missing fields: {missing_fields}")
                return jsonify({
                    'error': f"Missing required fields: {', '.join(missing_fields)}",
                    'code': 400,
                    'type': 'missing_fields'
                }), 400
            
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator


def log_request(func: Callable) -> Callable:
    """
    Decorator to log incoming requests
    
    Usage:
        @app.route('/api/products')
        @log_request
        def get_products():
            # Route logic
            pass
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.info(f"{request.method} {request.path} - {func.__name__}")
        # Only try to get JSON if the request actually has a body and is JSON
        if request.is_json and request.method in ['POST', 'PUT', 'PATCH']:
            try:
                logger.debug(f"Request data: {request.get_json()}")
            except Exception as e:
                logger.debug(f"Could not parse JSON request: {str(e)}")
        return func(*args, **kwargs)
    
    return wrapper
