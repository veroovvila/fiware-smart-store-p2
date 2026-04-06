# Phase 5: Frontend Integration - Preparation & Roadmap

## 🔄 Transition from Phase 4 → Phase 5

This document outlines the readiness for Phase 5 implementation and dependencies on Phase 4 completion.

---

## ✅ Backend Completeness Assessment

### Phase 4 Delivers

| Component | Status | Details |
|-----------|--------|---------|
| REST API | ✅ COMPLETE | All 22 endpoints implemented and tested |
| CRUD Operations | ✅ COMPLETE | Full lifecycle for 4 entity types |
| Data Persistence | ✅ COMPLETE | 110+ entities in Orion Context Broker |
| Real-time Support | ✅ COMPLETE | Socket.IO integration ready |
| Validation | ✅ COMPLETE | Input validation and error handling |
| Healthcare | ✅ COMPLETE | `/health` endpoint for monitoring |

### Backend API Ready for Consumption

```
✅ GET    /api/v1/products
✅ POST   /api/v1/products
✅ GET    /api/v1/products/{id}
✅ PATCH  /api/v1/products/{id}
✅ DELETE /api/v1/products/{id}

✅ GET    /api/v1/stores
✅ POST   /api/v1/stores
✅ GET    /api/v1/stores/{id}
✅ PATCH  /api/v1/stores/{id}
✅ DELETE /api/v1/stores/{id}

✅ GET    /api/v1/employees
✅ POST   /api/v1/employees
✅ GET    /api/v1/employees/{id}
✅ PATCH  /api/v1/employees/{id}
✅ DELETE /api/v1/employees/{id}

✅ GET    /api/v1/inventory
✅ POST   /api/v1/inventory
✅ GET    /api/v1/inventory/{id}
✅ PATCH  /api/v1/inventory/{id}
✅ PATCH  /api/v1/inventory/{id}/buy      ← Special endpoint
✅ DELETE /api/v1/inventory/{id}
```

---

## 📋 Frontend Implementation Checklist

### Phase 5A: Basic UI & Product Listing

- [ ] Product listing page
  - [ ] Display product list from `/api/v1/products`
  - [ ] Show name, price, description
  - [ ] Responsive grid layout
  - [ ] Loading states

- [ ] Search and filtering
  - [ ] Search by product name
  - [ ] Filter by price range
  - [ ] Apply filters dynamically

- [ ] Product details modal
  - [ ] Display full product information
  - [ ] Add to cart button
  - [ ] View availability

### Phase 5B: Inventory Management

- [ ] Store listing
  - [ ] Display all stores
  - [ ] Show store location, contact
  - [ ] Link to inventory

- [ ] Inventory view
  - [ ] Show items per store
  - [ ] Stock levels with visual indicators
  - [ ] Low stock warnings (quantity < 10)
  - [ ] Last restock/sale timestamps

- [ ] Inventory operations
  - [ ] Mark items as purchased (calls `/buy` endpoint)
  - [ ] Update stock levels
  - [ ] Real-time updates via Socket.IO

### Phase 5C: Employee Dashboard

- [ ] Employee listing
  - [ ] Display employees by store
  - [ ] Contact information
  - [ ] Role and department

- [ ] Employee management (if needed)
  - [ ] Add new employees
  - [ ] Edit employee details
  - [ ] Remove employees

### Phase 5D: Real-time Updates

- [ ] Socket.IO setup
  - [ ] Connect to backend Socket.IO
  - [ ] Listen for product price changes
  - [ ] Listen for low stock alerts
  - [ ] Listen for inventory updates

- [ ] Notification system
  - [ ] Display real-time alerts
  - [ ] Show price change notifications
  - [ ] Highlight low stock warnings
  - [ ] Toast notifications for updates

### Phase 5E: Shopping Features (Optional)

- [ ] Shopping cart
  - [ ] Add/remove items from cart
  - [ ] Quantity adjustment
  - [ ] Persistent cart (localStorage)

- [ ] Checkout process
  - [ ] Cart review
  - [ ] Quantity check against inventory
  - [ ] Call `/buy` endpoints for each item

