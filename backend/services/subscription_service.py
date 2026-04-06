"""
Subscription Service
Manages FIWARE Orion subscriptions for entities
Phase 3: Real Orion integration with HTTP calls
"""

import logging
import requests
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class SubscriptionService:
    """
    Service class for managing Orion subscriptions
    Handles creation and deletion of subscriptions
    Phase 3: Makes real HTTP calls to Orion
    """
    
    def __init__(self, orion_url: str = 'http://localhost:1026'):
        """
        Initialize SubscriptionService
        
        Args:
            orion_url: Base URL of Orion Context Broker
        """
        self.base_url = orion_url
        self.api_url = f"{orion_url}/v2"
        self.headers = {'Accept': 'application/json'}
        self.post_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        logger.info(f"SubscriptionService initialized with URL: {orion_url}")
    
    def create_subscription(self, subscription_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new subscription in Orion
        
        Args:
            subscription_data: Subscription configuration
            
        Returns:
            Response dictionary with subscription ID
        """
        try:
            description = subscription_data.get('description', 'Unnamed subscription')
            logger.info(f"Creating subscription: {description}")
            
            response = requests.post(
                f"{self.api_url}/subscriptions",
                json=subscription_data,
                headers=self.post_headers,
                timeout=10
            )
            
            if response.status_code in [201, 204]:
                subscription_id = response.headers.get('Location', '').split('/')[-1]
                logger.info(f"✓ Subscription created: {subscription_id}")
                return {
                    'success': True,
                    'subscription_id': subscription_id,
                    'message': 'Subscription created successfully'
                }
            else:
                logger.error(f"✗ Failed to create subscription: HTTP {response.status_code}")
                logger.error(f"Response: {response.text}")
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}: {response.text}"
                }
        except Exception as e:
            logger.error(f"Error creating subscription: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def delete_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """
        Delete a subscription from Orion
        
        Args:
            subscription_id: ID of subscription to delete
            
        Returns:
            Response dictionary with status
        """
        try:
            logger.info(f"Deleting subscription: {subscription_id}")
            response = requests.delete(
                f"{self.api_url}/subscriptions/{subscription_id}",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code in [204, 200]:
                logger.info(f"✓ Subscription deleted: {subscription_id}")
                return {
                    'success': True,
                    'subscription_id': subscription_id,
                    'message': 'Subscription deleted successfully'
                }
            else:
                logger.error(f"✗ Failed to delete subscription: HTTP {response.status_code}")
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}"
                }
        except Exception as e:
            logger.error(f"Error deleting subscription: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_subscriptions(self) -> Dict[str, Any]:
        """
        List all subscriptions from Orion
        
        Returns:
            List of subscriptions
        """
        try:
            logger.info("Listing subscriptions")
            response = requests.get(
                f"{self.api_url}/subscriptions",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                subscriptions = response.json()
                logger.info(f"✓ Retrieved {len(subscriptions)} subscriptions")
                return {
                    'success': True,
                    'count': len(subscriptions),
                    'subscriptions': subscriptions
                }
            else:
                logger.error(f"✗ Failed to list subscriptions: HTTP {response.status_code}")
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}",
                    'count': 0,
                    'subscriptions': []
                }
        except Exception as e:
            logger.error(f"Error listing subscriptions: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'count': 0,
                'subscriptions': []
            }
