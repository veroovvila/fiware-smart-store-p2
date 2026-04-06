# FIWARE Smart Store - P2

**Práctica 2: Sistema inteligente de tienda con FIWARE**

Solución completa para gestión inteligente de inventario en tiendas utilizando la plataforma FIWARE Orion Context Broker, Socket.IO para comunicación real-time, y una arquitectura de microservicios.

## 📋 Descripción

Este proyecto implementa un sistema de inteligencia ambiental (AmI - Ambient Intelligence) para tiendas de retail, permitiendo:

- **Gestión de Inventario**: Monitoreo automático de productos en estanterías
- **Notificaciones en Tiempo Real**: Socket.IO para alertas de bajo stock y cambios de precio
- **Análisis Geoespacial**: Integración de ubicación de tiendas con Leaflet.js
- **Datos Contextuales**: Información climática y tendencias de redes sociales
- **Arquitectura Escalable**: Microservicios con Docker Compose

Para documentación detallada, ver:
- [PRD.md](PRD.md) - Especificación de requisitos
- [architecture.md](architecture.md) - Diseño técnico
- [data_model.md](data_model.md) - Modelo de datos NGSIv2

## ⚙️ Requisitos Previos

- **Docker** & **Docker Compose** (última versión)
- **Python** 3.8+
- **Git**
- Navegador web moderno

## 🚀 Instalación Rápida

### 1. Clonar y configurar el repositorio

```bash
git clone https://github.com/veroovvila/fiware-smart-store-p2.git
cd fiware-smart-store-p2
```

### 2. Configurar variables de entorno

```bash
# Copiar el archivo de plantilla
cp .env.example .env

# Verificar configuración (editar si es necesario)
cat .env
```

**Variables principales en `.env`:**
- `MONGO_ROOT_USER` - Usuario raíz de MongoDB
- `MONGO_ROOT_PASSWORD` - Contraseña de MongoDB
- `MONGO_DB` - Nombre de la base de datos
- `FLASK_PORT` - Puerto del servidor Flask (default: 5000)
- `ORION_PORT` - Puerto de Orion Context Broker (default: 1026)
- `FLASK_ENV` - Modo development/production

### 3. Iniciar los servicios con Docker Compose

```bash
# Iniciar en background
docker-compose up -d

# Verificar estado de los servicios
docker-compose ps

# Ver logs de todos los servicios
docker-compose logs -f

# Para un servicio específico
docker-compose logs -f backend
```

## 📡 Servicios y Puertos

| Servicio | Puerto | URL | Descripción |
|----------|--------|-----|-------------|
| **MongoDB** | 27017 | `mongodb://localhost:27017` | Base de datos NoSQL (conexión interna) |
| **Orion** | 1026 | `http://localhost:1026` | FIWARE Context Broker (NGSIv2) |
| **Flask Backend** | 5000 | `http://localhost:5000` | API REST y Socket.IO |
| **Frontend** | 8080 | `http://localhost:8080` | Interfaz web (Nginx) |

### Verificar conectividad

```bash
# Orion health check
curl -s http://localhost:1026/version | jq .

# Flask health check
curl -s http://localhost:5000/health

# MongoDB connection (desde dentro del contenedor)
docker exec fiware-mongodb mongosh --username $MONGO_ROOT_USER --password $MONGO_ROOT_PASSWORD
```

## 📁 Estructura del Proyecto

```
fiware-smart-store-p2/
├── 📄 README.md                    # Este archivo
├── 📄 PRD.md                        # Especificación de requisitos
├── 📄 architecture.md               # Diseño de la arquitectura
├── 📄 data_model.md                 # Modelo de datos NGSIv2
├── 📄 docker-compose.yml            # Orquestación de contenedores
├── 📄 .env.example                  # Plantilla de variables de entorno
├── 📄 .env                          # Variables locales (gitignored)
├── 📄 .gitignore                    # Archivos a ignorar en git
│
├── 📂 backend/                      # Aplicación Flask
│   ├── __init__.py                  # Package marker
│   ├── app.py                       # Punto de entrada principal
│   ├── config.py                    # Configuración centralizada
│   ├── requirements.txt             # Dependencias Python (20+ packages)
│   │
│   ├── 📂 services/                 # Servicios reutilizables
│   │   ├── __init__.py
│   │   ├── orion_service.py         # Operaciones CRUD con Orion
│   │   ├── subscription_service.py  # Gestión de suscripciones
│   │   ├── provider_service.py      # Proveedores externos (weather, twitter)
│   │   └── notification_service.py  # Notificaciones Socket.IO
│   │
│   ├── 📂 routes/                   # Rutas de la API REST
│   │   └── (API endpoints - Phase 2)
│   │
│   ├── 📂 utils/                    # Funciones auxiliares
│   │   └── (Helpers - Phase 2)
│   │
│   └── 📂 data/                     # Scripts de datos
│       └── (Loaders - Phase 2)
│
├── 📂 frontend/                     # Aplicación web (Nginx)
│   ├── index.html                   # Página principal
│   │
│   ├── 📂 js/                       # JavaScript (Leaflet, Three.js)
│   │   └── (UI modules - Phase 2)
│   │
│   ├── 📂 css/                      # Estilos CSS
│   │   └── (Stylesheets - Phase 2)
│   │
│   └── 📂 templates/                # Plantillas HTML
│       └── (Views - Phase 2)
│
└── 📂 import-data/                  # Datos de inicialización (NGSIv2 JSON)
    ├── products.json                # 10 productos (P001-P010)
    ├── stores.json                  # 4 tiendas (S001-S004)
    ├── employees.json               # 4 empleados (E001-E004)
    ├── shelves.json                 # 16 estanterías (SH001-SH016)
    └── inventory.json               # 80 items de inventario (INV001-INV080)
```