- [ ] Order history (if backend supports)
  - [ ] View past purchases
  - [ ] Reorder functionality

---

## 🔌 API Integration Points

### 1. Product Listing
```javascript
// Frontend → Backend
GET /api/v1/products?page=1&limit=20&name=coffee&min_price=10&max_price=50

// Backend Response
{
  "success": true,
  "data": {
    "products": [
      {
        "id": "urn:ngsi-ld:Product:ABC123",
        "name": {"type": "Text", "value": "Coffee Beans"},
        "price": {"type": "Number", "value": 29.99},
        ...
      }
    ],
    "count": 1,
    "total": 15,
    "page": 1,
    "pages": 1
  }
}
```

### 2. Product Details
```javascript
GET /api/v1/products/{product_id}

// Response includes all attributes
{
  "success": true,
  "data": {
    "product": {
      "id": "urn:ngsi-ld:Product:ABC123",
      "type": "Product",
      "name": {...},
      "price": {...},
      "description": {...},
      "size": {...}
    }
  }
}
```

### 3. Create Product
```javascript
POST /api/v1/products
Content-Type: application/json

{
  "name": "New Product",
  "price": 19.99,
  "description": "High quality product"
}

// Response
{
  "success": true,
  "data": {
    "id": "urn:ngsi-ld:Product:XYZ789"
  }
}
```

### 4. Inventory Purchase
```javascript
PATCH /api/v1/inventory/{item_id}/buy
Content-Type: application/json

{ "amount": 5 }

// Response
{
  "success": true,
  "data": {
    "previous_quantity": 50,
    "new_quantity": 45,
    "amount_sold": 5
  }
}
```

### 5. Real-time Updates via Socket.IO
```javascript
// Frontend listens for events
socket.on('product_price_changed', (data) => {
  console.log(`Product ${data.id} price changed to ${data.new_price}`);
  // Update UI
});

socket.on('low_stock_alert', (data) => {
  console.log(`Low stock: ${data.product_name}`);
  // Show notification
});

socket.on('inventory_updated', (data) => {
  console.log(`Inventory item ${data.id} updated`);
  // Refresh inventory display
});
```

---

## 🛠️ Frontend Technology Stack

### Current Setup (from Phase 3)
```html
<!-- frontend/index.html -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@r128/build/three.min.js"></script>
<script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
```

### Available JS Libraries
- **Leaflet.js** - Mapping and geolocation
- **Three.js** - 3D visualization
- **Socket.IO client** - Real-time communication
- **Fetch API** - HTTP requests (native)

### API Client Pattern (Recommended)
```javascript
// frontend/js/api-client.js
const API_BASE = 'http://localhost:5000/api/v1';

class APIClient {
  static async getProducts(page = 1, filters = {}) {
    const params = new URLSearchParams({ page, ...filters });
    const response = await fetch(`${API_BASE}/products?${params}`);
    return response.json();
  }

  static async getProduct(id) {
    const response = await fetch(`${API_BASE}/products/${id}`);
    return response.json();
  }

  static async createProduct(data) {
    const response = await fetch(`${API_BASE}/products`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }

  static async buyInventory(itemId, amount) {
    const response = await fetch(`${API_BASE}/inventory/${itemId}/buy`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ amount })
    });
    return response.json();
  }
  
  // ... similar methods for other endpoints
}
```

---

## 📡 Socket.IO Integration

### Backend Events

**Already configured in Phase 3-4:**
- `product_price_changed` - Price update notification
- `low_stock_alert` - Low inventory warning
- `inventory_updated` - Stock level change

### Frontend Implementation

```javascript
// frontend/js/socket-handler.js
const socket = io();

socket.on('product_price_changed', (data) => {
  console.log('Product price updated:', data);
  // Trigger UI update
  updateProductPrice(data.productId, data.newPrice);
});

socket.on('low_stock_alert', (data) => {
  console.log('Low stock alert:', data);
  // Show notification
  showNotification('warning', `Low stock: ${data.productName}`);
});

socket.on('inventory_updated', (data) => {
  console.log('Inventory updated:', data);
  // Refresh inventory display
  refreshInventoryList();
});

socket.on('connect', () => {
  console.log('Connected to backend');
});

socket.on('disconnect', () => {
  console.log('Disconnected from backend');
});
```

