#!/usr/bin/env python3
"""
PHASE 3: ORION INTEGRATION & INITIAL DATA LOADING
Complete example and documentation
"""

# ============================================================
# 1. EXAMPLE: NGSIv2 SUBSCRIPTIONS
# ============================================================

# Price Change Subscription (created automatically on startup)
price_change_subscription = {
    "description": "Price change notification",
    "subject": {
        "entities": [{"type": "Product"}],
        "condition": {
            "attrs": ["price"]
        }
    },
    "notification": {
        "http": {
            "url": "http://backend:5000/notifications"
        },
        "attrs": ["price", "name", "id"]
    }
}

# Low Stock Subscription (created automatically on startup)  
low_stock_subscription = {
    "description": "Low stock notification",
    "subject": {
        "entities": [{"type": "InventoryItem"}],
        "condition": {
            "attrs": ["quantity"],
            "expression": {"q": "quantity<10"}
        }
    },
    "notification": {
        "http": {
            "url": "http://backend:5000/notifications"
        },
        "attrs": ["quantity", "productId", "storeId"]
    }
}


# ============================================================
# 2. EXAMPLE: Entity Creation (NGSIv2 Format)
# ============================================================

product_entity = {
    "id": "urn:ngsi-ld:Product:P001",
    "type": "Product",
    "name": {"type": "Text", "value": "Organic Coffee Beans"},
    "price": {"type": "Number", "value": 12.99},
    "size": {"type": "Text", "value": "500g"},
    "color": {"type": "Text", "value": "Brown"},
    "originCountry": {"type": "Text", "value": "Colombia"},
    "image": {"type": "Text", "value": "/images/coffee-beans.jpg"}
}

inventory_entity = {
    "id": "urn:ngsi-ld:InventoryItem:I001",
    "type": "InventoryItem",
    "productId": {"type": "Text", "value": "P001"},
    "storeId": {"type": "Text", "value": "urn:ngsi-ld:Store:S001"},
    "quantity": {"type": "Number", "value": 5},  # LOW STOCK - triggers notification
    "lastRestockDate": {"type": "DateTime", "value": "2026-04-06T16:37:00Z"}
}


# ============================================================
# 3. EXAMPLE: Notification from Orion (POST /notifications)
# ============================================================

orion_notification_payload = {
    "subscriptionId": "5e694e7e2dd2665558000001",
    "originator": "localhost",
    "data": [
        {
            "id": "urn:ngsi-ld:Product:P001",
            "type": "Product",
            "price": {
                "type": "Number",
                "value": 14.99,
                "metadata": {
                    "oldValue": 12.99
                }
            },
            "name": {
                "type": "Text",
                "value": "Organic Coffee Beans"
            }
        }
    ]
}

# This triggers:
# 1. OrionDataImporter detects it's a price_change
# 2. NotificationService.notify_price_change() is called
# 3. Socket.IO broadcasts 'price_change' event to connected clients:
socket_io_event_broadcast = {
    "event": "price_change",
    "data": {
        "product_id": "urn:ngsi-ld:Product:P001",
        "old_price": 12.99,
        "new_price": 14.99
    }
}


# ============================================================
# 4. EXAMPLE: External Providers (registered on startup)
# ============================================================

providers_registered = [
    {
        "name": "temperatura",
        "description": "Temperature data provider",
        "url": "http://weather-api:8080/temperature",
        "type": "weather"
    },
    {
        "name": "humedad",
        "description": "Humidity data provider",
        "url": "http://weather-api:8080/humidity",
        "type": "weather"
    },
    {
        "name": "tweets",
        "description": "Twitter data provider",
        "url": "http://twitter-api:8080/tweets",
        "type": "social"
    }
]


# ============================================================
# 5. STARTUP FLOW
# ============================================================

"""
When app.py is executed:

1. create_app() initializes Flask + Socket.IO
2. Creates instances of:
   - OrionService (HTTP client for Orion)
   - ProviderService (external provider registry)
   - SubscriptionService (Orion subscription manager)
   - NotificationService (Socket.IO broadcaster)

3. Checks Orion health status:
   - GET http://orion:1026/version
   - Returns: 200 OK with version info

4. If Orion is healthy, runs OrionDataImporter:
   
   a) Import JSON files (114 entities total):
      ✓ products.json (10 entities)
      ✓ stores.json (4 entities)
      ✓ employees.json (4 entities)
      ✓ shelves.json (16 entities)
      ✓ inventory.json (80 entities)
      
   b) Skip duplicates:
      - Before creating, checks if entity exists with GET
      - HTTP 200 = entity exists → skip
      - HTTP 404 = entity doesn't exist → create
      
   c) Register 3 external providers:
      - temperatura, humedad, tweets
      - Stored in ProviderService.providers dict
      
   d) Create 2 automatic subscriptions:
      - price_change: Triggers when Product.price changes
      - low_stock: Triggers when InventoryItem.quantity < 10
      
5. Flask app is ready to receive:
   - GET /health (healthcheck)
   - GET /api/version (API info)
   - POST /notifications (Orion callbacks)
   - Socket.IO connections
   
6. When Orion detects a change:
   - Sends POST to /notifications
   - Backend broadcasts to connected clients
   - Clients receive real-time updates via Socket.IO
"""


# ============================================================
# 6. EXPECTED LOGS FOR Phase 3
# ============================================================

expected_logs = """
INFO:backend.app:Flask app initialized with config: DevelopmentConfig
INFO:backend.services.orion_service:OrionService initialized with URL: http://orion:1026
INFO:backend.services.orion_service:Orion is healthy
INFO:backend.data.import_data:

============================================================
🚀 ORION DATA IMPORT STARTED
============================================================

📂 Importing products.json (10 entities)...
✓ Created entity: urn:ngsi-ld:Product:P001
✓ Created entity: urn:ngsi-ld:Product:P002
...
   Result: 10 created, 0 skipped

📂 Importing stores.json (4 entities)...
✓ Created entity: urn:ngsi-ld:Store:S001
...
   Result: 4 created, 0 skipped

📂 Importing employees.json (4 entities)...
✓ Created entity: urn:ngsi-ld:Employee:E001
...
   Result: 4 created, 0 skipped

📂 Importing shelves.json (16 entities)...
✓ Created entity: urn:ngsi-ld:Shelf:SH001
...
   Result: 16 created, 0 skipped

📂 Importing inventory.json (80 entities)...
✓ Created entity: urn:ngsi-ld:InventoryItem:I001
...
   Result: 80 created, 0 skipped

📡 Registering external providers...
✓ Registered provider: temperatura
✓ Registered provider: humedad
✓ Registered provider: tweets

🔔 Creating Orion subscriptions...
✓ Created subscription: Price change notification
✓ Created subscription: Low stock notification

============================================================
✅ IMPORT COMPLETED
============================================================

📊 Summary: 114 entities created, 0 skipped, 3 providers, 2 subscriptions
"""
