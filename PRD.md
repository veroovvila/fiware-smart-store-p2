# PRD: FIWARE Smart Store – Práctica 2

## Executive Summary

**FIWARE Smart Store** es una aplicación web basada en FIWARE (NGSIv2) que gestiona tiendas inteligentes con integración en tiempo real, visualización interactiva y notificaciones automáticas. El sistema permite a gerentes, empleados y clientes interactuar con un ecosistema de tiendas conectadas, inventario distribuido y proveedores de datos externos (temperatura, humedad, redes sociales).

**Contexto:** Práctica 2 del curso de FIWARE, implementando patrones de arquitectura moderna con notificaciones en tiempo real y datos contextuales dinámicos.

---

## 🎯 Objetivos del Sistema

### Objetivo Principal
Desarrollar una solución FIWARE basada en NGSIv2 que gestione tiendas inteligentes mediante el Orion Context Broker, demostrando integración real de datos contextuales, suscripciones y notificaciones.

### Objetivos Secundarios

1. **Integración NGSIv2 con Orion Context Broker**
   - Crear, leer, actualizar y eliminar entidades mediante REST API
   - Implementar referencias entre entidades (Product ↔ InventoryItem ↔ Store, etc.)
   - Demostrar uso de metadata en atributos

2. **Notificaciones en Tiempo Real**
   - Suscripciones a cambios de precios en productos
   - Alertas de bajo stock en estanterías
   - Transmisión a frontend mediante Socket.IO para actualización sin reload

3. **Visualización Interactiva**
   - Mapa geográfico de tiendas con Leaflet
   - Vista 3D del layout de tienda con Three.js
   - Tablas dinámicas con filtros y búsqueda

4. **Gestión Distribuida de Inventario**
   - Organización jerárquica: Tienda → Estantería → Producto
   - Conteo de stock en almacén vs. estantería visible
   - Operaciones de compra actualizando estado en Orion

5. **Experiencia de Usuario Multiidioma y Accesible**
   - Soporte de español e inglés (i18n)
   - Modo oscuro y claro (theme switcher)
   - Interfaz responsive para dispositivos móviles
   - Uso de iconos (Font Awesome) para accesibilidad

---

## 📋 Requisitos Funcionales (RF)

### RF1: Gestión de Productos
- **RF1.1** Listar todos los productos con atributos: nombre, precio, tamaño, color, imagen, país origen
- **RF1.2** Crear nuevo producto con validación de datos (precio > 0, tamaño en {S,M,L,XL}, color hex válido)
- **RF1.3** Actualizar precio de producto → dispara suscripción de cambio de precio
- **RF1.4** Actualizar otros atributos (nombre, tamaño, color, imagen)
- **RF1.5** Eliminar producto (solo si no tiene inventario asociado)
- **RF1.6** Vista detallada de producto mostrando inventario por tienda

### RF2: Gestión de Tiendas
- **RF2.1** Listar todas las tiendas con atributos: nombre, código país, temperatura, humedad, imagen
- **RF2.2** Crear tienda con geolocalización (latitud/longitud)
- **RF2.3** Actualizar información de tienda (nombre, URL, teléfono, capacidad, descripción)
- **RF2.4** Eliminar tienda
- **RF2.5** Ver atributos externos en tiempo real: temperatura, humedad relativa, tweets
- **RF2.6** Vista detallada de tienda con mapa (Leaflet) y vista 3D (Three.js)
- **RF2.7** Mostrar inventario agrupado por estantería

### RF3: Gestión de Empleados
- **RF3.1** Listar empleados con atributos: nombre, rol, tienda asignada, skills
- **RF3.2** Crear empleado asignado a una tienda con skills (MachineryDriving, WritingReports, CustomerRelationships)
- **RF3.3** Actualizar datos de empleado (salario, rol, email, skills)
- **RF3.4** Eliminar empleado
- **RF3.5** Autenticación: login con username/password

### RF4: Gestión de Inventario
- **RF4.1** Crear InventoryItem vinculando Producto + Tienda + Estantería
- **RF4.2** Actualizar cantidad en almacén (stockCount)
- **RF4.3** Actualizar cantidad en estantería (shelfCount)
- **RF4.4** Operación de compra: decrementar stockCount mediante PATCH
- **RF4.5** Listar inventario de tienda agrupado por estantería
- **RF4.6** Listar inventario de producto agrupado por tienda
- **RF4.7** Alerta cuando stockCount < umbral (bajo stock)

