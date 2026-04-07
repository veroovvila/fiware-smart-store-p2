# FIWARE Smart Store – Práctica 2 (Especificación Detallada)

## 🎯 Objetivo
Desarrollar una aplicación FIWARE basada en NGSIv2 que gestione tiendas inteligentes, integrando:

- Gestión de productos, tiendas y empleados
- Inventario distribuido en estanterías
- Integración con Orion Context Broker
- Suscripciones y notificaciones en tiempo real
- Proveedores de contexto externo
- Interfaz web interactiva

---

# 🧩 MODELO DE DATOS

## 📦 Product
Atributos:
- id (string)
- name (Text)
- price (Number)
- size (Text: S, M, L, XL)
- image (URL)
- originCountry (Text)
- color (Text, formato HEX RGB)

---

## 🏬 Store
Atributos:
- id
- name
- image
- location (coordenadas)
- url
- telephone
- countryCode (2 caracteres)
- capacity (m³)
- description (texto largo)

### Atributos externos:
- temperature (external provider)
- relativeHumidity (external provider)
- tweets (external provider)

---

## 👨‍💼 Employee
Atributos:
- id
- name
- image
- salary
- role
- email
- dateOfContract
- username
- password
- skills:
  - MachineryDriving
  - WritingReports
  - CustomerRelationships
- refStore (relación a Store)

---

## 📦 InventoryItem
- id
- refProduct
- refStore
- refShelf
- stockCount
- shelfCount

---

## 🧱 Shelf
- id
- name
- capacity
- refStore

---

# 🔗 RELACIONES

- Employee → Store (1:N)
- Store → Shelf (1:N)
- Shelf → InventoryItem (1:N)
- Product → InventoryItem (1:N)
- Store → InventoryItem (1:N)

---

# 📊 DIAGRAMA UML

Debe generarse usando Mermaid y mostrarse en Home.

---

# 📦 DATOS INICIALES

- 4 Stores
- 4 Employees
- 10 Products
- 4 Shelves por Store
- ≥ 4 productos por Shelf

Basado en `import-data`

---

# 🌍 PROVEEDORES EXTERNOS

- temperature
- relativeHumidity
- tweets

Registro en Orion al iniciar la app

---

# 🔔 SUSCRIPCIONES

Eventos:
- Cambio de precio de Product
- Bajo stock en Store

Notificaciones:
- Orion → Flask
- Flask → navegador (Socket.IO)

---

# 🖥️ INTERFAZ

## 🌐 Vistas
- Home
- Products
- Stores
- Employees
- Store Detail
- Product Detail
- Stores Map

---

## 📋 Tablas

### Products:
- image, name, price, size, color

### Stores:
- countryCode, temperature, humidity

### Employees:
- category, skills

---

## 🏬 Vista Store

- Mapa (Leaflet)
- Vista 3D (Three.js)
- Inventario agrupado por Shelf
- Barra de progreso
- Tweets
- Notificaciones

---

## 📦 Vista Product

- Inventario agrupado por Store

---

# 🎨 UI/UX

- Multiidioma (ES / EN)
- Dark / Light mode
- Navbar fija
- Uso de iconos (Font Awesome)
- CSS > JS

---

# ⚙️ OPERACIONES

## Compra de producto

PATCH:
/v2/entities/<inventoryitem_id>/attrs


---

# 🧠 ARQUITECTURA

## Backend
- Flask
- Flask-SocketIO
- Servicios:
  - OrionService
  - SubscriptionService
  - ProviderService

## Frontend
- HTML + CSS + JS
- Socket.IO

## Infraestructura
- Docker
- Orion
- MongoDB

---

# 🔁 GITHUB FLOW

Cada funcionalidad:
1. Plan
2. Issue
3. Branch
4. Implementación
5. Merge
6. Update docs

---

# 📄 ARCHIVOS CLAVE

- PRD.md
- architecture.md
- data_model.md
- AGENTS.md
- README.md