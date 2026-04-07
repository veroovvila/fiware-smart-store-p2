# Arquitectura: FIWARE Smart Store – Práctica 2

## 1. Visión General de Arquitectura

### Diagrama de Bloques Alto Nivel

```
┌─────────────────────────────────────────────────────────────────────┐
│                          CLIENTE WEB                                │
│  (HTML + CSS + JS + Leaflet + Three.js + Socket.IO)                │
│                    (ES 6+ Puro)                                     │
└──────────────────────────┬──────────────────────────────────────────┘
                           │ HTTP REST
                           │ WebSocket (Socket.IO)
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│                        BACKEND - FLASK                              │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Routes (CRUD: Products, Stores, Employees, Inventory)      │  │
│  │  - GET /v2/entities/* → Query Orion                          │  │
│  │  - POST /v2/entities → Create in Orion                       │  │
│  │  - PATCH /v2/entities/<id>/attrs → Update in Orion          │  │
│  │  - DELETE /v2/entities/* → Delete from Orion                │  │
│  │  - POST /notifications ← Receive webhook from Orion         │  │
│  └──────────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                   SERVICIOS REUTILIZABLES                    │  │
│  │  • OrionService: CRUD de entidades NGSIv2                   │  │
│  │  • SubscriptionService: Crear/gestionar suscripciones       │  │
│  │  • ProviderService: Registrar proveedores externos          │  │
│  │  • NotificationService: Recibir y emitir notificaciones     │  │
│  │  • SocketIOService: Emitir eventos a clientes               │  │
│  └──────────────────────────────────────────────────────────────┘  │
│  Puerto: 5000                                                       │
└──────────────────────────┬──────────────────────────────────────────┘
                           │ HTTP REST (NGSIv2)
                           │ (Webhook de suscripciones)
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│         FIWARE ORION CONTEXT BROKER (NGSIv2)                        │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Entidades: Product, Store, Employee, Shelf, InventoryItem  │  │
│  │  Suscripciones: Change Price, Low Stock                      │  │
│  │  Registrations: Temperature, Humidity, Tweets                │  │
│  └──────────────────────────────────────────────────────────────┘  │
│  Puerto: 1026                                                       │
└──────────────────────────┬──────────────────────────────────────────┘
                           │ MongoDB Driver
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│                      MONGODB                                        │
│  • Persistencia de entidades NGSIv2                                 │
│  • Índices en id, type, refProduct, refStore, refShelf            │  
│  • TTL indexes para datos temporales                               │
│  Puerto: 27017                                                      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│           PROVEEDORES EXTERNOS (Registrados en Orion)              │
│  • Weather API → temperature, relativeHumidity                      │
│  • Twitter API → tweets                                            │
│  • (Extensible para otros proveedores)                             │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. Arquitectura en Capas

### 2.1 Capa de Presentación (Frontend)

**Tecnologías:**
- HTML5 + CSS3 + JavaScript ES6+
- Socket.IO para comunicación bidireccional
- Leaflet.js para mapas interactivos
- Three.js para visualización 3D
- Font Awesome para iconos
- i18n (internacionalización ES/EN)
- Dark/Light theme switcher

**Estructura de Carpetas:**
```
frontend/
├── index.html                # Layout principal, navbar fija
├── css/
│   ├── styles.css           # Estilos generales, grid system
│   ├── dark-mode.css        # Estilos modo oscuro (variables CSS)
│   ├── responsive.css       # Media queries mobile-first
│   ├── components/
│   │   ├── navbar.css       # Barra de navegación
│   │   ├── table.css        # Estilos de tablas
│   │   ├── modal.css        # Diálogos
│   │   └── notification.css # Toasts/alerts
│   └── utils/
│       └── variables.css    # CSS variables (colores, espacios)
├── js/
│   ├── socket.js            # Configuración Cliente Socket.IO
│   ├── views/
│   │   ├── home.js          # Dashboard, diagrama UML
│   │   ├── products.js      # Tabla productos, búsqueda, filtros
│   │   ├── stores.js        # Tabla tiendas
│   │   ├── employees.js     # Tabla empleados, login
│   │   ├── store-detail.js  # Mapa (Leaflet), 3D (Three.js), inventario
│   │   ├── product-detail.js # Inventario por tienda, gráficos
│   │   └── stores-map.js    # Mapa global de tiendas (Leaflet)
│   ├── components/
│   │   ├── table.js         # Componente tabla reutilizable
│   │   ├── modal.js         # Componente modal (CRUD forms)
│   │   ├── notification.js  # Componente toast/alert
│   │   ├── map.js           # Inicialización Leaflet
│   │   └── 3d-viewer.js     # Inicialización Three.js
│   └── utils/
│       ├── api.js           # Wrapper fetch a endpoints Flask
│       ├── i18n.js          # Cargar/cambiar idioma
│       ├── theme.js         # Toggle dark/light mode
│       ├── formatters.js    # Formato fecha, precio, etc.
│       └── helpers.js       # Funciones comunes
└── templates/               # (Opcional si Flask renderiza plantillas)
    ├── products.html
    ├── stores.html
    ├── etc.