### RF5: Gestión de Estanterías
- **RF5.1** Crear estantería en tienda con nombre y capacidad
- **RF5.2** Listar estanterías de tienda
- **RF5.3** Actualizar estantería
- **RF5.4** Eliminar estantería (solo si no tiene inventario)
- **RF5.5** Ver progreso de ocupación (items presentes / capacidad)

### RF6: Suscripciones y Notificaciones
- **RF6.1** Suscripción 1: Cambio de precio en cualquier producto
  - Evento: Cuando price cambia en tabla Product
  - Notificación: Backend recibe desde Orion
  - Acción: Emitir por Socket.IO a clientes
- **RF6.2** Suscripción 2: Bajo stock en inventario
  - Evento: Cuando stockCount < 5 en InventoryItem
  - Notificación: Backend recibe desde Orion
  - Acción: Emitir alerta por Socket.IO
- **RF6.3** Interfaz visual de notificaciones en navbar/toast
- **RF6.4** Historial de últimas 10 notificaciones accesible

### RF7: Proveedores Externos
- **RF7.1** Registro de proveedor de temperatura (weather API)
- **RF7.2** Registro de proveedor de humedad relativa (weather API)
- **RF7.3** Registro de proveedor de tweets (social media API)
- **RF7.4** Actualización periódica de datos externos (cada 5 minutos)
- **RF7.5** Store muestra valores actualizados de temperatura, humedad y tweets

### RF8: Vistas Web
- **RF8.1** Home: Dashboard con estadísticas (total tiendas, productos, empleados, inventario)
- **RF8.2** Home: Diagrama UML del modelo de datos en Mermaid
- **RF8.3** Products: Tabla de productos con filtros por tamaño, precio, país origen
- **RF8.4** Stores: Tabla de tiendas con filtros por país
- **RF8.5** Employees: Tabla de empleados con filtros por rol y tienda
- **RF8.6** Store Detail: Mapa (Leaflet) de ubicación, vista 3D (Three.js), inventario por estantería, tweets
- **RF8.7** Product Detail: Inventario agrupado por tienda, gráfico de distribución
- **RF8.8** Stores Map: Mapa global con todas las tiendas y popups con info

### RF9: Operaciones CRUD
- **RF9.1** CRUD de Products (POST, GET, PATCH, DELETE)
- **RF9.2** CRUD de Stores (POST, GET, PATCH, DELETE)
- **RF9.3** CRUD de Employees (POST, GET, PATCH, DELETE)
- **RF9.4** CRUD de InventoryItems (POST, GET, PATCH, DELETE)
- **RF9.5** CRUD de Shelves (POST, GET, PATCH, DELETE)

### RF10: Operaciones de Compra
- **RF10.1** Endpoint PATCH para decrementar stockCount de InventoryItem
- **RF10.2** Validación: stockCount no puede ser negativo
- **RF10.3** Trigger de suscripción si stockCount cae bajo umbral

---

## 🔧 Requisitos No Funcionales (NF)

### Rendimiento
- **NF1.1** Notificaciones en tiempo real < 500ms desde evento Orion hasta UI
- **NF1.2** Listados de productos/tiendas/empleados carguen en < 2 segundos
- **NF1.3** Búsqueda y filtros respondan inmediatamente (debounce < 300ms)

### Usabilidad
- **NF2.1** Interfaz intuitiva sin documentación adicional
- **NF2.2** Soporte multiidioma (ES/EN) para todos los textos
- **NF2.3** Tema oscuro no causa fatiga ocular, contraste WCAG AA mínimo
- **NF2.4** Navbar fijo facilita navegación entre vistas
- **NF2.5** Iconos (Font Awesome) aumentan claridad visual

### Escalabilidad
- **NF3.1** Arquitectura basada en servicios reutilizables (OrionService, SubscriptionService, etc.)
- **NF3.2** Posibilidad de agregar nuevos proveedores externos sin cambios importantes
- **NF3.3** Base de datos (MongoDB) puede manejar N tiendas/productos

