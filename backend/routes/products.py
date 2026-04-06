"""
Products Routes
CRUD operations for Product entities in Orion
"""

import logging
import uuid
from flask import Blueprint, request, jsonify
from typing import Dict, Any, Tuple

from services.orion_service import OrionService
from utils.helpers import format_success_response, format_error_response, paginate_results
from utils.validators import validate_price, validate_entity_id
from utils.decorators import handle_errors, require_json, log_request

logger = logging.getLogger(__name__)

products_bp = Blueprint('products', __name__, url_prefix='/api/v1/products')


def get_orion_service() -> OrionService:
    """Get OrionService from app context"""
    from flask import current_app
    return current_app.orion_service


@products_bp.route('', methods=['GET'])
@log_request
def list_products():
    """
    List all products with optional filtering
    
    Query parameters:
    - type: Filter by entity type (default: Product)
    - limit: Max results (default: 100)
    - page: Page number (default: 1)
    - name: Search by name (partial match)
    - minPrice: Filter by minimum price
    - maxPrice: Filter by maximum price
    
    Returns:
        JSON list of products with pagination
    """
    try:
        limit = request.args.get('limit', 100, type=int)
        page = request.args.get('page', 1, type=int)
        name_filter = request.args.get('name', '', type=str).lower()
        min_price = request.args.get('minPrice', type=float)
        max_price = request.args.get('maxPrice', type=float)
        
        # Get products from Orion
        orion = get_orion_service()
        result = orion.list_entities(entity_type='Product', limit=1000)
        
        if not result.get('success'):
            return jsonify(format_error_response("Failed to fetch products")), 400
        
        products = result.get('entities', [])
        
        # Apply filters
        filtered = []
        for product in products:
            # Name filter
            if name_filter:
                product_name = product.get('name', {}).get('value', '').lower()
                if name_filter not in product_name:
                    continue
            
            # Price filters
            price = product.get('price', {}).get('value', 0)
            if min_price is not None and price < min_price:
                continue
            if max_price is not None and price > max_price:
                continue
            
            filtered.append(product)
        
        # Paginate
        paginated = paginate_results(filtered, page, limit)
        
        return jsonify(format_success_response(
            message="Products listed",
            data={
                'products': paginated['items'],
                'count': len(paginated['items']),
                'total': paginated['total'],
                'page': page,
                'pages': paginated['pages']
            }
        )), 200
        
    except Exception as e:
        logger.error(f"Error listing products: {str(e)}")
        return jsonify(format_error_response(str(e))), 500


@products_bp.route('/<product_id>', methods=['GET'])
@log_request
def get_product(product_id: str):
    """
    Get a specific product by ID
    
    Args:
        product_id: Product identifier
        
    Returns:
        JSON product data
    """
    try:
        # Validate ID format
        is_valid, error = validate_entity_id(product_id)
        if not is_valid:
            return jsonify(format_error_response(error)), 400
        
        # Build full URN if needed
        if not product_id.startswith('urn:'):
            product_id = f"urn:ngsi-ld:Product:{product_id}"
        
        orion = get_orion_service()
        result = orion.get_entity(product_id)
        
        if not result.get('success'):
            return jsonify(format_error_response("Product not found")), 404
        
        return jsonify(format_success_response(
            message="Product retrieved",
            data={'product': result.get('entity')}
        )), 200
        
    except Exception as e:
        logger.error(f"Error getting product {product_id}: {str(e)}")
        return jsonify(format_error_response(str(e))), 500


@products_bp.route('', methods=['POST'])
@require_json
@log_request
@handle_errors
def create_product():
    """
    Create a new product
    
    Required fields:
    - name (string)
    - price (number > 0)
    - type (default: Product)
    
    Optional fields:
    - size, color, originCountry, image
    
    Returns:
        JSON with created product ID
    """
    data = request.get_json()
    
    # Validate required fields
    required = ['name', 'price']
    for field in required:
        if field not in data:
            return jsonify(format_error_response(f"Missing required field: {field}")), 400
    
    # Validate price
    is_valid, error = validate_price(data['price'])
    if not is_valid:
        return jsonify(format_error_response(error)), 400
    
    # Build entity with unique ID
    product_id = f"urn:ngsi-ld:Product:{uuid.uuid4().hex[:8].upper()}"
    
    entity = {
        'id': product_id,
        'type': 'Product',
        'name': {'type': 'Text', 'value': data['name']},
        'price': {'type': 'Number', 'value': float(data['price'])}
    }
    
    # Add optional fields
    for field in ['size', 'color', 'originCountry', 'image']:
        if field in data:
            entity[field] = {'type': 'Text', 'value': str(data[field])}
    
    orion = get_orion_service()
    result = orion.create_entity(entity)
    
    if not result.get('success'):
        return jsonify(format_error_response(f"Failed to create product: {result.get('error')}")), 400
    
    return jsonify(format_success_response(
        message="Product created",
        data={'id': product_id}
    )), 201


@products_bp.route('/<product_id>', methods=['PATCH'])
@require_json
@log_request
@handle_errors
def update_product(product_id: str):
    """
    Update a product
    
    Args:
        product_id: Product identifier
        
    Request body: Fields to update
    
    Returns:
        JSON success message
    """
    data = request.get_json()
    
    # Build full URN if needed
    if not product_id.startswith('urn:'):
        product_id = f"urn:ngsi-ld:Product:{product_id}"
    
    # Validate price if provided
    if 'price' in data:
        is_valid, error = validate_price(data['price'])
        if not is_valid:
            return jsonify(format_error_response(error)), 400
    
    # Build updates dict
    updates = {}
    for field in ['name', 'price', 'size', 'color', 'originCountry', 'image']:
        if field in data:
            value = data[field]
            if field == 'price':
                updates[field] = {'type': 'Number', 'value': float(value)}
            else:
                updates[field] = {'type': 'Text', 'value': str(value)}
    
    if not updates:
        return jsonify(format_error_response("No fields to update")), 400
    
    orion = get_orion_service()
    result = orion.update_entity(product_id, updates)
    
    if not result.get('success'):
        return jsonify(format_error_response(f"Failed to update product: {result.get('error')}")), 400
    
    return jsonify(format_success_response(
        message="Product updated",
        data={'product_id': product_id}
    )), 200


@products_bp.route('/<product_id>', methods=['DELETE'])
@log_request
@handle_errors
def delete_product(product_id: str):
    """
    Delete a product
    
    Args:
        product_id: Product identifier
        
    Returns:
        JSON success message
    """
    # Build full URN if needed
    if not product_id.startswith('urn:'):
        product_id = f"urn:ngsi-ld:Product:{product_id}"
    
    orion = get_orion_service()
    result = orion.delete_entity(product_id)
    
    if not result.get('success'):
        return jsonify(format_error_response(f"Failed to delete product: {result.get('error')}")), 400
    
    return jsonify(format_success_response(
        message="Product deleted",
        data={'product_id': product_id}
    )), 200