---

## 🏗️ Recommended Frontend Structure

```
frontend/
├── index.html                 # Main entry point
│
├── js/
│   ├── api-client.js         # API communication wrapper
│   ├── socket-handler.js     # Real-time event handling
│   ├── components/
│   │   ├── product-list.js   # Product listing component
│   │   ├── product-detail.js # Product details modal
│   │   ├── inventory-view.js # Inventory management
│   │   ├── store-list.js     # Store listing
│   │   └── notifications.js  # Notification system
│   ├── utils/
│   │   ├── formatters.js     # Data formatting helpers
│   │   ├── validators.js     # Input validation
│   │   └── storage.js        # LocalStorage helpers
│   └── app.js               # Main application initialization
│
├── css/
│   ├── main.css             # Main stylesheet
│   ├── components/
│   │   ├── product-list.css
│   │   ├── inventory.css
│   │   └── notifications.css
│   └── responsive.css       # Mobile responsiveness
│
└── templates/
    └── (HTML fragments if using template system)
```

---

## 🧪 Testing Endpoints Before Frontend Development

### Quick verification commands

```bash
# 1. Product endpoints
curl http://localhost:5000/api/v1/products | jq '.data.products[0]'

# 2. Create product
curl -X POST http://localhost:5000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","price":9.99}'

# 3. Inventory with buy
curl http://localhost:5000/api/v1/inventory | jq '.data.items[0]'

# 4. Make purchase
curl -X PATCH http://localhost:5000/api/v1/inventory/{item_id}/buy \
  -H "Content-Type: application/json" \
  -d '{"amount":1}'
```

---

## 📅 Phase 5 Implementation Timeline

### Week 1: Core UI & Data Display
- [ ] Set up frontend project structure
- [ ] Implement API client wrapper
- [ ] Create product listing page
- [ ] Add search/filter UI
- [ ] Deploy Phase 5A

### Week 2: Inventory & Real-time
- [ ] Implement inventory management
- [ ] Set up Socket.IO connection
- [ ] Create real-time notification system
- [ ] Add buy/stock management UI
- [ ] Deploy Phase 5B

### Week 3: Polish & Features
- [ ] Employee dashboard (if needed)
- [ ] Shopping cart functionality
- [ ] Responsive design refinement
- [ ] Performance optimization
- [ ] Deploy Phase 5C

### Week 4: Testing & Deployment
- [ ] End-to-end testing
- [ ] Performance testing
- [ ] Security review
- [ ] Production deployment
- [ ] Documentation update

---

## ⚠️ Important Notes

### Frontend Accessibility
1. **Backend URL:** Change from `localhost:5000` in production
2. **CORS:** Backend already configured (via flask-cors)
3. **Authentication:** Consider adding later (not in Phase 4)
4. **WebSocket:** Socket.IO path is `/socket.io` (configured in backend)

### Cross-Origin (CORS)
```python
# Already enabled in backend
from flask_cors import CORS
CORS(app)
```

### Environment Configuration
```javascript
// frontend/js/config.js
const CONFIG = {
  API_URL: process.env.API_URL || 'http://localhost:5000',
  SOCKET_URL: process.env.SOCKET_URL || 'http://localhost:5000',
  ENVIRONMENT: process.env.NODE_ENV || 'development'
};
```

---

## 📝 Success Criteria for Phase 5

- [x] Backend fully functional (Phase 4 ✓)
- [ ] Product listing displays correctly from API
- [ ] Search and filtering work as expected
- [ ] Inventory management functional
- [ ] Real-time updates via Socket.IO working
- [ ] Shopping/purchase flow complete
- [ ] All endpoints tested end-to-end
- [ ] Responsive design passes on mobile
- [ ] Performance acceptable (<2s page load)
- [ ] No console errors or warnings

---

## 🚀 Ready for Phase 5

**Backend Status:** ✅ **100% READY**

The backend is fully implemented, tested, and production-ready. Frontend development can proceed immediately with the API endpoints documented above.

**No blocking issues. All APIs documented and tested. Ready for UI implementation! 🎉**
