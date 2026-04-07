# 🏪 FIWARE Smart Store - Práctica 2

<div align="center">

![FIWARE Badge](https://img.shields.io/badge/FIWARE-Smart%20Store-blue?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/status-Active-success?style=for-the-badge)
![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge)

**Una solución inteligente y en tiempo real para la gestión de tiendas basada en FIWARE NGSIv2**

[🔗 Repositorio GitHub](https://github.com/veroovvila/fiware-smart-store-p2) • [📚 Documentación](#documentación) • [🚀 Quick Start](#quick-start)

</div>

---

## 📖 Tabla de Contenidos

- [Descripción del Proyecto](#descripción-del-proyecto)
- [Propósito y Contexto](#propósito-y-contexto)
- [Funcionalidades Principales](#funcionalidades-principales)
- [Stack Tecnológico](#stack-tecnológico)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Ejecución](#ejecución)
- [API Reference](#api-reference)
- [Interfaz de Usuario](#interfaz-de-usuario)
- [Roadmap](#roadmap)
- [Contribuyentes](#contribuyentes)
- [Licencia](#licencia)

---

## 🎯 Descripción del Proyecto

**FIWARE Smart Store** es una aplicación web empresarial que demuestra cómo construir sistemas inteligentes de gestión de tiendas utilizando el stack FIWARE. La solución integra:

- **Gestión en tiempo real** de inventario distribuido
- **Notificaciones automáticas** mediante suscripciones NGSIv2
- **Visualización interactiva** de datos geoespaciales y 3D
- **Integración con proveedores externos** (clima, redes sociales, etc.)
- **Experiencia multiusuario** con autenticación y roles

El proyecto implementa patrones de arquitectura moderna incluyendo:
- API REST completa con CRUD operations
- Arquitectura orientada a servicios (SOA)
- WebSockets para comunicación bidireccional
- Validaciones de integridad referencial
- Documentación OpenAPI (Swagger)

---

## 🌍 Propósito y Contexto

Este proyecto es una **Práctica 2 del Curso de FIWARE** diseñada para demostrar:

### Objetivos Clave

| Objetivo | Descripción |
|----------|------------|
| **NGSIv2 Mastery** | Dominar CRUD de entidades y referencias en Orion Context Broker |
| **Real-time Subscriptions** | Implementar suscripciones a cambios de datos contextuales |
| **Smart Data** | Enriquecer datos con atributos externos de proveedores |
| **Full-Stack Integration** | Conectar frontend, backend y middleware en una solución cohesiva |
| **Scalability** | Demostrar patrones escalables con Docker y microservicios |

### Casos de Uso

1. **Gerentes de Tienda**: Monitorean inventario en tiempo real, cambios de precios
2. **Empleados**: Reciben notificaciones de bajo stock, gestión de estanterías
3. **Clientes**: Consultan disponibilidad, ubicación en mapas, información de productos
4. **Analistas**: Pueden integrar datos de clima y redes sociales para análisis

---

## ✨ Funcionalidades Principales

### 🎁 Gestión de Productos
- ✅ Listar, crear, actualizar y eliminar productos
- ✅ Búsqueda avanzada por nombre y rango de precios
- ✅ Validación automática de atributos (precio, tamaño, color hex)
- ✅ Vista detallada con disponibilidad por tienda
- ✅ **Suscripción automática**: Notificación de cambios de precio

### 🏬 Gestión de Tiendas
- ✅ CRUD completo de ubicaciones de tiendas
- ✅ Geolocalización con coordenadas (latitud/longitud)
- ✅ Visualización en mapa interactivo (Leaflet.js)
- ✅ Vista 3D del layout interno (Three.js)
- ✅ **Datos externos**: Temperatura, humedad, análisis de tweets
- ✅ Gestión de estanterías y capacidad

### 👥 Gestión de Empleados
- ✅ CRUD de empleados con roles y skills
- ✅ Asignación a tiendas
- ✅ Email validation automáticas
- ✅ Seguimiento de salario y departamento

### 📦 Gestión de Inventario
- ✅ Vinculación jerárquica: Producto → Tienda → Estantería
- ✅ Conteo de stock en almacén vs. estantería visible
- ✅ Operaciones de compra actualizando stock en tiempo real
- ✅ **Suscripción automática**: Alerta de bajo stock (< 5 unidades)
- ✅ Filtros y agrupación por ubicación

### 🔔 Notificaciones en Tiempo Real
- ✅ WebSocket (Socket.IO) para actualizaciones push
- ✅ Historial de últimas 10 notificaciones
- ✅ Toast notifications persistentes
- ✅ Categorización de alertas (precio, stock, etc.)

### 🌐 Características Transversales
- ✅ **i18n**: Soporte Español/English
- ✅ **Dark/Light Mode**: Theme switcher dinámico
- ✅ **Responsive Design**: Optimizado para mobile/tablet/desktop
- ✅ **Accessibility**: Iconos Font Awesome, ARIA labels
- ✅ **Error Handling**: Validaciones cliente y servidor

---

## 🛠 Stack Tecnológico

### 🎨 Frontend
| Tecnología | Uso |
|-----------|-----|
| **HTML5/CSS3** | Estructura y estilos base |
| **JavaScript ES6+** | Lógica de cliente pura (sin frameworks) |
| **Socket.IO** | Comunicación bidireccional en tiempo real |
| **Leaflet.js** | Mapas interactivos geoespaciales |
| **Three.js** | Visualización 3D del layout de tiendas |
| **Font Awesome** | Iconografía profesional |
| **i18n** | Internacionalización ES/EN |

### ⚙️ Backend
| Tecnología | Uso |
|-----------|-----|
| **Flask 2.3** | Framework web Python ligero |
| **Flask-SocketIO** | Extensión WebSocket para Flask |
| **Flask-CORS** | Cross-Origin Resource Sharing |
| **PyMongo** | Driver MongoDB para Python |
| **APScheduler** | Planificación de tareas background |
| **python-dotenv** | Gestión de variables de entorno |
| **requests** | Cliente HTTP para Orion |
| **bcrypt** | Hashing de contraseñas |

### 🌐 FIWARE Stack
| Componente | Versión | Puerto | Descripción |
|-----------|---------|--------|------------|
| **Orion Context Broker** | Latest | 1026 | Gestión de entidades NGSIv2 |
| **MongoDB** | 5.0 | 27017 | Persistencia de datos |

### 🐳 DevOps
| Tecnología | Uso |
|-----------|-----|
| **Docker** | Containerización de servicios |
| **Docker Compose** | Orquestación multi-contenedor |
| **Nginx** | Servidor web frontend |
| **Environment Variables** | Configuración por entorno |

### 📊 Extras
| Herramienta | Uso |
|-----------|-----|
| **cURL/Postman** | Testing manual de APIs |
| **Git** | Control de versiones |

---

## 📁 Estructura del Proyecto

```
fiware-smart-store-p2/
│
├── 📄 README.md                          # Este archivo
├── 📄 PRD.md                             # Product Requirements Document
├── 📄 architecture.md                    # Documento de Arquitectura
├── 📄 data_model.md                      # Modelo de Datos NGSIv2
├── 📄 docker-compose.yml                 # Orquestación Docker
├── 📄 .env.example                       # Variables de entorno (plantilla)
│
├── 📁 frontend/                          # Aplicación Web
│   ├── 📄 index.html                     # HTML principal (SPA entry point)
│   ├── 📁 css/
│   │   ├── style.css                    # Estilos generales
│   │   ├── dark-mode.css                # Tema oscuro
│   │   └── responsive.css               # Media queries mobile-first
│   ├── 📁 js/
│   │   ├── app.js                       # Bootstrap principal
│   │   ├── config.js                    # Configuración (URLs, constantes)
│   │   ├── api.js                       # Cliente REST para backend
│   │   ├── events.js                    # Manejadores de eventos DOM
│   │   ├── ui.js                        # Templates y DOM manipulation
│   │   ├── notifications.js             # Sistema de notificaciones
│   │   ├── theme.js                     # Dark/Light mode switcher
│   │   ├── i18n.js                      # Sistema de idiomas
│   │   └── socket.js                    # Cliente Socket.IO
│   └── 📁 images/                       # Imágenes de productos y tiendas
│
├── 📁 backend/                          # Aplicación Flask
│   ├── 📄 app.py                        # Factory y setup de Flask
│   ├── 📄 config.py                     # Configuración por entorno
│   ├── 📄 requirements.txt              # Dependencias Python
│   ├── 📄 Dockerfile                    # Containerización backend
│   ├── 📁 routes/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 products.py               # POST/GET/PATCH /products (CRUD)
│   │   ├── 📄 stores.py                 # POST/GET/PATCH /stores (CRUD)
│   │   ├── 📄 employees.py              # POST/GET/PATCH /employees (CRUD)
│   │   └── 📄 inventory.py              # POST/GET/PATCH /inventory (CRUD)
│   ├── 📁 services/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 orion_service.py          # Cliente NGSIv2 (proxy Orion)
│   │   ├── 📄 provider_service.py       # Integración de proveedores externos
│   │   ├── 📄 subscription_service.py   # Gestión de suscripciones Orion
│   │   └── 📄 notification_service.py   # Emisión WebSocket
│   ├── 📁 data/
│   │   ├── 📄 __init__.py
│   │   └── 📄 import_data.py            # Carga inicial de datos de prueba
│   ├── 📁 utils/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 validators.py             # Validaciones de campos
│   │   ├── 📄 helpers.py                # Funciones auxiliares
│   │   └── 📄 decorators.py             # Decoradores (auth, logging, etc.)
│   ├── 📁 import-data/                  # Datos de prueba en JSON
│   │   ├── products.json
│   │   ├── stores.json
│   │   ├── employees.json
│   │   ├── inventory.json
│   │   └── shelves.json
│
├── 📁 import-data/                      # Datos quemados para carga inicial
│   └── (JSON files duplicados de backend/import-data)
│
└── 📄 nginx.conf                         # Configuración Nginx para frontend

```

---

## 📋 Requisitos Previos

### ✅ Sistema
- **OS**: Linux, macOS o Windows (con WSL2)
- **Docker**: v20.0 o superior
- **Docker Compose**: v1.29 o superior

### ✅ Software
```bash
# Verificar versiones
docker --version        # Docker 20.10+
docker-compose --version # Docker Compose 1.29+
git --version          # Git 2.0+
```

### ✅ Navegadores Soportados
- Chrome/Chromium 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### ✅ Puertos Necesarios
La aplicación usa los siguientes puertos (modificables en `.env`):
- `8081` - Frontend (Nginx)
- `5000` - Backend (Flask)
- `1026` - Orion Context Broker
- `27017` - MongoDB

---

## 🚀 Instalación

### Opción 1: Docker Compose (Recomendado)

#### Paso 1: Clonar el repositorio
```bash
git clone https://github.com/veroovvila/fiware-smart-store-p2.git
cd fiware-smart-store-p2
```

#### Paso 2: Configurar variables de entorno
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con valores específicos (opcional)
nano .env
# o
code .env
```

Contenido típico de `.env`:
```env
# Flask
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_PORT=5000

# MongoDB
MONGO_ROOT_USER=root
MONGO_ROOT_PASSWORD=root
MONGO_PORT=27017
MONGO_DB=fiware_smartstore

# Orion
ORION_PORT=1026
ORION_URL=http://orion:1026

# Frontend
FRONTEND_PORT=8081
```

#### Paso 3: Construir y ejecutar
```bash
# Construir las imágenes Docker
docker-compose build

# Ejecutar contenedores en modo detached
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f
```

#### Paso 4: Verificar que todo está funcionando
```bash
# Esperar ~30s a que Orion esté listo
sleep 30

# Verificar servicios
curl http://localhost:5000/health
curl http://localhost:1026/version
```

---

### Opción 2: Ejecución Local (Desarrollo)

#### Requisitos previos
```bash
# Python 3.9+
python3 --version

# MongoDB en ejecución (local o Docker)
# Orion Context Broker en ejecución
```

#### Paso 1: Clonar repositorio
```bash
git clone https://github.com/veroovvila/fiware-smart-store-p2.git
cd fiware-smart-store-p2
```

#### Paso 2: Instalar dependencias Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

pip install -r requirements.txt
```

#### Paso 3: Configurar Backend
```bash
# Crear .env en backend/
cat > .env << EOF
FLASK_ENV=development
FLASK_DEBUG=True
ORION_URL=http://localhost:1026
MONGODB_URL=mongodb://root:root@localhost:27017/
MONGO_DB=fiware_smartstore
EOF
```

#### Paso 4: Ejecutar Backend
```bash
python3 app.py
# Backend disponible en http://localhost:5000
```

#### Paso 5: Servir Frontend (nueva terminal)
```bash
cd frontend

# Opción A: Python built-in server
python3 -m http.server 8000

# Opción B: Node.js live-server
npm install -g live-server
live-server

# Frontend disponible en http://localhost:8000 o http://localhost:8080
```

#### Paso 6: Abrir en navegador
```bash
# Automáticamente se debería abrir en:
# http://localhost:8000 (python) o http://localhost:8080 (live-server)
```

---

## ⚙️ Ejecución

### Con Docker Compose (Recomendado para Producción)

```bash
# Iniciar todos los servicios
docker-compose up -d

# Ver estado de contenedores
docker-compose ps

# Ver logs de un servicio específico
docker-compose logs -f backend
docker-compose logs -f orion
docker-compose logs -f mongodb

# Detener todos los servicios
docker-compose down

# Eliminar volúmenes (resetea datos)
docker-compose down -v
```

### Localmente (Recomendado para Desarrollo)

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python3 app.py
# Servidor en http://localhost:5000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
python3 -m http.server 8000
# Accede en http://localhost:8000
```

**Terminal 3 - Monitorear Logs:**
```bash
# Si usas Docker para Orion/MongoDB
docker-compose logs -f
```

---

## 🔌 API Reference

### Base URL
```
http://localhost:5000/api/v1
```

### Health Check
```http
GET /health
```

Response (200):
```json
{
  "status": "healthy",
  "service": "fiware-smart-store-backend",
  "version": "1.0.0",
  "environment": "development"
}
```

### 🎁 Products

#### Listar todos los productos
```http
GET /products
```

Query Parameters:
- `page` (int, default=1) - Número de página
- `limit` (int, default=20) - Resultados por página
- `search` (string) - Búsqueda por nombre
- `min_price` (float) - Precio mínimo
- `max_price` (float) - Precio máximo

Response (200):
```json
{
  "data": [
    {
      "id": "PRD-001",
      "name": "Laptop Dell XPS 13",
      "price": 899.99,
      "size": "M",
      "color": "#2C3E50",
      "originCountry": "IT"
    }
  ],
  "total": 42,
  "page": 1,
  "pages": 3
}
```

#### Crear producto
```http
POST /products
Content-Type: application/json

{
  "id": "PRD-NEW",
  "name": "Product Name",
  "price": 99.99,
  "size": "M",
  "color": "#FF0000",
  "originCountry": "ES",
  "image": "https://example.com/image.jpg"
}
```

#### Actualizar producto
```http
PATCH /products/{productId}
Content-Type: application/json

{
  "price": 89.99,
  "name": "Updated Name"
}
```

#### Eliminar producto
```http
DELETE /products/{productId}
```

---

### 🏬 Stores

#### Listar tiendas
```http
GET /stores
```

Query Parameters: `page`, `limit`

Response (200):
```json
{
  "data": [
    {
      "id": "STORE-001",
      "name": "Madrid Central",
      "countryCode": "ES",
      "location": {
        "type": "geo:point",
        "value": "40.4168 -3.7038"
      },
      "capacity": 500
    }
  ],
  "total": 7,
  "page": 1
}
```

#### Crear tienda
```http
POST /stores
Content-Type: application/json

{
  "id": "STORE-NEW",
  "name": "Barcelona Nord",
  "countryCode": "ES",
  "location": "41.3851,-2.1734",
  "capacity": 450,
  "description": "Tienda con estacionamiento"
}
```

---

### 👥 Employees

#### Listar empleados
```http
GET /employees
```

Response (200):
```json
{
  "data": [
    {
      "id": "EMP-001",
      "name": "Juan García",
      "email": "juan@store.com",
      "department": "Ventas",
      "position": "Gerente"
    }
  ],
  "total": 6,
  "page": 1
}
```

#### Crear empleado
```http
POST /employees
Content-Type: application/json

{
  "id": "EMP-NEW",
  "name": "María López",
  "email": "maria@store.com",
  "department": "Logística",
  "position": "Coordinadora",
  "salary": 24000,
  "skills": ["Inventario", "Logística"]
}
```

---

### 📦 Inventory

#### Listar inventario
```http
GET /inventory
```

Response (200):
```json
{
  "data": [
    {
      "id": "INV-001",
      "refProduct": "PRD-001",
      "refStore": "STORE-001",
      "refShelf": "SHELF-01",
      "stockCount": 25,
      "shelfCount": 8
    }
  ],
  "total": 120,
  "page": 1
}
```

#### Crear item de inventario
```http
POST /inventory
Content-Type: application/json

{
  "id": "INV-NEW",
  "refProduct": "PRD-001",
  "refStore": "STORE-001",
  "refShelf": "SHELF-01",
  "stockCount": 50,
  "shelfCount": 10
}
```

#### Actualizar stock (Compra)
```http
PATCH /inventory/{inventoryId}
Content-Type: application/json

{
  "stockCount": 24,
  "action": "purchase"
}
```

---

### 🔔 Notificaciones

#### Recibir notificaciones (WebSocket)
```javascript
import io from 'socket.io-client';

const socket = io('http://localhost:5000');

socket.on('notification', (data) => {
  console.log('Nueva notificación:', data);
  // {
  //   type: 'price_change' | 'low_stock',
  //   message: 'Laptop prices updated',
  //   data: { productId, oldPrice, newPrice }
  // }
});
```

---

## 🎨 Interfaz de Usuario

### Vistas Principales

#### 📊 Dashboard
- Estadísticas en tiempo real (# productos, tiendas, empleados)
- Gráfico de distribución de stock
- Últimas notificaciones
- Mapa de tiendas en miniatura

#### 🏪 Productos
- Tabla searcheable de productos
- Filtros por precio y disponibilidad
- Modal de creación/edición
- Vista detallada con inventario por tienda

#### 🗺️ Tiendas
- Mapa interactivo (Leaflet) con markers de tiendas
- Vista 3D del layout (Three.js)
- Información de clima en tiempo real
- Análisis de tweets por zona

#### 📦 Inventario
- Tabla agrupada por tienda y estantería
- Conteo visual de stock
- Operaciones de compra inline
- Alertas de bajo stock destacadas

#### 👥 Empleados
- Directorio de empleados
- Filtros por departamento y tienda
- Gestión de roles y skills

#### 🔔 Notificaciones
- Centro de notificaciones con historial
- Filtros por tipo (precio, stock, etc.)
- Marcado como leído
- Toast notifications push

### Características UX
- **Responsive**: Adaptado a mobile (320px+), tablet y desktop
- **Dark Mode**: Tema oscuro automático según preferencias del sistema
- **i18n**: Interfaz completa en Español e Inglés
- **Accessibility**: ARIA labels, navegación por teclado
- **Real-time**: Actualizaciones instantáneas vía Socket.IO
- **Loading States**: Indicadores de carga durante operaciones

---

## 🗺️ Roadmap

### Fase 1 ✅ (Completado)
- [x] Setup inicial del proyecto (Docker, conexión Orion)
- [x] Modelos de datos NGSIv2
- [x] Importación inicial de datos

### Fase 2 ✅ (Completado)
- [x] Backend con todas las rutas CRUD
- [x] Sistema de validaciones
- [x] Manejo de errores

### Fase 3 ✅ (Completado)
- [x] Suscripciones a cambios de precio
- [x] Suscripciones a bajo stock
- [x] Integración con proveedores externos

### Fase 4 ✅ (Completado)
- [x] WebSocket (Socket.IO) para notificaciones
- [x] Centro de notificaciones
- [x] Validación end-to-end

### 📌 Fase 5 (Próximo)
- [ ] Frontend completo (HTML/CSS/JS)
- [ ] Integración API con backend
- [ ] Mapas interactivos y 3D
- [ ] Testing y validación

### 🚀 Mejoras Futuras
- [ ] **Autenticación JWT**: Sistema de login/logout seguro
- [ ] **Rate Limiting**: Protección contra abuso de API
- [ ] **GraphQL Bridge**: Endpoint GraphQL alternativo
- [ ] **Analytics Dashboard**: Reportes avanzados con gráficos
- [ ] **Mobile App**: Aplicación React Native
- [ ] **Internationalization**: Soporte para más idiomas (FR, DE, IT)
- [ ] **Testing Coverage**: 80%+ code coverage (Jest + PyTest)
- [ ] **CI/CD Pipeline**: GitHub Actions para auto-deployment
- [ ] **Kubernetes**: Orquestación con K8s en lugar de Docker Compose
- [ ] **Cache Layer**: Redis para mejorar performance
- [ ] **Message Queue**: RabbitMQ para procesamiento async
- [ ] **Blockchain**: Inmutabilidad de transacciones de compra
- [ ] **IoT Integration**: Conexión con sensores físicos (temperatura, humedad)

---

## 📚 Documentación Adicional

- [PRD.md](PRD.md) - Product Requirements Document (40+ requisitos funcionales)
- [architecture.md](architecture.md) - Documento de arquitectura en capas
- [data_model.md](data_model.md) - Especificación completa de entidades NGSIv2
- [TESTING_GUIDE.md](TESTING_GUIDE.md) - Guía de testing manual
- [FRONTEND_GUIDE.md](FRONTEND_GUIDE.md) - Guía de desarrollo frontend

---

## 🐛 Troubleshooting

### Backend no se conecta a Orion
```bash
# Verificar que Orion está en ejecución
curl http://localhost:1026/version

# Revisar logs del backend
docker-compose logs backend | grep -i error

# Verificar .env tiene URL correcta
cat backend/.env | grep ORION_URL
```

### Frontend no ve cambios en tiempo real
```bash
# Verificar Socket.IO está conectado
# Abrir Developer Tools (F12) → Console
# Debería haber: "Socket connected: [id]"

# Verificar backend emite eventos
docker-compose logs backend | grep -i socket
```

### MongoDB con problemas de permiso
```bash
# Resetear base de datos
docker-compose down -v
docker-compose up -d
# Esperará a que MongoDB se inicialice
```

### Puerto ya en uso
```bash
# Encontrar qué proceso usa el puerto
lsof -i :5000    # Puerto backend
lsof -i :8081    # Puerto frontend
lsof -i :1026    # Puerto Orion

# Matar proceso (si es necesario)
kill -9 <PID>

# O cambiar puerto en .env
```

---

## 🤝 Contribuyentes

| Rol | Nombre |
|-----|--------|
| **Desarrollador Principal** | Verónica Villa |
| **Consultor FIWARE** | Universidad de Sevilla |
| **Tecnologías** | Flask, React, Orion, MongoDB |

---

## 📝 Licencia

Este proyecto está bajo la licencia **MIT**. Consulta [LICENSE](LICENSE) para más detalles.

---

## 📞 Contacto

- **GitHub**: [@veroovvila](https://github.com/veroovvila)
- **Email**: vill.veroalba@gmail.com
- **Repositorio**: https://github.com/veroovvila/fiware-smart-store-p2

---

## 🙏 Agradecimientos

- **FIWARE Foundation** por el excelente ecosistema
- **Orion Context Broker** team
- **Community** que aporta ideas y feedback

---

<div align="center">

### Made with ❤️ for Smart Cities

*Última actualización: Abril 2026*

</div>
