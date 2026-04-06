"""
Employees Routes
CRUD operations for Employee entities in Orion
"""

import logging
import uuid
from flask import Blueprint, request, jsonify

from services.orion_service import OrionService
from utils.helpers import format_success_response, format_error_response, paginate_results
from utils.validators import validate_email
from utils.decorators import handle_errors, require_json, log_request

logger = logging.getLogger(__name__)

employees_bp = Blueprint('employees', __name__, url_prefix='/api/v1/employees')


def get_orion_service() -> OrionService:
    """Get OrionService from app context"""
    from flask import current_app
    return current_app.orion_service


@employees_bp.route('', methods=['GET'])
@log_request
def list_employees():
    """List all employees with pagination"""
    try:
        limit = request.args.get('limit', 100, type=int)
        page = request.args.get('page', 1, type=int)
        
        orion = get_orion_service()
        result = orion.list_entities(entity_type='Employee', limit=1000)
        
        if not result.get('success'):
            return jsonify(format_error_response("Failed to fetch employees")), 400
        
        employees = result.get('entities', [])
        paginated = paginate_results(employees, page, limit)
        
        return jsonify(format_success_response(
            message="Employees listed",
            data={
                'employees': paginated['items'],
                'count': len(paginated['items']),
                'total': paginated['total'],
                'page': page,
                'pages': paginated['pages']
            }
        )), 200
        
    except Exception as e:
        logger.error(f"Error listing employees: {str(e)}")
        return jsonify(format_error_response(str(e))), 500


@employees_bp.route('/<employee_id>', methods=['GET'])
@log_request
def get_employee(employee_id: str):
    """Get a specific employee by ID"""
    try:
        if not employee_id.startswith('urn:'):
            employee_id = f"urn:ngsi-ld:Employee:{employee_id}"
        
        orion = get_orion_service()
        result = orion.get_entity(employee_id)
        
        if not result.get('success'):
            return jsonify(format_error_response("Employee not found")), 404
        
        return jsonify(format_success_response(
            message="Employee retrieved",
            data={'employee': result.get('entity')}
        )), 200
        
    except Exception as e:
        logger.error(f"Error getting employee {employee_id}: {str(e)}")
        return jsonify(format_error_response(str(e))), 500


@employees_bp.route('', methods=['POST'])
@require_json
@log_request
@handle_errors
def create_employee():
    """Create a new employee"""
    data = request.get_json()
    
    required = ['name', 'email']
    for field in required:
        if field not in data:
            return jsonify(format_error_response(f"Missing required field: {field}")), 400
    
    # Validate email
    is_valid, error = validate_email(data['email'])
    if not is_valid:
        return jsonify(format_error_response(error)), 400
    
    employee_id = f"urn:ngsi-ld:Employee:{uuid.uuid4().hex[:8].upper()}"
    
    entity = {
        'id': employee_id,
        'type': 'Employee',
        'name': {'type': 'Text', 'value': data['name']},
        'email': {'type': 'Text', 'value': data['email']}
    }
    
    # Optional fields
    for field in ['phone', 'department', 'position', 'storeId']:
        if field in data:
            entity[field] = {'type': 'Text', 'value': str(data[field])}
    
    orion = get_orion_service()
    result = orion.create_entity(entity)
    
    if not result.get('success'):
        return jsonify(format_error_response(f"Failed to create employee: {result.get('error')}")), 400
    
    return jsonify(format_success_response(
        message="Employee created",
        data={'id': employee_id}
    )), 201


@employees_bp.route('/<employee_id>', methods=['PATCH'])
@require_json
@log_request
@handle_errors
def update_employee(employee_id: str):
    """Update an employee"""
    data = request.get_json()
    
    if not employee_id.startswith('urn:'):
        employee_id = f"urn:ngsi-ld:Employee:{employee_id}"
    
    # Validate email if provided
    if 'email' in data:
        is_valid, error = validate_email(data['email'])
        if not is_valid:
            return jsonify(format_error_response(error)), 400
    
    updates = {}
    for field in ['name', 'email', 'phone', 'department', 'position', 'storeId']:
        if field in data:
            updates[field] = {'type': 'Text', 'value': str(data[field])}
    
    if not updates:
        return jsonify(format_error_response("No fields to update")), 400
    
    orion = get_orion_service()
    result = orion.update_entity(employee_id, updates)
    
    if not result.get('success'):
        return jsonify(format_error_response(f"Failed to update employee: {result.get('error')}")), 400
    
    return jsonify(format_success_response(
        message="Employee updated",
        data={'employee_id': employee_id}
    )), 200


@employees_bp.route('/<employee_id>', methods=['DELETE'])
@log_request
@handle_errors
def delete_employee(employee_id: str):
    """Delete an employee"""
    if not employee_id.startswith('urn:'):
        employee_id = f"urn:ngsi-ld:Employee:{employee_id}"
    
    orion = get_orion_service()
    result = orion.delete_entity(employee_id)
    
    if not result.get('success'):
        return jsonify(format_error_response(f"Failed to delete employee: {result.get('error')}")), 400
    
    return jsonify(format_success_response(
        message="Employee deleted",
        data={'employee_id': employee_id}
    )), 200