```

**Vistas Principales:**

1. **Home**
   - 4 tarjetas: Total Stores, Total Products, Total Employees, Total Inventory Items
   - Diagrama UML generado dinámicamente con Mermaid
   - Botones de acceso rápido a otras vistas

2. **Products**
   - Tabla: imagen (thumbnail), nombre, precio, tamaño, color, país origen
   - Búsqueda by nombre (debounce 300ms)
   - Filtros: tamaño, rango precio, país origen
   - Click en fila → Product Detail

3. **Stores**
   - Tabla: nombre, código país, temperatura, humedad relativa
   - Filtro por país
   - Click en fila → Store Detail

4. **Employees**
   - Tabla: nombre, rol, tienda asignada, skills (checkbox icons)
   - Filtro por tienda y rol
   - Click en fila → detalles/editar
   - Formulario de login en navegación

5. **Store Detail**
   - Panel izquierdo: Mapa (Leaflet) con ubicación
   - Panel central: Vista 3D (Three.js) de estanterías
   - Panel derecho: 
     - Inventario agrupado por Shelf (tabla con % ocupación)
     - Widget de tweets
     - Panel de notificaciones recientes

6. **Product Detail**
   - Tabla: tienda, cantidad almacén, cantidad estantería
   - Gráfico pie/bar: distribución por tienda
   - Suma total de inventario
   - Opción de editar producto

7. **Stores Map**
   - Leaflet map global
   - Marcadores en coordenadas de tiendas
   - Popups con nombre, dirección, teléfono
   - Zoom y pan interactivos

---

### 2.2 Capa de Lógica de Negocio (Backend - Flask)

**Arquitectura:** Blueprint pattern (modular)

**Estructura de Carpetas:**
```
backend/
├── app.py                   # Punto de entrada, configuración Flask-SocketIO
├── config.py               # Configuración, variables de entorno
├── requirements.txt        # Dependencias Python
├── services/
│   ├── __init__.py
│   ├── orion_service.py    # Servicio CRUD a Orion NGSIv2
│   ├── subscription_service.py # Crear/gestionar suscripciones
│   ├── provider_service.py # Registrar proveedores externos
│   └── notification_service.py # Emitir eventos Socket.IO
├── routes/
│   ├── __init__.py
│   ├── products.py         # GET/POST/PATCH/DELETE Products
│   ├── stores.py           # GET/POST/PATCH/DELETE Stores
│   ├── employees.py        # GET/POST/PATCH/DELETE Employees
│   ├── inventory.py        # GET/POST/PATCH/DELETE InventoryItems, Shelves
│   └── notifications.py    # POST /notifications (webhook de Orion)
├── utils/
│   ├── __init__.py
│   ├── helpers.py          # Funciones comunes
│   ├── validators.py       # Validaciones de datos
│   └── decorators.py       # Decoradores (auth, error handling)
└── data/
    └── import_data.py      # Script para cargar datos iniciales
