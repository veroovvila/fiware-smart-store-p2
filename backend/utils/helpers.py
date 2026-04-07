"""
Helper Functions Module
Common utility functions for data processing and formatting
Phase 2: Basic helper functions for Phase 3+ implementation
"""

import logging
from typing import Any, Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)


def format_entity_response(entity_id: str, entity_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format an entity into standard response format
    
    Args:
        entity_id: Entity ID
        entity_type: Entity type
        data: Entity data
        
    Returns:
        Formatted entity dictionary
    """
    return {
        'id': entity_id,
        'type': entity_type,
        'data': data,
        'timestamp': datetime.utcnow().isoformat()
    }


def format_error_response(error: str, code: int = 400) -> Dict[str, Any]:
    """
    Format an error response
    
    Args:
        error: Error message
        code: HTTP error code
        
    Returns:
        Formatted error dictionary
    """
    return {
        'error': error,
        'code': code,
        'timestamp': datetime.utcnow().isoformat()
    }


def format_success_response(message: str, data: Any = None) -> Dict[str, Any]:
    """
    Format a success response
    
    Args:
        message: Success message
        data: Optional data payload
        
    Returns:
        Formatted success dictionary
    """
    response = {
        'success': True,
        'message': message,
        'timestamp': datetime.utcnow().isoformat()
    }
    if data is not None:
        response['data'] = data
    return response


def convert_to_ngsi_format(entity_type: str, attributes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert plain attributes to NGSIv2 format
    
    Args:
        entity_type: Type of entity
        attributes: Dictionary of attributes
        
    Returns:
        NGSIv2 formatted entity
        
    Example:
        Input: {'name': 'Coffee', 'price': 12.99}
        Output: {'name': {'type': 'Text', 'value': 'Coffee'}, 'price': {'type': 'Number', 'value': 12.99}}
    """
    ngsi_attributes = {}
    for key, value in attributes.items():
        ngsi_type = infer_attribute_type(value)
        ngsi_attributes[key] = {
            'type': ngsi_type,
            'value': value
        }
    return ngsi_attributes


def infer_attribute_type(value: Any) -> str:
    """
    Infer NGSIv2 attribute type from Python value
    
    Args:
        value: Python value
        
    Returns:
        NGSIv2 type string
    """
    if isinstance(value, bool):
        return 'Boolean'
    elif isinstance(value, int):
        return 'Number'
    elif isinstance(value, float):
        return 'Number'
    elif isinstance(value, list):
        return 'array'
    elif isinstance(value, dict):
        return 'StructuredValue'
    else:
        return 'Text'


def paginate_results(items: List[Any], page: int = 1, limit: int = 100) -> Dict[str, Any]:
    """
    Paginate a list of items
    
    Args:
        items: List to paginate
        page: Page number (1-indexed)
        limit: Items per page
        
    Returns:
        Dictionary with paginated results
    """
    if page < 1:
        page = 1
    if limit < 1:
        limit = 100
    
    total = len(items)
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    
    return {
        'items': items[start_idx:end_idx],
        'page': page,
        'limit': limit,
        'total': total,
        'pages': (total + limit - 1) // limit
    }
