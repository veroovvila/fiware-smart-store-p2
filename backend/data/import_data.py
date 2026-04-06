"""
Orion Data Import Module
Loads initial data from JSON files and creates NGSIv2 entities in Orion
Registers external providers and creates subscriptions
"""

import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Any, Tuple

import requests

logger = logging.getLogger(__name__)


class OrionDataImporter:
    """Handles importing data into Orion Context Broker"""
    
    def __init__(self, orion_url: str, import_path: str = '/app/import-data'):
        """
        Initialize importer
        
        Args:
            orion_url: Base URL of Orion (e.g., http://localhost:1026)
            import_path: Path to JSON import files
        """
        self.orion_url = orion_url
        self.api_url = f"{orion_url}/v2"
        self.import_path = import_path
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.entities_created = 0
        self.entities_skipped = 0
    
    def _entity_exists(self, entity_id: str) -> bool:
        """Check if entity already exists in Orion"""
        try:
            response = requests.get(
                f"{self.api_url}/entities/{entity_id}",
                headers=self.headers,
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Error checking entity existence: {str(e)}")
            return False
    
    def _create_entity(self, entity: Dict[str, Any]) -> bool:
        """
        Create entity in Orion
        
        Args:
            entity: NGSIv2 entity data
            
        Returns:
            True if created, False otherwise
        """
        try:
            response = requests.post(
                f"{self.api_url}/entities",
                json=entity,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code in [201, 204]:
                logger.info(f"✓ Created entity: {entity['id']}")
                self.entities_created += 1
                return True
            else:
                logger.error(f"✗ Failed to create {entity['id']}: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"✗ Error creating entity {entity.get('id')}: {str(e)}")
            return False
    
    def import_file(self, filename: str, entity_type: str) -> Tuple[int, int]:
        """
        Import entities from JSON file
        
        Args:
            filename: JSON filename to import
            entity_type: Type of entity (e.g., 'Product')
            
        Returns:
            Tuple of (created_count, skipped_count)
        """
        file_path = os.path.join(self.import_path, filename)
        
        if not os.path.exists(file_path):
            logger.warning(f"File not found: {file_path}")
            return 0, 0
        
        try:
            with open(file_path, 'r') as f:
                entities = json.load(f)
            
            if not isinstance(entities, list):
                entities = [entities]
            
            created = 0
            skipped = 0
            
            logger.info(f"\n📂 Importing {filename} ({len(entities)} entities)...")
            
            for entity in entities:
                if not isinstance(entity, dict):
                    continue
                
                entity_id = entity.get('id')
                
                if self._entity_exists(entity_id):
                    logger.debug(f"⊘ Entity already exists: {entity_id}")
                    skipped += 1
                    self.entities_skipped += 1
                else:
                    if self._create_entity(entity):
                        created += 1
            
            logger.info(f"   Result: {created} created, {skipped} skipped")
            return created, skipped
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {filename}: {str(e)}")
            return 0, 0
        except Exception as e:
            logger.error(f"Error importing {filename}: {str(e)}")
            return 0, 0
    
    def register_providers(self, provider_service) -> int:
        """
        Register external data providers
        
        Args:
            provider_service: ProviderService instance
            
        Returns:
            Count of providers registered
        """
        providers = [
            {
                'name': 'temperatura',
                'description': 'Temperature data provider',
                'url': 'http://weather-api:8080/temperature',
                'type': 'weather'
            },
            {
                'name': 'humedad',
                'description': 'Humidity data provider',
                'url': 'http://weather-api:8080/humidity',
                'type': 'weather'
            },
            {
                'name': 'tweets',
                'description': 'Twitter data provider',
                'url': 'http://twitter-api:8080/tweets',
                'type': 'social'
            }
        ]
        
        logger.info("\n📡 Registering external providers...")
        registered = 0
        
        for provider in providers:
            result = provider_service.register_provider(provider['name'], provider)
            if result.get('success'):
                logger.info(f"✓ Registered provider: {provider['name']}")
                registered += 1
            else:
                logger.warning(f"⊘ Provider already registered: {provider['name']}")
        
        return registered
    
    def create_subscriptions(self, subscription_service, orion_url: str) -> int:
        """
        Create Orion subscriptions for notifications
        
        Args:
            subscription_service: SubscriptionService instance
            orion_url: Orion base URL
            
        Returns:
            Count of subscriptions created
        """
        subscriptions = [
            {
                'description': 'Price change notification',
                'subject': {
                    'entities': [{'type': 'Product'}],
                    'condition': {
                        'attrs': ['price']
                    }
                },
                'notification': {
                    'http': {
                        'url': f'http://backend:5000/notifications'
                    },
                    'attrs': ['price', 'name', 'id']
                }
            },
            {
                'description': 'Low stock notification',
                'subject': {
                    'entities': [{'type': 'InventoryItem'}],
                    'condition': {
                        'attrs': ['quantity'],
                        'expression': {'q': 'quantity<10'}
                    }
                },
                'notification': {
                    'http': {
                        'url': f'http://backend:5000/notifications'
                    },
                    'attrs': ['quantity', 'productId', 'storeId']
                }
            }
        ]
        
        logger.info("\n🔔 Creating Orion subscriptions...")
        created = 0
        
        for sub in subscriptions:
            result = subscription_service.create_subscription(sub)
            if result.get('success'):
                logger.info(f"✓ Created subscription: {sub['description']}")
                created += 1
            else:
                logger.warning(f"⊘ Subscription already exists: {sub['description']}")
        
        return created
    
    def run(self, provider_service, subscription_service) -> Dict[str, Any]:
        """
        Execute full import process
        
        Args:
            provider_service: ProviderService instance
            subscription_service: SubscriptionService instance
            
        Returns:
            Summary dictionary with import statistics
        """
        logger.info("\n" + "="*60)
        logger.info("🚀 ORION DATA IMPORT STARTED")
        logger.info("="*60)
        
        # Import entities from JSON files
        files_to_import = [
            ('products.json', 'Product'),
            ('stores.json', 'Store'),
            ('employees.json', 'Employee'),
            ('shelves.json', 'Shelf'),
            ('inventory.json', 'InventoryItem')
        ]
        
        total_created = 0
        total_skipped = 0
        
        for filename, entity_type in files_to_import:
            created, skipped = self.import_file(filename, entity_type)
            total_created += created
            total_skipped += skipped
        
        # Register providers
        providers_registered = self.register_providers(provider_service)
        
        # Create subscriptions
        subscriptions_created = self.create_subscriptions(subscription_service, self.orion_url)
        
        logger.info("\n" + "="*60)
        logger.info("✅ IMPORT COMPLETED")
        logger.info("="*60)
        
        summary = {
            'success': True,
            'entities_created': self.entities_created,
            'entities_skipped': self.entities_skipped,
            'providers_registered': providers_registered,
            'subscriptions_created': subscriptions_created,
            'total_operations': self.entities_created + self.entities_skipped + providers_registered + subscriptions_created
        }
        
        logger.info(f"📊 Summary: {summary['entities_created']} entities created, "
                   f"{summary['entities_skipped']} skipped, "
                   f"{summary['providers_registered']} providers, "
                   f"{summary['subscriptions_created']} subscriptions")
        
        return summary


def run_import(app, orion_url: str, provider_service, subscription_service) -> Dict[str, Any]:
    """
    Convenience function to run import process
    
    Args:
        app: Flask app instance (used for logging context)
        orion_url: Orion base URL
        provider_service: ProviderService instance
        subscription_service: SubscriptionService instance
        
    Returns:
        Import summary dictionary
    """
    importer = OrionDataImporter(orion_url)
    return importer.run(provider_service, subscription_service)
