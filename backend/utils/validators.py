"""
Validators Module
Input validation functions for request data
Phase 2: Basic validators for common data types
"""

import logging
import re
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

# Regex patterns
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
HEX_COLOR_PATTERN = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
VALID_SIZES = {'S', 'M', 'L', 'XL'}


def validate_price(price: float) -> Tuple[bool, Optional[str]]:
    """
    Validate product price
    
    Args:
        price: Price value
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        price_float = float(price)
        if price_float <= 0:
            return False, "Price must be greater than 0"
        if price_float > 1000000:  # Sanity check
            return False, "Price exceeds maximum allowed value"
        return True, None
    except (ValueError, TypeError):
        return False, "Price must be a valid number"


def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """
    Validate email address
    
    Args:
        email: Email address
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not email or not isinstance(email, str):
        return False, "Email must be a non-empty string"
    
    if len(email) > 254:  # RFC 5321
        return False, "Email address is too long"
    
    if re.match(EMAIL_PATTERN, email):
        return True, None
    else:
        return False, "Invalid email format"


def validate_color_hex(color: str) -> Tuple[bool, Optional[str]]:
    """
    Validate hexadecimal color code
    
    Args:
        color: Color hex code (e.g., '#FF0000')
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not color or not isinstance(color, str):
        return False, "Color must be a non-empty string"
    
    if re.match(HEX_COLOR_PATTERN, color):
        return True, None
    else:
        return False, "Invalid hex color format. Use #RRGGBB or #RGB"


def validate_size(size: str) -> Tuple[bool, Optional[str]]:
    """
    Validate product size
    
    Args:
        size: Product size (S, M, L, XL)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not size or not isinstance(size, str):
        return False, "Size must be a non-empty string"
    
    size_upper = size.upper()
    if size_upper in VALID_SIZES:
        return True, None
    else:
        return False, f"Invalid size. Must be one of: {', '.join(VALID_SIZES)}"


def validate_quantity(quantity: int) -> Tuple[bool, Optional[str]]:
    """
    Validate product quantity
    
    Args:
        quantity: Quantity value
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        qty = int(quantity)
        if qty < 0:
            return False, "Quantity cannot be negative"
        if qty > 999999:
            return False, "Quantity exceeds maximum allowed value"
        return True, None
    except (ValueError, TypeError):
        return False, "Quantity must be a valid integer"


def validate_entity_id(entity_id: str) -> Tuple[bool, Optional[str]]:
    """
    Validate NGSIv2 entity ID
    
    Args:
        entity_id: Entity ID (e.g., 'urn:ngsi-ld:Product:P001')
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not entity_id or not isinstance(entity_id, str):
        return False, "Entity ID must be a non-empty string"
    
    if len(entity_id) > 256:
        return False, "Entity ID is too long"
    
    # NGSIv2 allows URNs and other ID formats
    if entity_id.startswith('urn:') or ':' in entity_id:
        return True, None
    else:
        return True, None  # Allow simple IDs too


def validate_entity_type(entity_type: str) -> Tuple[bool, Optional[str]]:
    """
    Validate NGSIv2 entity type
    
    Args:
        entity_type: Entity type (e.g., 'Product')
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not entity_type or not isinstance(entity_type, str):
        return False, "Entity type must be a non-empty string"
    
    if len(entity_type) > 100:
        return False, "Entity type is too long"
    
    # Simple alphanumeric check
    if entity_type.replace('_', '').replace('-', '').isalnum():
        return True, None
    else:
        return False, "Entity type must contain only alphanumeric characters, hyphens, and underscores"
