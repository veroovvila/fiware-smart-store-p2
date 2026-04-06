"""
Inventory Routes
CRUD operations for InventoryItem entities in Orion
Includes special endpoint for purchasing items
"""

import logging
import uuid
from flask import Blueprint, request, jsonify
from datetime import datetime, timezone

from services.orion_service import OrionService
from utils.helpers import format_success_response, format_error_response, paginate_results
from utils.validators import validate_quantity
from utils.decorators import handle_errors, require_json, log_request

logger = logging.getLogger(__name__)

inventory_bp = Blueprint('inventory', __name__, url_prefix='/api/v1/inventory')


def get_orion_service() -> OrionService:
    """Get OrionService from app context"""
    from flask import current_app
    return current_app.orion_service


@inventory_bp.route('', methods=['GET'])
@log_request
def list_inventory():
    """List all inventory items with optional filtering"""
    try:
        limit = request.args.get('limit', 100, type=int)
        page = request.args.get('page', 1, type=int)
        low_stock = request.args.get('lowStock', False, type=lambda x: x.lower() == 'true')
        product_id = request.args.get('productId', '', type=str)
        store_id = request.args.get('storeId', '', type=str)
        
        orion = get_orion_service()
        result = orion.list_entities(entity_type='InventoryItem', limit=1000)
        
        if not result.get('success'):
            return jsonify(format_error_response("Failed to fetch inventory")), 400
        
        items = result.get('entities', [])
        
        # Apply filters
        filtered = []
        for item in items:
            # Product filter
            if product_id:
                item_product = item.get('productId', {}).get('value', '')
                if product_id not in item_product:
                    continue
            
            # Store filter
            if store_id:
                item_store = item.get('storeId', {}).get('value', '')
                if store_id not in item_store:
                    continue
            
            # Low stock filter
            if low_stock:
                quantity = item.get('quantity', {}).get('value', 0)
                if quantity >= 10:  # Threshold
                    continue
            
            filtered.append(item)
        
        paginated = paginate_results(filtered, page, limit)
        
        return jsonify(format_success_response(
            message="Inventory items listed",
            data={
                'items': paginated['items'],
                'count': len(paginated['items']),
                'total': paginated['total'],
                'page': page,
                'pages': paginated['pages']
            }
        )), 200
        
    except Exception as e:
        logger.error(f"Error listing inventory: {str(e)}")
        return jsonify(format_error_response(str(e))), 500


@inventory_bp.route('/<item_id>', methods=['GET'])
@log_request
def get_inventory_item(item_id: str):
    """Get a specific inventory item by ID"""
    try:
        if not item_id.startswith('urn:'):
            item_id = f"urn:ngsi-ld:InventoryItem:{item_id}"
        
        orion = get_orion_service()
        result = orion.get_entity(item_id)
        
        if not result.get('success'):
            return jsonify(format_error_response("Inventory item not found")), 404
        
        return jsonify(format_success_response(
            message="Inventory item retrieved",
            data={'item': result.get('entity')}
        )), 200
        
    except Exception as e:
        logger.error(f"Error getting inventory item {item_id}: {str(e)}")
        return jsonify(format_error_response(str(e))), 500


@inventory_bp.route('', methods=['POST'])
@require_json
@log_request
@handle_errors
def create_inventory_item():
    """Create a new inventory item"""
    data = request.get_json()
    
    required = ['productId', 'storeId', 'quantity']
    for field in required:
        if field not in data:
            return jsonify(format_error_response(f"Missing required field: {field}")), 400
    
    # Validate quantity
    is_valid, error = validate_quantity(data['quantity'])
    if not is_valid:
        return jsonify(format_error_response(error)), 400
    
    item_id = f"urn:ngsi-ld:InventoryItem:{uuid.uuid4().hex[:8].upper()}"
    
    entity = {
        'id': item_id,
        'type': 'InventoryItem',
        'productId': {'type': 'Text', 'value': str(data['productId'])},
        'storeId': {'type': 'Text', 'value': str(data['storeId'])},
        'quantity': {'type': 'Number', 'value': int(data['quantity'])},
        'lastRestockDate': {'type': 'DateTime', 'value': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}
    }
    
    # Optional fields
    if 'shelf' in data:
        entity['shelf'] = {'type': 'Text', 'value': str(data['shelf'])}
    
    orion = get_orion_service()
    result = orion.create_entity(entity)
    
    if not result.get('success'):
        return jsonify(format_error_response(f"Failed to create inventory item: {result.get('error')}")), 400
    
    return jsonify(format_success_response(
        message="Inventory item created",
        data={'id': item_id}
    )), 201


