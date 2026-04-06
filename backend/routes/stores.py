"""
Stores Routes
CRUD operations for Store entities in Orion
"""

import logging
import uuid
from flask import Blueprint, request, jsonify

from services.orion_service import OrionService
from utils.helpers import format_success_response, format_error_response, paginate_results
from utils.decorators import handle_errors, require_json, log_request

logger = logging.getLogger(__name__)

stores_bp = Blueprint('stores', __name__, url_prefix='/api/v1/stores')


def get_orion_service() -> OrionService:
    """Get OrionService from app context"""
    from flask import current_app
    return current_app.orion_service


@stores_bp.route('', methods=['GET'])
@log_request
def list_stores():
    """List all stores with pagination"""
    try:
        limit = request.args.get('limit', 100, type=int)
        page = request.args.get('page', 1, type=int)
        
        orion = get_orion_service()
        result = orion.list_entities(entity_type='Store', limit=1000)
        
        if not result.get('success'):
            return jsonify(format_error_response("Failed to fetch stores")), 400
        
        stores = result.get('entities', [])
        paginated = paginate_results(stores, page, limit)
        
        return jsonify(format_success_response(
            message="Stores listed",
            data={
                'stores': paginated['items'],
                'count': len(paginated['items']),
                'total': paginated['total'],
                'page': page,
                'pages': paginated['pages']
            }
        )), 200
        
    except Exception as e:
        logger.error(f"Error listing stores: {str(e)}")
        return jsonify(format_error_response(str(e))), 500


@stores_bp.route('/<store_id>', methods=['GET'])
@log_request
def get_store(store_id: str):
    """Get a specific store by ID"""
    try:
        if not store_id.startswith('urn:'):
            store_id = f"urn:ngsi-ld:Store:{store_id}"
        
        orion = get_orion_service()
        result = orion.get_entity(store_id)
        
        if not result.get('success'):
            return jsonify(format_error_response("Store not found")), 404
        
        return jsonify(format_success_response(
            message="Store retrieved",
            data={'store': result.get('entity')}
        )), 200
        
    except Exception as e:
        logger.error(f"Error getting store {store_id}: {str(e)}")
        return jsonify(format_error_response(str(e))), 500


@stores_bp.route('', methods=['POST'])
@require_json
@log_request
@handle_errors
def create_store():
    """Create a new store"""
    data = request.get_json()
    
    if 'name' not in data:
        return jsonify(format_error_response("Missing required field: name")), 400
    
    store_id = f"urn:ngsi-ld:Store:{uuid.uuid4().hex[:8].upper()}"
    
    entity = {
        'id': store_id,
        'type': 'Store',
        'name': {'type': 'Text', 'value': data['name']}
    }
    
    # Optional fields
    for field in ['address', 'city', 'country', 'phone', 'email']:
        if field in data:
            entity[field] = {'type': 'Text', 'value': str(data[field])}
    
    orion = get_orion_service()
    result = orion.create_entity(entity)
    
    if not result.get('success'):
        return jsonify(format_error_response(f"Failed to create store: {result.get('error')}")), 400
    
    return jsonify(format_success_response(
        message="Store created",
        data={'id': store_id}
    )), 201


@stores_bp.route('/<store_id>', methods=['PATCH'])
@require_json
@log_request
@handle_errors
def update_store(store_id: str):
    """Update a store"""
    data = request.get_json()
    
    if not store_id.startswith('urn:'):
        store_id = f"urn:ngsi-ld:Store:{store_id}"
    
    updates = {}
    for field in ['name', 'address', 'city', 'country', 'phone', 'email']:
        if field in data:
            updates[field] = {'type': 'Text', 'value': str(data[field])}
    
    if not updates:
        return jsonify(format_error_response("No fields to update")), 400
    
    orion = get_orion_service()
    result = orion.update_entity(store_id, updates)
    
    if not result.get('success'):
        return jsonify(format_error_response(f"Failed to update store: {result.get('error')}")), 400
    
    return jsonify(format_success_response(
        message="Store updated",
        data={'store_id': store_id}
    )), 200


@stores_bp.route('/<store_id>', methods=['DELETE'])
@log_request
@handle_errors
def delete_store(store_id: str):
    """Delete a store"""
    if not store_id.startswith('urn:'):
        store_id = f"urn:ngsi-ld:Store:{store_id}"
    
    orion = get_orion_service()
    result = orion.delete_entity(store_id)
    
    if not result.get('success'):
        return jsonify(format_error_response(f"Failed to delete store: {result.get('error')}")), 400
    
    return jsonify(format_success_response(
        message="Store deleted",
        data={'store_id': store_id}
    )), 200
