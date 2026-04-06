# Phase 5: Frontend Integration - Quick Start Guide

## 📁 Frontend Structure

La arquitectura frontend sigue un patrón modular limpio con Vanilla JS:

```
frontend/
├── index.html                 # HTML base
├── css/
│   └── style.css             # Estilos responsive
└── js/
    ├── config.js             # Configuración centralizada
    ├── api.js                # Capa de API (fetch calls)
    ├── ui.js                 # Rendering y actualización de UI
    ├── events.js             # Event handlers
    ├── notifications.js      # Socket.IO real-time
    └── app.js                # Orquestación principal
```

## 🏗️ Arquitectura

### 4 Capas Separadas

1. **config.js** - Configuración
   - URLs del backend
   - Socket.IO settings
   - Umbrales y constantes UI

2. **api.js** - HTTP Layer
   - `API.getProducts(page, limit, name, min_price, max_price)`
   - `API.getInventory(page, limit, lowStock, productId, storeId)`
   - `API.buyInventoryItem(inventoryId, quantity)`
   - Error handling automático

3. **ui.js** - Rendering Layer
   - `UI.renderProducts(products, pagination)`
   - `UI.renderInventory(items)`
   - `UI.renderStores(stores)`
   - `UI.renderEmployees(employees)`
   - `UI.showError()`, `UI.showSuccess()`
   - `UI.escapeHtml()` para XSS prevention

4. **events.js** - Event Handlers
   - Navigation clicks
   - Filter changes (búsqueda, rango precio, tienda)
   - Buy button clicks
   - Automatic re-render on filter change

5. **notifications.js** - Socket.IO
   - Real-time price changes
   - Low stock alerts
   - Inventory updates
   - New sales notifications

6. **app.js** - Orchestration
   - DOMContentLoaded initialization
   - `App.loadProducts()`, `App.loadInventory()`, etc.
   - `App.buyInventoryItem()` - calls buy endpoint
   - State management (currentPage, products[], etc.)

## 🚀 Cómo Ejecutar

### Opción 1: Abrir directamente en navegador
```bash
cd /home/vvero/XDEI/P2/frontend
# En Windows:
start index.html
# O simplemente abre la carpeta en el navegador y hace clic en index.html
```

### Opción 2: Usar Live Server (recomendado)
```bash
# Instala globalmente (si no lo tienes)
npm install -g live-server

# En la carpeta frontend
live-server

# Se abrirá automáticamente en http://localhost:8080
```

### Opción 3: Servidor Python simple
```bash
cd frontend
python -m http.server 8000
# Accede a http://localhost:8000
```

## ✨ Funcionalidades Implementadas

### ✅ PRODUCTOS (PRODUCTS listing)
- ✅ Listar todos los productos desde `/api/v1/products`
- ✅ Mostrar: nombre, precio, descripción, imagen
- ✅ Filtro por nombre (búsqueda en tiempo real)
- ✅ Filtro por rango de precio (precio mínimo/máximo)
- ✅ Tarjetas responsivas con hover effects
- ✅ Paginación soportada (12 items/página por defecto)

### ✅ INVENTARIO (INVENTORY)
- ✅ Mostrar stock de cada producto en cada tienda
- ✅ Indicador visual de "low stock" (rojo si qty < 10)
- ✅ Botón "Comprar" → llama a `/inventory/{id}/buy`
- ✅ Dialog para seleccionar cantidad a comprar
- ✅ Validación: no permite comprar más del disponible
- ✅ Tabla responsive con filtro por tienda
- ✅ Actualización automática después de compra

### ⚙️ CONFIGURACIÓN DE CONEXIÓN
- ✅ Backend URL: `http://localhost:5000` (en config.js)
- ✅ Manejo de errores de red
- ✅ Respuestas vacías → mensaje "No hay datos"
- ✅ Loading states: spinner durante carga
- ✅ Error states: mensajes claros

### 🔌 REAL-TIME (Socket.IO)
- ✅ Conecta con Socket.IO desde `http://localhost:5000`
- ✅ Escucha eventos en tiempo real:
  - `price_change` - cambios de precio
  - `low_stock` - alertas de stock bajo
  - `inventory_update` - actualizaciones de inventario
  - `new_sale` - notificaciones de nuevas ventas
- ✅ Notificaciones popup automáticas
- ✅ Auto-refresh de datos cuando cambian