## 🔧 Configuración detallada

### Docker Compose Services

**mongodb:**
- Imagen: `mongo:5.0`
- Puerto: 27017
- Volúmenes: Persistencia de datos
- Salud: TCP health check cada 10s

**orion:**
- Imagen: `fiware/orion:latest`
- Puerto: 1026
- Depende de: MongoDB
- NGSIv2 endpoints disponibles

**backend (Flask):**
- Build: Dockerfile local
- Puerto: 5000
- Dependencias: Mongodb, Orion
- Socket.IO para notificaciones real-time

**frontend (Nginx):**
- Imagen: `nginx:alpine`
- Puerto: 8080
- Expone: Aplicación web estática

### Red Docker

Todos los servicios conectados a la red personalizada `fiware`:
```yaml
networks:
  fiware:
    driver: bridge
```

## 📊 Datos de Inicialización

En la carpeta `import-data/` se incluyen 5 archivos JSON con datos NGSIv2:

- **products.json**: 10 productos variados (café, yogur, pan, tomates, etc.)
- **stores.json**: 4 tiendas en Madrid con geo:point
- **employees.json**: 4 empleados asignados a tiendas
- **shelves.json**: 16 estanterías (4 por tienda)
- **inventory.json**: 80 items de inventario con referencias cruzadas

Formato NGSIv2 estándar con tipos de datos validados.

## 📝 Primeros Pasos

### 1. Verificar que los servicios están running:

```bash
docker-compose ps
# Esperado: all containers STATUS "Up"
```

### 2. Acceder a la aplicación:

- **Frontend**: http://localhost:8080 (interfaz web)
- **API Backend**: http://localhost:5000/api
- **Orion**: http://localhost:1026

### 3. Consultar logs:

```bash
# Todos los servicios
docker-compose logs

# Filtrar por líneas recientes
docker-compose logs --tail=50

# Seguir logs en vivo
docker-compose logs -f backend
```

## 🛑 Detener los servicios

```bash
# Parar contenedores
docker-compose stop

# Parar y eliminar contenedores
docker-compose down

# Eliminar también volúmenes (¡cuidado, borra datos!)
docker-compose down -v
```

## 📚 Fases de Implementación

Este proyecto se implementa en **6 fases**:

1. **Phase 1: Project Setup & Infrastructure** ✅ (completada)
   - Docker Compose configuration
   - Environment setup
   - Folder structure
   - Initial data files

2. **Phase 2-6: Development**
   - Backend API (Flask)
   - Orion integrations
   - Frontend UI
   - Real-time notifications
   - Testing y deployment

Ver [Issue #3](https://github.com/veroovvila/fiware-smart-store-p2/issues/3) para el plan detallado.

## 🔍 Troubleshooting

### Puerto ya en uso:
```bash
# Identificar proceso en puerto 5000
lsof -i :5000

# Matar proceso (si es necesario)
kill -9 <PID>
```

### MongoDB connection error:
```bash
# Verificar credenciales en .env
# Reiniciar servicio
docker-compose restart mongodb
```

### Orion not responding:
```bash
# Verificar que mongodb está up
docker-compose logs mongodb

# Reiniciar Orion
docker-compose restart orion
```

## 📞 Contacto y Soporte

Proyecto: FIWARE Smart Store - Práctica 2  
Repositorio: https://github.com/veroovvila/fiware-smart-store-p2

## 📄 Licencia

XDEI Project - Práctica FIWARE