```

**Servicios Reutilizables:**

1. **OrionService**
   ```
   Métodos:
   - create_entity(entity_dict) → POST /v2/entities
   - get_entity(entity_id) → GET /v2/entities/{entity_id}
   - get_entities(entity_type) → GET /v2/entities?type={type}
   - update_entity(entity_id, attrs) → PATCH /v2/entities/{entity_id}/attrs
   - delete_entity(entity_id) → DELETE /v2/entities/{entity_id}
   - create_reference(from_id, to_id, refName) → Crear atributo ref
   ```

2. **SubscriptionService**
   ```
   Métodos:
   - create_subscription(description, entities, attributes, condition, webhook_url)
   - create_price_change_subscription() → Monitorear cambios price en Products
   - create_low_stock_subscription() → Monitorear stockCount < 5 en InventoryItems
   - get_subscriptions() → Listar suscripciones
   - delete_subscription(subscription_id) → Eliminar
   ```

3. **ProviderService**
   ```
   Métodos:
   - register_provider(id, name, entity_type, endpoint, attributes)
   - register_temperature_provider(api_key)
   - register_humidity_provider(api_key)
   - register_tweets_provider(api_key)
   - refresh_external_attributes() → Actualizar datos cada 5 min (scheduler)
   ```

4. **NotificationService** (Socket.IO)
   ```
   Métodos:
   - emit_price_change(product_id, old_price, new_price)
   - emit_low_stock(store_id, shelf_id, product_id, stock_count)
   - emit_notification(event_type, data)
   - broadcast_to_all(event, data)
   - notify_user(session_id, event, data)
   ```

**Rutas (Endpoints REST):**

```
Products:
  GET  /api/products              → Listar con filtros
  POST /api/products              → Crear
  GET  /api/products/<id>         → Obtener detalles
  PATCH /api/products/<id>        → Actualizar
  DELETE /api/products/<id>       → Eliminar

Stores:
  GET  /api/stores                → Listar con filtros
  POST /api/stores                → Crear
  GET  /api/stores/<id>           → Obtener detalles
  PATCH /api/stores/<id>          → Actualizar
  DELETE /api/stores/<id>         → Eliminar

Employees:
  GET  /api/employees             → Listar con filtros
  POST /api/employees             → Crear
  GET  /api/employees/<id>        → Obtener detalles
  PATCH /api/employees/<id>       → Actualizar
  DELETE /api/employees/<id>      → Eliminar
  POST /api/auth/login            → Autenticación

Inventory:
  GET  /api/inventory             → Listar InventoryItems
  POST /api/inventory             → Crear InventoryItem
  GET  /api/inventory/<id>        → Obtener
  PATCH /api/inventory/<id>       → Actualizar (incluye decrementar stock)
  DELETE /api/inventory/<id>      → Eliminar
  
  GET  /api/shelves               → Listar Shelves
  POST /api/shelves               → Crear Shelf
  PATCH /api/shelves/<id>         → Actualizar Shelf
  DELETE /api/shelves/<id>        → Eliminar Shelf

Notifications:
  POST /notifications             ← Webhook de Orion (subscripciones)
```

**Socket.IO Events:**

```
Frontend → Backend:
  subscribe_events()              → Cliente se suscribe a eventos

Backend → Frontend:
  price_change                    → {productId, oldPrice, newPrice, timestamp}
  low_stock                       → {storeId, shelfId, productId, stock, timestamp}
  notification                    → {type, message, data, timestamp}
  data_updated                    → {entity_type, entity_id, action} (refresh hints)
```

---

### 2.3 Capa de Datos (Orion + MongoDB)

**Orion Context Broker (NGSIv2):**
- Almacena entidades con modelo semántico
- Metadata en atributos (origen, tipo, etc.)
- Suscripciones basadas en cambios
- Registrations para proveedores externos

**MongoDB:**
- Backend de persistencia de Orion
- Almacena documentos JSON de entidades
- Índices en campos críticos
- TTL indexes para sesiones

---

## 3. Flujo de Datos Completo

### Caso de Uso: Compra de Producto (Operational Flow)

```
1. USUARIO INTERACTÚA EN FRONTEND
   ├─ Usuario en vista Store Detail
   ├─ Click botón "Comprar" en tabla de inventario
   └─ Abre modal de confirmación

2. FRONTEND ENVÍA REQUEST
   ├─ POST /api/inventory/<inventory_item_id>/buy
   ├─ Body: {"quantity": 1}
   └─ Headers: Authorization (si aplica)

3. BACKEND RECIBE EN ROUTE (routes/inventory.py)
   ├─ Valida: inventory_item_id existe, quantity > 0
   ├─ Valida: stockCount >= quantity
   └─ Llama: InventoryService.process_purchase()