### 🏪 TIENDAS (STORES)
- ✅ Listado de tiendas con información
- ✅ Dirección, ciudad, país, teléfono, email
- ✅ Filtro en inventario por tienda

### 👥 EMPLEADOS (EMPLOYEES)
- ✅ Listado de empleados
- ✅ Información: nombre, rol, email

### 📊 DASHBOARD
- ✅ Estadísticas: número de tiendas, productos, inventario, empleados
- ✅ Actualización en tiempo real

## 🎯 Flujo de Uso

1. **Al cargar la página**
   - Se inicializa APP.init()
   - Se cargan configuraciones
   - Se conecta Socket.IO
   - Se muestra Dashboard con estadísticas

2. **Navegar a "Productos"**
   - Clic en nav "Productos"
   - Se cargan todos los productos
   - Se pueden usar filtros: búsqueda y rango de precio
   - Filtros actualizan en tiempo real

3. **Ver Inventario**
   - Clic en nav "Inventario"
   - Se muestra tabla de stock
   - Cada fila tiene botón "Comprar"
   - Se puede filtrar por tienda

4. **Comprar producto**
   - Clic en "Comprar"
   - Dialogo pregunta cantidad
   - Validación de cantidad disponible
   - POST al backend `/inventory/{id}/buy`
   - Recibe confirmación y tabla se actualiza

5. **Novedades en tiempo real**
   - Socket.IO escucha cambios
   - Notificación popup aparece
   - Inventario auto-actualiza si está visible

## 🔧 Configuración

### Cambiar URL del backend
En `js/config.js`:
```javascript
API: {
  BASE_URL: 'http://localhost:5000',  // ← Cambiar aquí
  // ...
}
```

### Cambiar Items por página
En `js/config.js`:
```javascript
UI: {
  ITEMS_PER_PAGE: 12,  // ← Cambiar aquí
  LOW_STOCK_THRESHOLD: 10,  // ← Umbral de stock bajo
}
```

## ✅ Checklist de Testing

- [ ] Abre index.html en navegador
- [ ] Backend corre en http://localhost:5000 ¿Ves "Dashboard" con números?
- [ ] Click en "Productos" - ¿Aparecen los productos?
- [ ] Filtro por nombre - ¿Se actualiza en tiempo real?
- [ ] Filtro por precio - ¿Funciona el rango?
- [ ] Click en "Inventario" - ¿Ves la tabla?
- [ ] Click en "Comprar" - ¿Aparece el dialogo?
- [ ] Ingresas cantidad y compras - ¿Se actualiza la tabla?
- [ ] Socket.IO conecta - ¿Ves notificaciones en caso de cambios?

## 🐛 Debugging

### Abre Developer Console
```
F12 → Console
```

Busca mensajes:
- ✅ "Application initialized successfully" - app lista
- ✅ "Connected to backend via Socket.IO" - Socket.IO conectado
- ❌ Errores rojo - problemas de conexión o API

### Verificar conexión al backend
En console:
```javascript
API.getProducts(1, 12).then(r => console.log(r))
```

Deberías ver los productos en la respuesta.

### Ver Socket.IO events
En console:
```javascript
Notifications.socket.onAny((event, ...args) => {
  console.log(event, args);
});
```

## 📝 Notas Importantes

1. **NO modificar backend** - está perfecto y listo
2. **Todos los endpoints están documentados** en [PHASE4_COMPLETION.md](../PHASE4_COMPLETION.md)
3. **CSV/JSON import** - ya está hecho en Phase 3 (110+ entidades en Orion)
4. **Socket.IO** - backend envia eventos, frontend los escucha
5. **Dashboard** - muestra stats iniciales, se actualiza con Socket.IO

## 🚧 Próximos Pasos (opcionales)

1. Agregar modal para ver detalles de productos
2. Agregar carrito de compras (cliente-side)
3. Agregar gráficos de inventario
4. Agregar búsqueda de empleados por tienda
5. Exportar datos a CSV/PDF

## 💡 Tips

- Frontend se puede desarrollar completamente sin modificar backend
- Usa Chrome DevTools para debugging
- Todos los errores de API van a console.error()
- Las notificaciones desaparecen después de 5 segundos
- Responsive design: funciona en mobile también

---

**Estado**: Phase 5 Iniciado ✅
**Backend**: 100% Listo
**Frontend**: Arquitectura lista, funcionalidades implementadas
**Test**: Ready para testing manual