### Compatibilidad
- **NF4.1** Navegadores modernos: Chrome, Firefox, Safari, Edge (últimas 2 versiones)
- **NF4.2** JavaScript ES6+ sin polyfills
- **NF4.3** Infraestructura: Docker Compose para fácil despliegue

### Seguridad
- **NF5.1** Passwords hasheados (no almacenar en texto plano)
- **NF5.2** Autorización básica por rol (empleado, gerente, admin)
- **NF5.3** Variables sensibles en .env (URLs Orion, credenciales)

### Mantenibilidad
- **NF6.1** Código comentado en secciones complejas
- **NF6.2** GitHub Flow obligatorio: issues, ramas, PRs
- **NF6.3** README.md con instrucciones de setup y uso
- **NF6.4** Estructura de carpetas clara y organizada

---

## 👤 Historias de Usuario

### Historia 1: Gerente – Ver Dashboard
**Como** gerente de tienda  
**Quiero** ver un dashboard con estadísticas globales (total tiendas, productos, empleados, inventario)  
**Para** tener una visión de negocio completa al iniciar la aplicación

**Criterios de Aceptación:**
- Dashboard muestra: 4 tarjetas con números (tiendas, productos, empleados, items inventario)
- Incluye diagrama UML generado dinámicamente con Mermaid
- Carga en < 2 segundos

---

### Historia 2: Gerente – Recibir Alerta de Precio Cambiante
**Como** gerente  
**Quiero** recibir una notificación en tiempo real cuando cambia el precio de un producto  
**Para** estar informado de cambios de precios inmediatamente

**Criterios de Aceptación:**
- Al cambiar price en un Product en Orion, se dispara notificación
- Notificación llega al frontend via Socket.IO en < 500ms
- Toast/banner visual aparece en navbar
- Historial de notificaciones accesible

---

### Historia 3: Gerente – Alerta de Bajo Stock
**Como** gerente de tienda  
**Quiero** recibir alerta cuando el stock de un producto cae bajo un umbral (< 5)  
**Para** reponer inventario antes de agotar

**Criterios de Aceptación:**
- Suscripción en Orion monitorea stockCount < 5
- Notificación indica: producto, tienda, estantería, cantidad actual
- Toast destacado en interfaz
- Puede ackowledgear notificación

---

### Historia 4: Vendedor – Registrar Compra
**Como** vendedor de tienda  
**Quiero** registrar una compra decrementando el stock de un producto  
**Para** mantener el inventario actualizado

**Criterios de Aceptación:**
- En vista de tienda, hacer click en producto → "Comprar"
- Decremente shelfCount y stockCount via PATCH
- Confirmar cambio en tabla sin reload
- Si stockCount < 5, dispara notificación

---

### Historia 5: Gerente – Ver Tienda en 3D
**Como** gerente  
**Quiero** visualizar el layout de una tienda en 3D (Three.js)  
**Para** entender la distribución física de estanterías

**Criterios de Aceptación:**
- Vista detallada de tienda incluye canvas 3D
- Three.js renderiza estanterías como cubos
- Rotación con mouse funciona
- Mostrar labels de estantería

---

### Historia 6: Empleado – Login y Acceso
**Como** empleado  
**Quiero** hacer login con username y password  
**Para** acceder solo a información de mi tienda asignada

**Criterios de Aceptación:**
- Campo de login en inicio
- Validación contra Employee en Orion
- Post-login, restricción de vistas por tienda
- Session/token persiste en navegador

---

### Historia 7: Cliente – Buscar Producto
**Como** cliente potencial  
**Quiero** buscar un producto por nombre, filtrar por tamaño/precio/color  
**Para** encontrar lo que busco rápidamente

**Criterios de Aceptación:**
- Vista Products tiene búsqueda de texto
- Filtros por tamaño (S/M/L/XL), rango de precio, país origen
- Resultados actualizan en < 300ms
- Muestra disponibilidad por tienda

---

### Historia 8: Cliente – Ver Mapa de Tiendas
**Como** cliente  
**Quiero** ver un mapa interactivo de todas las tiendas (Leaflet)  
**Para** encontrar la tienda más cercana

**Criterios de Aceptación:**
- Vista Stores Map muestra mapa global
- Marcadores en coordenadas de tiendas
- Click en marcador → popup con nombre, dirección, teléfono
- Zoom y pan funcionan

