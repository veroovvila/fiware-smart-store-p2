# Phase 5: Frontend Testing & Verification

## ✅ Pre-requisitos

- [ ] Backend corriendo en `http://localhost:5000`
- [ ] PostgreSQL/MongoDB funcional  
- [ ] Frontend files en `frontend/` carpeta
- [ ] Navegador moderno (Chrome, Firefox, Safari, Edge)

## 🚀 Inicio Rápido

### Opción 1: Servir con Script (Recomendado)
```bash
cd /home/vvero/XDEI/P2
./serve-frontend.sh
# Se abre automáticamente en http://localhost:8000
```

### Opción 2: Servir Manualmente
```bash
cd /home/vvero/XDEI/P2/frontend
python3 -m http.server 8000
# Accede a http://localhost:8000
```

### Opción 3: Live Server (si tienes Node.js)
```bash
npm install -g live-server
cd frontend
live-server
```

### Opción 4: Abrir directamente
```bash
open frontend/index.html  # macOS
xdg-open frontend/index.html  # Linux
start frontend/index.html  # Windows
```

## 📋 Testing Checklist

### 1. Verificar Backend Disponible ✅

**Endpoint**: GET `http://localhost:5000/health`
**Respuesta esperada**:
```json
{
  "status": "healthy",
  "service": "fiware-smart-store-backend"
}
```

**Comando**:
```bash
curl http://localhost:5000/health
```

### 2. Cargar Página Frontend

1. Abre navegador a `http://localhost:8000`
2. **Verificaciones**:
   - ✅ Página carga sin errores
   - ✅ Navbar visible con navegación
   - ✅ Console (F12) sin errores rojo
   - ✅ Mensaje "Application initialized successfully"
   - ✅ Socket.IO conectando o conectado

**Errores comunes**:
- ❌ CORS error → Backend no tiene CORS habilitado
- ❌ 404 on css/style.css → Archivo no existe
- ❌ Cannot find CONFIG → config.js no cargó

### 3. Verificar Estadísticas del Dashboard

**Pasos**:
1. Frontend carga automáticamente en Dashboard
2. Deberías ver 4 tarjetas con números:
   - Tiendas Activas
   - Productos
   - Inventario Total
   - Empleados

**Valores esperados** (basado en data importada):
- Tiendas: 7
- Productos: 11
- Inventario: 82+ items
- Empleados: 6

**Si no ves números**:
- Abre Console (F12)
- Ejecuta: `API.getProducts(1, 1).then(r => console.log(r))`
- Verifica la respuesta

### 4. Testear Productos (PRODUCTS listing)

#### 4a. Listar Productos
**Pasos**:
1. Clic en navbar "FIWARE Smart Store" o "Dashboard"
2. Deberías ver grid de productos

**Verificaciones**:
- ✅ Mínimo 11 productos visibles (si es la primera página)
- ✅ Cada card muestra: nombre, descripción, precio, imagen
- ✅ Precios en formato €X.XX

**Si no ves productos**:
```bash
curl http://localhost:5000/api/v1/products?page=1&limit=12
```

#### 4b. Filtro por Nombre
**Pasos**:
1. Ingresa "laptop" en campo "Buscar por nombre..."
2. Presiona Enter o espera 1 segundo

**Verificaciones**:
- ✅ Lista filtra en tiempo real
- ✅ Solo muestra productos que coincidan
- ✅ Borra el campo → vuelven todos

**Test case**:
- Busca "Laptop" → debe mostrar Laptop entries
- Busca "xyz" → "No hay productos disponibles"
- Borra → vuelven todos

#### 4c. Filtro por Precio
**Pasos**:
1. Ingresa "100" en "Precio mínimo"
2. Ingresa "500" en "Precio máximo"
3. Observa el cambio

**Verificaciones**:
- ✅ Solo muestra productos entre €100-€500
- ✅ Rango funciona correctamente
- ✅ Combina con búsqueda por nombre

### 5. Testear Inventario (INVENTORY display)

#### 5a. Ver Tabla de Inventario
**Pasos**:
1. Clic en navbar "Inventario"
2. Deberías ver tabla con columnas:
   - Producto
   - Tienda
   - Cantidad
   - Estantería
   - Estado
   - Botón Comprar

**Verificaciones**:
- ✅ Tabla muestra items
- ✅ Cantidades son números
- ✅ Estado muestra ✅ Normal o ⚠️ Stock Bajo

**Low Stock Pattern**:
- Si qty < 10 → ⚠️ Stock Bajo (naranja)
- Si qty ≥ 10 → ✅ Normal (verde)

#### 5b. Filtro por Tienda
**Pasos**:
1. Clic en "Inventario"
2. Select "Todas las tiendas" dropdown
3. Selecciona una tienda específica
4. Observa que filtra

**Verificaciones**:
- ✅ Solo muestra items de esa tienda
- ✅ Vuelve a "Todas las tiendas" → muestra todas