4. ORION SERVICE ACTUALIZA
   ├─ Calcula: new_stockCount = stockCount - quantity
   ├─ PATCH /v2/entities/<inventory_item_id>/attrs
   │  Body: {"stockCount": {"value": new_stockCount}}
   └─ Respuesta: 204 No Content (éxito)

5. ORION PROCESAMIENTO
   ├─ Actualiza documento en MongoDB
   ├─ Detecta cambio en atributo monitoreado
   └─ Dispara suscripción #2 (Low Stock)

6. ORION ENVÍA NOTIFICACIÓN
   ├─ Si new_stockCount < 5:
   ├─ POST /notifications (webhook)
   ├─ Body: {
   │    "data": [{
   │      "id": "INV-001-STORE1-SHELF1",
   │      "type": "InventoryItem",
   │      "stockCount": {"value": 2}
   │    }]
   │  }
   └─ Target: Backend notificación endpoint

7. BACKEND RECIBE NOTIFICACIÓN
   ├─ Route POST /notifications
   ├─ Parse JSON de Orion
   ├─ NotificationService.handle_subscription_notification()
   ├─ Extrae: inventory_id, producto, tienda, stock_nueva
   └─ Prepara evento Socket.IO

8. BACKEND EMITE POR SOCKET.IO
   ├─ io.emit("low_stock", {
   │    "product_id": "PRD-001",
   │    "store_id": "STORE-001",
   │    "shelf_id": "SHELF-001",
   │    "stock_count": 2,
   │    "timestamp": ISO8601
   │  })
   └─ Transmite a todos los clientes conectados

9. FRONTEND RECIBE EVENTO
   ├─ socket.on("low_stock", function(data) {...})
   ├─ Deserializa JSON
   ├─ NotificationComponent.show_toast(data)
   └─ Renderiza: "⚠️ Bajo stock: PRD-001 en STORE-001 (2 unidades)"

10. UI ACTUALIZA
    ├─ Toast notification en navbar
    ├─ Si usuario está en Store Detail:
    │  └─ Actualiza tabla de inventario (PATCH local)
    ├─ Si usuario está en Home:
    │  └─ Actualiza contador "Total Inventory Items"
    └─ Sin reload de página (AJAX/Socket.IO)
```

**Latencia Total:** < 500ms (Orion procesa, HTTP POST, Socket.IO emite, JS renderiza)

---

## 4. Patrones de Diseño y Decisiones Arquitectónicas

### 4.1 Patrón Service Layer

El backend utiliza un patrón Service Layer para separar concerns:

**Ventajas:**
- ✅ Reutilización de lógica de negocio
- ✅ Testabilidad mejorada
- ✅ Desacoplamiento entre rutas y servicios
- ✅ Centralización de lógica Orion

**Capas:**
```
Routes (Capa HTTP)
    ↓
Services (Lógica de negocio)
    ↓
External APIs (Orion, Weather, Twitter)
```

### 4.2 Patrón Publish-Subscribe (Suscripciones)

Orion Context Broker proporciona notificaciones push:

- **Productor**: Cambios en entidades (PATCH/DELETE)
- **Orion**: Detecta cambios y emite notificaciones
- **Consumidor**: Backend recibe via webhook
- **Distribuidor**: Backend propaga via Socket.IO

Ventajas:
- ✅ Desacoplamiento temporal (no espera respuesta)
- ✅ Escalabilidad horizontal (múltiples subscribers)
- ✅ Actualizaciones en tiempo real

### 4.3 Patrón Reference (Relaciones entre Entidades)

Orion no soporta foreign keys tradicionales, usamos atributos de tipo Relationship:

```json
{
  "id": "INV-001",
  "type": "InventoryItem",
  "refProduct": {
    "type": "Relationship",
    "value": "PRD-001"
  },
  "refStore": {
    "type": "Relationship",
    "value": "STORE-001"
  }
}
```

Validación referencial se hace en backend (integrity checks).

### 4.4 Patrón Metadata (Anotaciones en Atributos)

Cada atributo puede incluir metadata sobre su origen/tipo:

```json
"temperature": {
  "type": "Number",
  "value": 22.5,
  "metadata": {
    "provider": "WeatherAPI",
    "lastUpdate": "2026-04-06T10:30:00Z",
    "accuracy": 1.0
  }
}
```

Casos de uso:
- Rastreabilidad de datos
- Validación de freshness de datos
- Routing inteligente

---

## 5. Integración con Orion Context Broker

### 5.1 Endpoints NGSIv2 Utilizados

**Gestión de Entidades:**

```
POST /v2/entities
  Crear entidad
  Body: {
    "id": "PRD-001",
    "type": "Product",
    "name": {"type": "Text", "value": "Laptop"},
    "price": {"type": "Number", "value": 899.99},
    ...
  }
  
