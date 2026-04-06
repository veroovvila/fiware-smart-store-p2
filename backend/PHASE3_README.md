# Phase 3: Orion Integration & Initial Data Loading

## Overview
- Real HTTP integration with Orion Context Broker
- Automatic bulk data import (114 NGSIv2 entities)
- External provider registration
- Automatic subscription creation
- Real-time notifications via Socket.IO

## Core Files

### 1. `backend/data/import_data.py`
**Class:** `OrionDataImporter`

**Main Features:**
- Reads JSON files from `/import-data/`
- Creates NGSIv2 entities in Orion
- Detects and skips duplicates
- Registers external providers
- Creates subscriptions

**Key Methods:**
```python
import_file(filename, entity_type)      # Import single file
register_providers(provider_service)     # Register 3 providers
create_subscriptions(subscription_service, orion_url)  # Create 2 subs
run(provider_service, subscription_service)  # Full import process
```

### 2. `backend/app.py` (Updated)
**New capabilities:**
- Auto-run importer on startup
- POST `/notifications` endpoint
- Socket.IO event broadcasting

**Startup Flow:**
1. Checks Orion health
2. Runs import if healthy
3. Registers providers
4. Creates subscriptions
5. Ready for notifications

### 3. `backend/services/orion_service.py` (Updated)
**Now with real HTTP calls:**
- `create_entity()` → POST /v2/entities
- `get_entity()` → GET /v2/entities/{id}
- `update_entity()` → PATCH /v2/entities/{id}/attrs
- `delete_entity()` → DELETE /v2/entities/{id}
- `list_entities()` → GET /v2/entities
- `health_check()` → GET /version

**Header Fix:** GET/DELETE requests no longer include Content-Type

## Data Import Process

**Files Imported:**
```
import-data/
├── products.json        (10 entities)
├── stores.json          (4 entities)
├── employees.json       (4 entities)
├── shelves.json         (16 entities)
└── inventory.json       (80 entities)
Total: 114 entities
```

**Duplicate Detection:**
- Before creating: GET entity by ID
- 200 OK → entity exists → skip
- 404 Not Found → create new entity
- Prevents data duplication on re-runs

## External Providers

**Automatically Registered:**
1. `temperatura` - Weather API (temperature)
2. `humedad` - Weather API (humidity)
3. `tweets` - Twitter API (social data)

Registered in ProviderService on startup.

## Subscriptions

**Price Change:**
```json
{
  "subject": {"entities": [{"type": "Product"}], "condition": {"attrs": ["price"]}},
  "notification": {"http": {"url": "http://backend:5000/notifications"}}
}
```
Triggers when Product.price changes.

**Low Stock:**
```json
{
  "subject": {"entities": [{"type": "InventoryItem"}], 
    "condition": {"attrs": ["quantity"], "expression": {"q": "quantity<10"}}},
  "notification": {"http": {"url": "http://backend:5000/notifications"}}
}
```
Triggers when InventoryItem.quantity drops below 10.

## Notifications Endpoint

**Endpoint:** `POST /notifications`

**Purpose:** Receives notifications from Orion when subscribed events occur

**Response:**
```json
{
  "success": true,
  "message": "Notification received",
  "subscription_id": "subscription_uuid"
}
```

**Actions:**
1. Detects notification type (price_change, low_stock)
2. Calls appropriate NotificationService method
3. Broadcasts via Socket.IO to connected clients:
   - `price_change` event
   - `low_stock` event
   - `entity_update` event (generic)

## Socket.IO Events

**Price Change Event:**
```javascript
socket.on('price_change', (data) => {
  console.log(`Price updated: ${data.product_id}`);
  console.log(`Old: ${data.old_price}, New: ${data.new_price}`);
});
```

**Low Stock Event:**
```javascript
socket.on('low_stock', (data) => {
  console.log(`Low stock alert: ${data.product_id}`);
  console.log(`Quantity: ${data.quantity}, Threshold: ${data.threshold}`);
});
```

**Generic Entity Update:**
```javascript
socket.on('entity_update', (data) => {
  console.log(`Entity updated: ${data.entity_id}`);
  console.log(`Type: ${data.entity_type}`);
  console.log(`Notification: ${data.notification_type}`);
});
```

## Testing

**Check Orion Health:**
```bash
curl http://localhost:1026/version
```

**List All Products:**
```bash
curl http://localhost:1026/v2/entities?type=Product
```

**Check Subscriptions:**
```bash
curl http://localhost:1026/v2/subscriptions
```

**Check Inventory (Low Stock):**
```bash
curl 'http://localhost:1026/v2/entities?type=InventoryItem&q=quantity<10'
```

## Architecture

```
Docker Network (fiware)
├── MongoDB:27017
│   └── Database: fiware_smartstore
│       ├── Products
│       ├── Stores
│       ├── Employees
│       ├── Shelves
│       └── InventoryItems
│
├── Orion:1026
│   ├── NGSIv2 API
│   ├── 114 entities
│   ├── 2 subscriptions
│   └── Sends notifications to backend:5000
│
├── Backend:5000
│   ├── /health
│   ├── /api/version
│   ├── POST /notifications (receives from Orion)
│   └── Socket.IO (broadcasts to clients)
│
└── Frontend:8080
    └── Receives real-time updates via Socket.IO
```

## Error Handling

**Import Failures:**
- Missing JSON file → warning, skips
- Invalid JSON → error, skips file
- Orion unreachable → error, aborts import
- Entity creation fails → logs error, continues

**Notification Failures:**
- Invalid payload → 400 error
- Missing required fields → 400 error
- Processing error → logs and returns error

## NGSIv2 Format

All entities follow strict NGSIv2 structure:
```json
{
  "id": "urn:ngsi-ld:Type:ID",
  "type": "EntityType",
  "attribute1": {"type": "Text", "value": "text_value"},
  "attribute2": {"type": "Number", "value": 123.45},
  "attribute3": {"type": "DateTime", "value": "2026-04-06T16:37:00Z"}
}
```

## Status

✅ Real Orion integration complete
✅ Bulk data import functional
✅ Subscriptions created
✅ Notifications working
✅ Socket.IO broadcasting ready

**Next:** Phase 4 - API Route Implementation
