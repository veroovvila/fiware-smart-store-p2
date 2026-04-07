"""
Orion Context Broker Service
Handles CRUD operations for NGSIv2 entities
Phase 2: Basic structure without real Orion connection
"""

import logging
import requests
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class OrionService:
    """
    Service class for interacting with FIWARE Orion Context Broker
    Implements NGSIv2 API operations
    
    Note: In Phase 2, this is a base structure without real HTTP calls
    Real Orion integration will happen in Phase 3
    """
    
    def __init__(self, orion_url: str = 'http://localhost:1026'):
        """
        Initialize OrionService
        
        Args:
            orion_url: Base URL of Orion Context Broker
        """
        self.base_url = orion_url
        self.api_url = f"{orion_url}/v2"
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        logger.info(f"OrionService initialized with URL: {orion_url}")
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check Orion health status
        
        Returns:
            Dictionary with health status information
        """
        try:
            # GET requests should not include Content-Type header
            get_headers = {'Accept': 'application/json'}
            response = requests.get(
                f"{self.base_url}/version",
                headers=get_headers,
                timeout=5
            )
            if response.status_code == 200:
                logger.info("Orion is healthy")
                return {
                    'status': 'healthy',
                    'orion_version': response.json()
                }
            else:
                logger.error(f"Orion health check failed: {response.status_code}")
                return {
                    'status': 'unhealthy',
                    'error': f"HTTP {response.status_code}"
                }
        except requests.exceptions.RequestException as e:
            logger.error(f"Orion connection error: {str(e)}")
            return {
                'status': 'unreachable',
                'error': str(e)
            }
    
    def create_entity(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new NGSIv2 entity in Orion
        
        Args:
            entity: Entity data in NGSIv2 format
            
        Returns:
            Response dictionary with status
            
        Example entity:
            {
                "id": "urn:ngsi-ld:Product:P001",
                "type": "Product",
                "name": {"type": "Text", "value": "Coffee"},
                "price": {"type": "Number", "value": 12.99}
            }
        """
        if not entity or 'id' not in entity or 'type' not in entity:
            logger.error("Invalid entity: missing 'id' or 'type'")
            return {
                'success': False,
                'error': "Entity must have 'id' and 'type'"
            }
        
        try:
            logger.info(f"Creating entity: {entity.get('id')}")
            response = requests.post(
                f"{self.api_url}/entities",
                json=entity,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code in [201, 204]:
                logger.info(f"✓ Entity created: {entity.get('id')}")
                return {
                    'success': True,
                    'entity_id': entity.get('id'),
                    'message': 'Entity created successfully'
                }
            else:
                logger.error(f"✗ Failed to create entity: HTTP {response.status_code}")
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}: {response.text}"
                }
        except Exception as e:
            logger.error(f"Error creating entity: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_entity(self, entity_id: str) -> Dict[str, Any]:
        """
        Retrieve an entity by ID
        
        Args:
            entity_id: NGSIv2 entity ID
            
        Returns:
            Entity data or error dictionary
        """
        if not entity_id:
            logger.error("Invalid entity_id")
            return {
                'success': False,
                'error': 'entity_id is required'
            }
        
        try:
            logger.info(f"Retrieving entity: {entity_id}")
            # GET requests should not include Content-Type header
            get_headers = {'Accept': 'application/json'}
            response = requests.get(
                f"{self.api_url}/entities/{entity_id}",
                headers=get_headers,
                timeout=5
            )
            
            if response.status_code == 200:
                logger.info(f"✓ Entity retrieved: {entity_id}")
                return {
                    'success': True,
                    'entity': response.json(),
                    'message': 'Entity retrieved successfully'
                }
            else:
                logger.error(f"✗ Failed to retrieve entity: HTTP {response.status_code}")
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}"
                }
        except Exception as e:
            logger.error(f"Error retrieving entity: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def update_entity(self, entity_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing entity
        
        Args:
            entity_id: NGSIv2 entity ID
            updates: Dictionary with fields to update
            
        Returns:
            Response dictionary with status
        """
        if not entity_id or not updates:
            logger.error("Invalid parameters for update")
            return {
                'success': False,
                'error': 'entity_id and updates are required'
            }
        
        try:
            logger.info(f"Updating entity: {entity_id}")
            response = requests.patch(
                f"{self.api_url}/entities/{entity_id}/attrs",
                json=updates,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code in [204, 200]:
                logger.info(f"✓ Entity updated: {entity_id}")
                return {
                    'success': True,
                    'entity_id': entity_id,
                    'updates': updates,
                    'message': 'Entity updated successfully'
                }
            else:
                logger.error(f"✗ Failed to update entity: HTTP {response.status_code}")
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}"
                }
        except Exception as e:
            logger.error(f"Error updating entity: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def delete_entity(self, entity_id: str) -> Dict[str, Any]:
        """
        Delete an entity
        
        Args:
            entity_id: NGSIv2 entity ID
            
        Returns:
            Response dictionary with status
        """
        if not entity_id:
            logger.error("Invalid entity_id")
            return {
                'success': False,
                'error': 'entity_id is required'
            }
        
        try:
            logger.info(f"Deleting entity: {entity_id}")
            # DELETE requests should not include Content-Type header
            delete_headers = {'Accept': 'application/json'}
            response = requests.delete(
                f"{self.api_url}/entities/{entity_id}",
                headers=delete_headers,
                timeout=10
            )
            
            if response.status_code in [204, 200]:
                logger.info(f"✓ Entity deleted: {entity_id}")
                return {
                    'success': True,
                    'entity_id': entity_id,
                    'message': 'Entity deleted successfully'
                }
            else:
                logger.error(f"✗ Failed to delete entity: HTTP {response.status_code}")
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}"
                }
        except Exception as e:
            logger.error(f"Error deleting entity: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_entities(self, entity_type: Optional[str] = None, limit: int = 100) -> Dict[str, Any]:
        """
        List entities, optionally filtered by type
        
        Args:
            entity_type: Filter by entity type (e.g., 'Product', 'Store')
            limit: Maximum number of entities to return
            
        Returns:
            List of entities or error dictionary
        """
        try:
            logger.info(f"Listing entities (type: {entity_type}, limit: {limit})")
            
            params = {'limit': limit}
            if entity_type:
                params['type'] = entity_type
            
            # GET requests should not include Content-Type header
            get_headers = {'Accept': 'application/json'}
            response = requests.get(
                f"{self.api_url}/entities",
                params=params,
                headers=get_headers,
                timeout=10
            )
            
            if response.status_code == 200:
                entities = response.json()
                logger.info(f"✓ Retrieved {len(entities)} entities")
                return {
                    'success': True,
                    'entity_type': entity_type,
                    'limit': limit,
                    'entities': entities,
                    'count': len(entities),
                    'message': 'Entities retrieved successfully'
                }
            else:
                logger.error(f"✗ Failed to list entities: HTTP {response.status_code}")
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}",
                    'entities': [],
                    'count': 0
                }
        except Exception as e:
            logger.error(f"Error listing entities: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'entities': [],
                'count': 0
            }