---

### Historia 9: Gerente – Crear Nueva Tienda
**Como** gerente corporativo  
**Quiero** crear una nueva tienda en el sistema con ubicación GPS  
**Para** expandir la red

**Criterios de Aceptación:**
- Formulario con campos: nombre, país, lat/lon, capacidad, URL, teléfono
- Validación de coordenadas válidas
- Crear automáticamente 4 estanterías por defecto
- Redirigir a vista de tienda creada

---

### Historia 10: Gerente – Cargar Inventario Inicial
**Como** gerente  
**Quiero** cargar productos e inventario desde import-data al iniciar  
**Para** no tener que ingresar manualmente 64+ items

**Criterios de Aceptación:**
- Script de importación en startup
- Lee JSON de import-data/
- Crea 10 Products, 4 Stores, 4 Employees, 64+ InventoryItems
- Valida relaciones (product → shelf → store)
- Log de importación visible

---

### Historia 11: Jefe de Almacén – Inventario por Estantería
**Como** jefe de almacén  
**Quiero** ver el inventario de mi tienda agrupado por estantería  
**Para** gestionar espacios físicamente

**Criterios de Aceptación:**
- Vista Store Detail agrupa InventoryItems por Shelf
- Cada estantería muestra: nombre, capacidad, items presentes, % ocupación
- Barra de progreso visual por estantería
- Click en estantería → desglose de productos

---

### Historia 12: Analyst – Ver Distribución de Producto
**Como** analista de negocio  
**Quiero** ver dónde está distribuido un producto (qué tiendas, cuánto en cada una)  
**Para** entender patrón de ventas

**Criterios de Aceptación:**
- Vista Product Detail muestra tabla: tienda, cantidad almacén, cantidad estantería
- Gráfico tipo pie/bar con distribución por tienda
- Suma total de inventario

---

### Historia 13: Admin – Gestionar Empleados
**Como** administrador  
**Quiero** crear, actualizar, eliminar empleados asignándolos a tiendas  
**Para** mantener el directorio actual

**Criterios de Aceptación:**
- Formulario completo: nombre, email, rol, tienda, salary, skills checkbox
- Validación de email único
- Encriptación de password
- Tabla de empleados con filtros por tienda y rol

---

### Historia 14: Meteorólogo Externo – Temperatura en Tiempo Real
**Como** proveedor de datos meteorológicos  
**Quiero** que mis datos de temperatura se actualicen en la tienda cada 5 minutos  
**Para** reflejar condiciones reales del aire acondicionado

**Criterios de Aceptación:**
- Proveedor registrado en Orion con endpoint de datos
- Orion consulta proveedor periódicamente
- Temperature en Store actualiza sin reload en UI
- Metadata indica "WeatherAPI" como origen

---

### Historia 15: Social Media Manager – Tweets de Tienda
**Como** community manager  
**Quiero** que aparezcan tweets relacionados con cada tienda en su vista  
**Para** mostrar engagement de clientes

**Criterios de Aceptación:**
- Vista Store Detail muestra widget de tweets
- Atributo tweets en Store actualizado por proveedor externo
- Refresh cada 5 minutos
- Tweets mostrados en panel lateral

---

### Historia 16: Usuario – Cambiar Idioma
**Como** usuario  
**Quiero** cambiar la interfaz entre español e inglés  
**Para** usar la aplicación en mi idioma preferido

**Criterios de Aceptación:**
- Button de idioma en navbar (ES/EN)
- Todos los labels, botones, tablas cambian de idioma
- Preferencia guardada en localStorage
- Persistente entre sesiones

---

### Historia 17: Usuario – Modo Oscuro
**Como** usuario nocturno  
**Quiero** activar tema oscuro en la interfaz  
**Para** reducir fatiga ocular

**Criterios de Aceptación:**
- Toggle en navbar activar/desactivar dark mode
- CSS se aplica completo (colores, fondo, texto)
- Contraste WCAG AA mínimo
- Preferencia guardada en localStorage

---

### Historia 18: Técnico – Documentación de Arquitectura
**Como** técnico nuevo en el proyecto  
**Quiero** leer documentación clara de arquitectura, modelo de datos, endpoints  
**Para** entender cómo funcionan los sistemas