#### 5c. Comprar (BUY functionality)
**Pasos**:
1. Encuentra un item con cantidad > 0
2. Clic en botón "Comprar"
3. Dialogo pregunta cantidad
4. Ingresa cantidad válida (ej: "2")
5. OK

**Verificaciones**:
- ✅ Dialogo aparece
- ✅ Notificación de éxito ✅
- ✅ Cantidad en tabla se actualiza
- ✅ Stock bajo indicator cambia si aplica

**Test cases**:
- Ingresa cantidad válida → Compra OK
- Ingresa cantidad > disponible → Error
- Ingresa cantidad 0 → Error
- Ingresa letra → Error
- Cancela dialogo → Nada sucede

### 6. Testear Real-time (Socket.IO)

#### 6a. Verificar Conexión
**Pasos**:
1. Abre Console (F12)
2. Busca mensaje: "Connected to backend via Socket.IO"

**Verificaciones**:
- ✅ Mensaje aparece después de 1-2 segundos
- ✅ Sin errores en console relacionados a Socket.IO

#### 6b. Test Real-time Notification
**Pasos**:
1. En otra terminal, simula un evento del backend:
```bash
curl -X POST http://localhost:5000/api/v1/inventory/test-notification \
  -H "Content-Type: application/json" \
  -d '{"type":"low_stock", "productName":"Laptop", "quantity":5}'
```

**Verificaciones**:
- ✅ Notificación aparece en pantalla
- ✅ Desaparece después de 5 segundos
- ✅ Sin errores en console

### 7. Testear Tiendas (STORES)

**Pasos**:
1. Clic en navbar "Tiendas"

**Verificaciones**:
- ✅ Grid de tiendas muestra
- ✅ Cada card muestra: nombre, dirección, ciudad, teléfono, email
- ✅ Mínimo 7 tiendas

### 8. Testear Empleados (EMPLOYEES)

**Pasos**:
1. Clic en navbar "Empleados"

**Verificaciones**:
- ✅ Grid de empleados muestra
- ✅ Cada card muestra: nombre, rol, email
- ✅ Mínimo 6 empleados

## 🐛 Debugging Console Commands

### Ver productos en consola
```javascript
API.getProducts(1, 12).then(r => console.log(r))
```

### Ver inventario
```javascript
API.getInventory(1, 12).then(r => console.log(r))
```

### Ver Socket.IO eventos
```javascript
Notifications.socket.onAny((event, ...args) => {
  console.log('Socket event:', event, args);
});
```

### Manual buy test
```javascript
API.buyInventoryItem('urn:ngsi-ld:Inventory:abc123', 2).then(r => console.log(r))
```

### Ver estado de la app
```javascript
console.log({
  products: App.products,
  inventory: App.inventory,
  page: App.currentPage,
  socketConnected: Notifications.isConnected
})
```

## ✅ Final Verification Test

```
[ ] Backend health check: OK
[ ] Frontend loads without errors
[ ] Dashboard shows statistics
[ ] Products list displays 11+ items
[ ] Product name filter works
[ ] Product price filter works
[ ] Inventory table shows items
[ ] Store filter in inventory works
[ ] Buy button opens dialog
[ ] Can buy with valid quantity
[ ] Error on invalid quantity
[ ] Socket.IO connected message appears
[ ] Stores section loads
[ ] Employees section loads
[ ] Console has no red errors
```

## 📊 Expected Data Count

- **Products**: 11
- **Stores**: 7
- **Employees**: 6
- **Inventory Items**: 82+
- **Subscriptions**: 2 active
- **Entities in Orion**: 110+

## 🔧 Common Issues & Solutions

### Issue: CORS Errors
**Error**: "Access to XMLHttpRequest blocked by CORS policy"
**Solution**: Backend already has CORS enabled in Flask. Verify backend running.

### Issue: 404 on CSS/JS files
**Error**: "GET http://localhost:8000/css/style.css 404"
**Solution**: frontend/css/ folder exists with style.css? Check file paths.

### Issue: Socket.IO not connecting
**Error**: "WebSocket connection to ... failed"
**Solution**: Backend Socket.IO needs to be ready. Check backend logs.

### Issue: Products show "No hay productos disponibles"
**Solution**: 
1. Check backend is running: `curl http://localhost:5000/health`
2. Check database has data: `curl http://localhost:5000/api/v1/products`
3. If empty, run data import: `python backend/data/import_data.py`

### Issue: Images not loading
**Cause**: Product images use placeholder URLs
**Solution**: Normal behavior. Images will show placeholder if URL invalid.

## 📈 Performance Notes

- Products load: ~100ms (from backend)
- Inventory page: ~150ms
- Buy operation: ~200ms (includes backend processing)
- Real-time notifications: <100ms latency

## 🎯 Next Steps After Testing

1. ✅ All tests pass → Phase 5 COMPLETE
2. Enhance UI (optional):
   - Modal for product details
   - Shopping cart
   - Order history
3. Add charts/graphs
4. Export to CSV/PDF

---

**Last Updated**: Phase 5 Implementation
**Status**: Testing Ready ✅
**Backend Verified**: Yes
**Frontend Ready**: Yes
