# Sistema de Grafos - Versión Simplificada

Un sistema web desarrollado en Flask para la gestión y visualización de grafos de rutas entre ciudades, utilizando el algoritmo de Dijkstra para encontrar rutas óptimas.

## Características Principales

### 🗺️ Gestión de Grafos
- **Provincias**: Crear y gestionar provincias argentinas
- **Ciudades**: Agregar ciudades a provincias, clasificar como costeras o interiores
- **Rutas**: Definir rutas entre ciudades con pesos/distancias
- **Visualización**: Visualizar el grafo completo de forma interactiva

### 🚀 Algoritmos Implementados
- **Algoritmo de Dijkstra**: Para encontrar rutas óptimas entre ciudades
- **Detección de rutas costeras**: Identificar rutas que pasan por ciudades costeras
- **Cálculo de distancias**: Obtener distancias totales de rutas

### 👥 Sistema de Usuarios
- **Administradores**: Gestión completa del sistema
- **Usuarios**: Solo visualización de grafos

## Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **Base de Datos**: MySQL
- **ORM**: SQLAlchemy
- **Grafos**: NetworkX
- **Frontend**: AdminLTE 3, Bootstrap 4
- **Autenticación**: Flask-Login
- **Visualización**: Chart.js, D3.js

## Estructura del Proyecto

```
Final_project_flask_MYSQL/
├── app.py                      # Aplicación principal
├── config.py                   # Configuración
├── extensions.py               # Extensiones Flask
├── grafo_utils.py             # Utilidades para grafos
├── requirements.txt           # Dependencias Python
├── database_setup_simplified.sql # Base de datos simplificada
├── controllers/               # Controladores
│   ├── auth_controller.py
│   ├── grafo_controller.py
│   └── user_controller.py
├── models/                    # Modelos de datos
│   ├── usuario.py
│   ├── provincia.py
│   ├── ciudad.py
│   └── ruta.py
├── routes/                    # Rutas Flask
│   ├── auth_routes.py
│   ├── grafo_routes.py
│   ├── home_routes.py
│   └── user_routes.py
├── templates/                 # Templates HTML
│   ├── base.html
│   ├── home.html
│   ├── auth/
│   └── grafo/
└── static/                   # Archivos estáticos
    ├── css/
    ├── js/
    └── img/
```

## Instalación y Configuración

### 1. Requisitos Previos
- Python 3.8+
- MySQL 8.0+
- Laragon (o servidor web con MySQL)

### 2. Configuración del Entorno

```bash
# Clonar el proyecto
git clone [url-del-repositorio]
cd Final_project_flask_MYSQL

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configuración de la Base de Datos

1. Iniciar Laragon y MySQL
2. Crear la base de datos:
```sql
mysql -u root -p < database_setup_simplified.sql
```

3. Configurar credenciales en `config.py`:
```python
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3307
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''
MYSQL_DB = 'sistema_grafos'
```

### 4. Ejecutar la Aplicación

```bash
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

## Uso del Sistema

### 1. Inicio de Sesión
- **Usuario por defecto**: `admin`
- **Contraseña**: `admin123`

### 2. Gestión de Grafos
1. **Crear Provincias**: Agregar nuevas provincias
2. **Agregar Ciudades**: Crear ciudades y asignar a provincias
3. **Definir Rutas**: Conectar ciudades con pesos/distancias
4. **Visualizar**: Ver el grafo completo

### 3. Búsqueda de Rutas
- Seleccionar ciudad origen y destino
- Obtener ruta óptima usando Dijkstra
- Visualizar el camino encontrado

## Características Técnicas

### Base de Datos
- **usuarios**: Gestión de usuarios y administradores
- **provincias**: Información de provincias
- **ciudades**: Ciudades con clasificación costera/interior
- **rutas**: Conexiones entre ciudades con pesos

### Algoritmos
- **Dijkstra**: Implementado con NetworkX para rutas óptimas
- **Grafos dirigidos**: Soporte para rutas bidireccionales
- **Visualización**: Representación gráfica del grafo

### Seguridad
- Autenticación con Flask-Login
- Hasheo de contraseñas con Werkzeug
- Validación de formularios
- Protección CSRF

## Contribución

1. Fork el proyecto
2. Crear rama para nueva funcionalidad
3. Hacer commit de los cambios
4. Push a la rama
5. Crear Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

## Contacto

Para dudas o sugerencias, crear un issue en el repositorio.

---

**Sistema de Grafos** - Gestión inteligente de rutas entre ciudades