GET /v2/entities
  Listar entidades con filtros
  Query params:
    ?type=Product
    ?q=price>500
    ?attrs=name,price
    
GET /v2/entities/<id>
  Obtener entidad específica
  
PATCH /v2/entities/<id>/attrs
  Actualizar atributos
  Body: {
    "price": {"value": 749.99},
    "updatedAt": {"value": "2026-04-06T10:30:00Z"}
  }
  
DELETE /v2/entities/<id>
  Eliminar entidad
```

### 5.2 Metadata en Atributos

**Ejemplo:** Store con atributos externos

```json
{
  "id": "STORE-001",
  "type": "Store",
  "name": {"type": "Text", "value": "Smart Store Madrid"},
  "temperature": {
    "type": "Number",
    "value": 22.5,
    "metadata": {
      "provider": {"type": "Text", "value": "WeatherAPI"},
      "lastUpdate": {"type": "DateTime", "value": "2026-04-06T10:30:00Z"},
      "unit": {"type": "Text", "value": "Celsius"}
    }
  },
  "location": {
    "type": "geo:point",
    "value": "40.4168 -3.7038",
    "metadata": {
      "accuracy": {"type": "Number", "value": 50}
    }
  }
}
```

### 5.3 Suscripciones NGSIv2

**Suscripción 1: Cambio de Precio**

```json
{
  "description": "Notificar cuando cambia el precio de cualquier producto",
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
    "attrs": ["price", "name"]
  },
  "throttling": 300
}
```

**Suscripción 2: Bajo Stock**

```json
{
  "description": "Notificar cuando stock baja del umbral",
  "subject": {
    "entities": [{"type": "InventoryItem"}],
    "condition": {
      "attrs": ["stockCount"],
      "expression": {"q": "stockCount<5"}
    }
  },
  "notification": {
    "http": {
      "url": "http://backend:5000/notifications"
    },
    "attrs": ["stockCount", "refProduct", "refStore", "refShelf"]
  }
}
```

### 5.4 Registrations (Proveedores Externos)

**Ejemplo: Weather Provider**

```json
{
  "description": "Proveedor de temperatura y humedad",
  "dataProvided": {
    "entities": [{"type": "Store"}],
    "attrs": ["temperature", "relativeHumidity"]
  },
  "provider": {
    "http": {
      "url": "http://weather-api:8080/data"
    }
  }
}
```

Flujo:
1. Backend registra provider en Orion
2. Orion consulta provider cada N minutos
3. Provider responde con JSON de temperatura/humedad
4. Orion actualiza atributos en Store
5. Backend recibe cambios via Socket.IO

---

## 6. Socket.IO y Notificaciones en Tiempo Real

### 6.1 Configuración Cliente

```javascript
// frontend/js/socket.js
const socket = io();

socket.on('connect', function() {
  console.log('Conectado a Backend');
  socket.emit('subscribe_events');
});

socket.on('price_change', function(data) {
  // {productId, oldPrice, newPrice, timestamp}
  NotificationComponent.show_toast({
    type: 'info',
    message: `Precio actualizado: ${data.productId} ($${data.oldPrice} → $${data.newPrice})`
  });
  if (window.currentView === 'product-detail') {
    updateProductTable();
  }
});

socket.on('low_stock', function(data) {
  // {storeId, shelfId, productId, stock_count, timestamp}
  NotificationComponent.show_toast({
    type: 'warning',
    message: `⚠️ Bajo stock: ${data.productId} en ${data.storeId} (${data.stock_count} unidades)`
  });
  if (window.currentView === 'store-detail') {
    updateInventoryTable();
  }
});

socket.on('notification', function(data) {
  // {type, message, event_type, data, timestamp}
  console.log('Notificación genérica:', data);
});

