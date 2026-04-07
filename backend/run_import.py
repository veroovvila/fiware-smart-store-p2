#!/usr/bin/env python3
"""
Standalone script to run data import into Orion
"""

import os
import sys
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import required modules
from data.import_data import OrionDataImporter
from services.provider_service import ProviderService
from services.subscription_service import SubscriptionService
from config import get_config

if __name__ == '__main__':
    # Get configuration
    config = get_config(os.getenv('FLASK_ENV', 'development'))
    orion_url = config.ORION_URL
    
    logger.info(f"Importing data to Orion at: {orion_url}")
    
    # Initialize services
    provider_service = ProviderService()
    subscription_service = SubscriptionService(orion_url)
    
    # Run importer
    importer = OrionDataImporter(orion_url)
    result = importer.run(provider_service, subscription_service)
    
    # Print summary
    logger.info("\n" + "="*60)
    logger.info(f"✅ Import Summary:")
    logger.info(f"   Entities Created: {result['entities_created']}")
    logger.info(f"   Entities Skipped: {result['entities_skipped']}")
    logger.info(f"   Providers Registered: {result['providers_registered']}")
    logger.info(f"   Subscriptions Created: {result['subscriptions_created']}")
    logger.info("="*60 + "\n")
    
    sys.exit(0 if result['success'] else 1)