@inventory_bp.route('/<item_id>', methods=['PATCH'])
@require_json
@log_request
@handle_errors
def update_inventory_item(item_id: str):
    """Update an inventory item"""
    data = request.get_json()
    
    if not item_id.startswith('urn:'):
        item_id = f"urn:ngsi-ld:InventoryItem:{item_id}"
    
    # Validate quantity if provided
    if 'quantity' in data:
        is_valid, error = validate_quantity(data['quantity'])
        if not is_valid:
            return jsonify(format_error_response(error)), 400
    
    updates = {}
    for field in ['productId', 'storeId', 'quantity', 'shelf']:
        if field in data:
            if field == 'quantity':
                updates[field] = {'type': 'Number', 'value': int(data[field])}
            else:
                updates[field] = {'type': 'Text', 'value': str(data[field])}
    
    if not updates:
        return jsonify(format_error_response("No fields to update")), 400
    
    orion = get_orion_service()
    result = orion.update_entity(item_id, updates)
    
    if not result.get('success'):
        return jsonify(format_error_response(f"Failed to update inventory item: {result.get('error')}")), 400
    
    return jsonify(format_success_response(
        message="Inventory item updated",
        data={'item_id': item_id}
    )), 200


@inventory_bp.route('/<item_id>/buy', methods=['PATCH'])
@require_json
@log_request
@handle_errors
def buy_from_inventory(item_id: str):
    """
    Special endpoint: Purchase items from inventory
    Decreases quantity by amount specified
    
    Request body:
    - amount: Number of items to buy (required)
    
    Returns:
        Updated inventory item
    """
    data = request.get_json()
    
    if 'amount' not in data:
        return jsonify(format_error_response("Missing required field: amount")), 400
    
    # Validate amount
    is_valid, error = validate_quantity(data['amount'])
    if not is_valid:
        return jsonify(format_error_response(error)), 400
    
    if not item_id.startswith('urn:'):
        item_id = f"urn:ngsi-ld:InventoryItem:{item_id}"
    
    # Get current item
    orion = get_orion_service()
    get_result = orion.get_entity(item_id)
    
    if not get_result.get('success'):
        return jsonify(format_error_response("Inventory item not found")), 404
    
    entity = get_result.get('entity', {})
    current_quantity = entity.get('quantity', {}).get('value', 0)
    amount = int(data['amount'])
    
    # Check sufficient stock
    if current_quantity < amount:
        return jsonify(format_error_response(
            f"Insufficient stock. Available: {current_quantity}, Requested: {amount}"
        )), 400
    
    # Update quantity
    new_quantity = current_quantity - amount
    updates = {
        'quantity': {'type': 'Number', 'value': new_quantity},
        'lastSaleDate': {'type': 'DateTime', 'value': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}
    }
    
    update_result = orion.update_entity(item_id, updates)
    
    if not update_result.get('success'):
        return jsonify(format_error_response(f"Failed to process purchase: {update_result.get('error')}")), 400
    
    return jsonify(format_success_response(
        message="Purchase completed",
        data={
            'item_id': item_id,
            'amount_sold': amount,
            'previous_quantity': current_quantity,
            'new_quantity': new_quantity
        }
    )), 200


@inventory_bp.route('/<item_id>', methods=['DELETE'])
@log_request
@handle_errors
def delete_inventory_item(item_id: str):
    """Delete an inventory item"""
    if not item_id.startswith('urn:'):
        item_id = f"urn:ngsi-ld:InventoryItem:{item_id}"
    
    orion = get_orion_service()
    result = orion.delete_entity(item_id)
    
    if not result.get('success'):
        return jsonify(format_error_response(f"Failed to delete inventory item: {result.get('error')}")), 400
    
    return jsonify(format_success_response(
        message="Inventory item deleted",
        data={'item_id': item_id}
    )), 200