// Desconexión
socket.on('disconnect', function() {
  console.log('Desconectado del Backend');
});
```

### 6.2 Configuración Servidor

```python
# backend/app.py
from flask import Flask
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    print(f'Cliente conectado: {request.sid}')
    emit('response', {'data': 'Conectado al servidor'})

@socketio.on('subscribe_events')
def handle_subscribe():
    print(f'Cliente {request.sid} se suscribió a eventos')
    join_room('broadcasts')

@socketio.on('disconnect')
def handle_disconnect():
    print(f'Cliente desconectado: {request.sid}')

# Servicio de Notificaciones emite eventos
def notify_price_change(product_id, old_price, new_price):
    socketio.emit('price_change', {
        'productId': product_id,
        'oldPrice': old_price,
        'newPrice': new_price,
        'timestamp': datetime.now().isoformat()
    }, room='broadcasts')

def notify_low_stock(store_id, shelf_id, product_id, stock_count):
    socketio.emit('low_stock', {
        'storeId': store_id,
        'shelfId': shelf_id,
        'productId': product_id,
        'stock_count': stock_count,
        'timestamp': datetime.now().isoformat()
    }, room='broadcasts')
```

---

## 6. Proveedores Externos

### 6.1 Registración de Proveedores

**Al iniciar app.py:**

```python
# backend/data/import_data.py

def register_external_providers():
    """Registrar 3 proveedores en Orion"""
    providers = [
        {
            "id": "temp-provider-001",
            "name": "Weather Temperature Provider",
            "entity_type": "Store",
            "attributes": ["temperature"],
            "endpoint": os.getenv("WEATHER_API_URL")
        },
        {
            "id": "humidity-provider-001",
            "name": "Weather Humidity Provider",
            "entity_type": "Store",
            "attributes": ["relativeHumidity"],
            "endpoint": os.getenv("WEATHER_API_URL")
        },
        {
            "id": "tweets-provider-001",
            "name": "Twitter Sentiment Provider",
            "entity_type": "Store",
            "attributes": ["tweets"],
            "endpoint": os.getenv("TWITTER_API_URL")
        }
    ]
    
    for provider in providers:
        ProviderService.register_provider(
            id=provider['id'],
            name=provider['name'],
            entity_type=provider['entity_type'],
            attributes=provider['attributes'],
            endpoint=provider['endpoint']
        )
```

### 6.2 Actualización Periódica

**Scheduler (APScheduler):**

```python
# backend/services/provider_service.py

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

@scheduler.scheduled_job('interval', minutes=5)
def refresh_external_attributes():
    """Cada 5 minutos, actualizar datos de proveedores"""
    stores = OrionService.get_entities("Store")
    
    for store in stores:
        # Obtener temperatura
        temp_data = requests.get(f"{WEATHER_API_URL}?city={store.name}")
        OrionService.update_entity(store['id'], {
            "temperature": {"value": temp_data['temp']},
            "relativeHumidity": {"value": temp_data['humidity']}
        })
        
        # Obtener tweets
        tweets = requests.get(f"{TWITTER_API_URL}?q={store.name}#smartstore")
        OrionService.update_entity(store['id'], {
            "tweets": {"value": tweets['sentiment_analysis']}
        })

scheduler.start()
```

---

## 7. Inicialización del Sistema

### 7.1 Diagrama de Secuencia (Startup)

```
1. Docker-compose up
   ├─ Levanta MongoDB
   ├─ Levanta Orion
   └─ Levanta Flask app

2. Flask app.py inicia
   ├─ Carga config.py (URLs, credenciales)
   ├─ Conecta a Orion (healthcheck)
   ├─ Conecta a MongoDB (indirect via Orion)
   └─ Inicia Socket.IO server