**Criterios de Aceptación:**
- Archivos: architecture.md, data_model.md, API.md (si aplica)
- Diagramas Mermaid incluidos
- Ejemplos JSON de suscripciones
- Flujos de datos paso a paso

---

### Historia 19: DevOps – Desplegar con Docker
**Como** DevOps engineer  
**Quiero** levantar toda la infraestructura con docker-compose  
**Para** tener ambiente reproducible

**Criterios de Aceptación:**
- docker-compose.yml con 3 servicios: Flask, MongoDB, Orion
- .env con variables de configuración
- README con instrucciones: git clone, cp .env, docker-compose up
- Ports: 5000 (Flask), 27017 (MongoDB), 1026 (Orion)

---

### Historia 20: QA – Validación de Datos
**Como** tester  
**Quiero** validaciones correctas en formularios (precio > 0, tamaño en enum, color hex válido)  
**Para** evitar datos inválidos en base de datos

**Criterios de Aceptación:**
- Formulario rechaza precio negativo
- Tamaño solo acepta S/M/L/XL
- Color valida formato hex (#RRGGBB)
- Mensajes de error descriptivos

---

## 📦 Datos Iniciales (Dataset)

### Especificación Exacta

| Entidad | Cantidad | Detalles |
|---------|----------|----------|
| **Stores** | 4 | Madrid, Barcelona, Valencia, Bilbao |
| **Employees** | 4 | Distribuidos: 1-2 por tienda |
| **Products** | 10 | Diverso: laptops, ropa, accesorios |
| **Shelves** | 16 (4/store) | 4 por cada tienda |
| **InventoryItems** | ≥64 | ≥4 productos por estantería |

### Ubicación Fuente
- Directorio: `/home/vvero/XDEI/P2/import-data/`
- Formato: JSON (productos, tiendas, empleados, inventario)
- Script importación: Backend lee y crea entidades POST a Orion

### Inicialización
- Al iniciar app.py:
  1. Conexión a Orion
  2. Crear 10 Products (GET check existencia primero)
  3. Crear 4 Stores
  4. Crear 4 Employees
  5. Crear 16 Shelves
  6. Crear 64+ InventoryItems
  7. Registrar 3 proveedores externos

---

## 🔐 Restricciones y Dependencias

### Stack Tecnológico Obligatorio
- **Backend:** Flask + Flask-SocketIO
- **Frontend:** HTML5 + CSS3 + JavaScript (ES6+)
- **Broker:** FIWARE Orion (NGSIv2)
- **Base de datos:** MongoDB
- **Containerización:** Docker + Docker Compose

### Dependencias del Proyecto
1. FIWARE Orion ejecutándose (puerto 1026)
2. MongoDB conexionado a Orion (puerto 27017)
3. Python 3.8+ con Flask instalado
4. Node.js NO requerido (JS puro, sin build)

### Restricciones de Negocio
1. GitHub Flow obligatorio:
   - 1 issue por funcionalidad
   - 1 rama por issue (feature/*, fix/*, etc.)
   - 1 PR con review antes de merge a main
2. Todos los cambios documentados en commits
3. README.md actualizado con instrucciones
4. Especificación.md es source of truth

### Restricciones Técnicas
1. Multiidioma (ES/EN) en todos los textos
2. Dark/Light mode debe ser funcional
3. Responsive design (mobile-first si es posible)
4. NGSIv2 es estándar, no NGSIv3
5. Socket.IO para comunicación real-time
6. Leaflet + Three.js para visualización

---

## 📊 Criterios de Éxito

✅ **Funcional:**
- Todas las 20 historias de usuario implementadas
- CRUD completo para 5 entidades
- 2 suscripciones funcionando (precio, stock bajo)
- 3 proveedores externos registrados

✅ **Técnico:**
- Notificaciones en tiempo real < 500ms
- Interfaz responsive y accesible
- Código documentado
- Docker-compose funcional

✅ **Procesos:**
- GitHub Flow seguido para cada feature
- Documentación actualizada
- Commits semánticos
- PRs revisadas

---

## 📝 Referencias Cruzadas

- Ver **architecture.md** para detalles técnicos de cómo se implementan estos requisitos
- Ver **data_model.md** para definición exacta de entidades y relaciones NGSIv2
- Ver **specification.md** para contexto inicial del proyecto