3. import_data.py ejecuta
   ├─ Lee import-data/*.json
   ├─ Valida estructuras
   └─ Crea entidades en Orion

4. Crear Entidades (POST /v2/entities)
   ├─ 10 Products
   ├─ 4 Stores (con location: geo:point)
   ├─ 4 Employees
   ├─ 16 Shelves
   └─ 64+ InventoryItems

5. Registrar Proveedores (POST /v2/registrations)
   ├─ Temperature provider
   ├─ Humidity provider
   └─ Tweets provider

6. Crear Suscripciones (POST /v2/subscriptions)
   ├─ Suscripción Price Change
   └─ Suscripción Low Stock

7. Scheduler inicia (APScheduler)
   ├─ Background job cada 5 min
   └─ Refresh external attributes

8. App lista
   ├─ Escucha puerto 5000
   ├─ Socket.IO server activo
   └─ Endpoints disponibles
```

### 7.2 Script de Inicialización

```python
# backend/app.py

def initialize_app():
    """Inicializar sistema"""
    print("[INIT] Iniciando FIWARE Smart Store...")
    
    try:
        # 1. Health check Orion
        response = requests.get(f"{ORION_URL}/version")
        print(f"[INIT] Orion conectado: {response.json()}")
        
        # 2. Cargar datos iniciales
        import_data()
        print("[INIT] Datos iniciales cargados")
        
        # 3. Registrar proveedores
        register_external_providers()
        print("[INIT] Proveedores externos registrados")
        
        # 4. Crear suscripciones
        create_subscriptions()
        print("[INIT] Suscripciones configuradas")
        
        # 5. Iniciar scheduler
        start_scheduler()
        print("[INIT] Scheduler iniciado")
        
        print("[INIT] ✓ Sistema listo")
        
    except Exception as e:
        print(f"[ERROR INIT] {e}")
        raise

if __name__ == '__main__':
    initialize_app()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
```

---

## 8. Estructura de Carpetas Completa

```
/home/vvero/XDEI/P2/
│
├── README.md                    # Guía de instalación y uso
├── PRD.md                       # Documento de requisitos
├── architecture.md              # Este archivo
├── data_model.md               # Modelo de datos
├── specification.md            # Especificación original
├── .gitignore                  # Exclusiones Git
├── .env.example                # Variables de entorno (plantilla)
├── docker-compose.yml          # Infraestructura
│
├── backend/
│   ├── app.py                  # Punto de entrada Flask
│   ├── config.py               # Configuración de la app
│   ├── requirements.txt        # Dependencias Python
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── orion_service.py    # CRUD a Orion
│   │   ├── subscription_service.py
│   │   ├── provider_service.py
│   │   └── notification_service.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── products.py
│   │   ├── stores.py
│   │   ├── employees.py
│   │   ├── inventory.py
│   │   └── notifications.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── helpers.py
│   │   ├── validators.py
│   │   └── decorators.py
│   │
│   └── data/
│       └── import_data.py      # Script de carga inicial
│
├── frontend/
│   ├── index.html              # Layout principal
│   │
│   ├── css/
│   │   ├── styles.css
│   │   ├── dark-mode.css
│   │   ├── responsive.css
│   │   ├── components/
│   │   │   ├── navbar.css
│   │   │   ├── table.css
│   │   │   ├── modal.css
│   │   │   └── notification.css
│   │   └── utils/
│   │       └── variables.css
│   │
│   └── js/
│       ├── socket.js
│       ├── views/
│       │   ├── home.js
│       │   ├── products.js
│       │   ├── stores.js
│       │   ├── employees.js
│       │   ├── store-detail.js
│       │   ├── product-detail.js
│       │   └── stores-map.js
│       ├── components/
│       │   ├── table.js
│       │   ├── modal.js
│       │   ├── notification.js
│       │   ├── map.js
│       │   └── 3d-viewer.js
│       └── utils/
│           ├── api.js
│           ├── i18n.js
│           ├── theme.js
│           ├── formatters.js
│           └── helpers.js
│
└── import-data/                # Datos iniciales (JSON)
    ├── products.json
    ├── stores.json
    ├── employees.json
    ├── shelves.json
    └── inventory.json
```

---

## 9. Infraestructura: Docker Compose

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  
  mongodb:
    image: mongo:5.0
    container_name: fiware-mongodb
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: root
    volumes:
      - mongodb_data:/data/db
    networks:
      - fiware

  orion:
    image: fiware/orion:latest
    container_name: fiware-orion
    ports:
      - "1026:1026"
    depends_on:
      - mongodb
    environment:
      DB_HOST: mongodb
      DB_USERNAME: root
      DB_PASSWORD: root
    command: -dbhost mongodb -rplSet rs0
    networks:
      - fiware

  backend:
    build: ./backend
    container_name: smart-store-backend
    ports:
      - "5000:5000"
    depends_on:
      - orion
    environment:
      FLASK_ENV: development
      ORION_URL: http://orion:1026
      MONGODB_URL: mongodb://root:root@mongodb:27017/
      WEATHER_API_URL: ${WEATHER_API_URL}
      TWITTER_API_URL: ${TWITTER_API_URL}
    volumes:
      - ./backend:/app
    networks:
      - fiware

  frontend:
    image: nginx:latest
    container_name: smart-store-frontend
    ports:
      - "8080:80"
    volumes:
      - ./frontend:/usr/share/nginx/html
    depends_on:
      - backend
    networks:
      - fiware

volumes:
  mongodb_data:

networks:
  fiware:
    driver: bridge
```

**Puertos:**
- 5000: Flask Backend
- 8080: Frontend (Nginx)
- 1026: Orion Context Broker
- 27017: MongoDB

---

## 10. Flujos de Datos Específicos

### 10.1 Lectura de Tienda con Inventario

```
Frontend: GET /api/stores/<store_id>/inventory
  ↓
Backend (REST route):
  ├─ OrionService.get_entity(store_id) → Store
  ├─ OrionService.get_entities("InventoryItem", q=refStore==store_id)
  ├─ Para cada InventoryItem:
  │  ├─ Get Product (via refProduct)
  │  ├─ Get Shelf (via refShelf)
  │  └─ Agrupar por Shelf
  └─ Return: JSON agrupado
  
  ↓
Orion/MongoDB: Queries
  GET /v2/entities?type=Store&id=STORE-001
  GET /v2/entities?type=InventoryItem&q=refStore==STORE-001
  GET /v2/entities?type=Product&ids=...
  GET /v2/entities?type=Shelf&ids=...
  
  ↓
Frontend: Renderizar tabla agrupada por Shelf
  [Shelf A1]
    - Producto 1: 5 en almacén, 3 en estantería
    - Producto 2: 10 en almacén, 8 en estantería
  [Shelf A2]
    - Producto 3: 2 en almacén, 2 en estantería
  (Progress bars visualizan ocupación)
```

### 10.2 Búsqueda con Filtros de Productos

```
Frontend: GET /api/products?search=laptop&size=M&price_min=500&price_max=1000
  ↓
Backend: OrionService construye query NGSIv2
  GET /v2/entities?type=Product&q=name~=*laptop*;size==M;price>500;price<1000
  ↓
MongoDB: Query con índices
  ├─ Index name (text search)
  ├─ Index size
  └─ Index price
  
  ↓
Respuesta: Array de Products
  ├─ PRD-001: Laptop Dell XPS (size: M, price: 899.99)
  ├─ PRD-002: Laptop HP Pavilion (size: M, price: 649.99)
  └─ ...
  
  ↓
Frontend JS: 
  - Aplica debounce (300ms) a búsqueda
  - Renderiza tabla con resultados
  - Paginación si > 20 resultados
```

---

## 11. Consideraciones de Rendimiento

1. **Caché:** Frontend cachea productos/tiendas/empleados (localStorage, IndexedDB)
2. **Lazy Loading:** Tablas cargan por página (10 items/página)
3. **Índices MongoDB:** Crear en id, type, refProduct, refStore, refShelf
4. **Throttling Suscripciones:** 300s throttling para evitar spam de notificaciones
5. **Compresión:** Gzip en respuestas HTTP
6. **CDN:** CSS/JS minimizados, imágenes optimizadas

---

## 12. Seguridad y Autenticación

**Autenticación:**
- Tabla Employee con username/password (hasheado con bcrypt)
- Login genera JWT token
- Token almacenado en localStorage
- Headers Authorization en requests

**Autorización:**
- Middleware verifica JWT
- Empleados ven solo su tienda (filtro refStore)
- Gerentes ven todas las tiendas
- Admin acceso completo

**Variables Sensibles:**
- `.env` con credenciales (NO en Git)
- `--env-file` en docker-compose
- URLs de APIs externas

---

## Referencias Cruzadas

- **PRD.md:** Requisitos que esta arquitectura implementa
- **data_model.md:** Estructura de datos NGSIv2 que circula aquí
- **specification.md:** Contexto original y restricciones
