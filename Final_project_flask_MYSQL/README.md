# 🚀 Sistema de Rutas - Flask + MySQL (Básico)

Un sistema básico de gestión de rutas implementado con Flask y MySQL, utilizando el algoritmo de Dijkstra para encontrar rutas óptimas.

## 🎯 Características Principales

### 🔐 Sistema de Autenticación
- Login y logout básico
- Usuario administrador por defecto

### 📝 Gestión de Notas
- Crear, leer, actualizar y eliminar notas
- Notas personales por usuario

### 🗺️ Gestión de Grafos (Básico)
- **Provincias**: Crear provincias
- **Ciudades**: Agregar ciudades (pregunta si es costera)
- **Rutas**: Registrar rutas solo con peso/distancia
- **Algoritmo de Dijkstra**: Ruta más corta entre ciudades
- **Detección de Rutas Costeras**: Indica si la ruta pasa por ciudad costera

## 🛠️ Tecnologías Utilizadas

- **Flask**: Framework web
- **MySQL**: Base de datos
- **NetworkX**: Algoritmos de grafos
- **Matplotlib**: Visualización
- **AdminLTE**: Interfaz de usuario

## 📂 Estructura del Proyecto

```
Final_project_flask_MYSQL/
├── app.py                 # Archivo principal
├── config.py             # Configuración
├── extensions.py         # Extensiones de Flask
├── requirements.txt      # Dependencias
├── database_setup.sql    # Script de BD
├── .env.template        # Template de variables
├── .gitignore           # Archivos a ignorar
├── controllers/         # Controladores (Lógica de negocio)
│   ├── auth_controller.py
│   ├── grafo_controller.py
│   ├── nota_controller.py
│   └── user_controller.py
├── models/              # Modelos (ORM)
│   ├── ciudad.py
│   ├── nota.py
│   ├── provincia.py
│   ├── ruta.py
│   └── usuario.py
├── routes/              # Rutas (Endpoints)
│   ├── auth_routes.py
│   ├── grafo_routes.py
│   ├── home_routes.py
│   ├── nota_routes.py
│   └── user_routes.py
├── templates/           # Templates HTML
│   ├── base.html
│   ├── home.html
│   ├── formulario.html
│   ├── ruta_fija.html
│   ├── auth/
│   │   ├── login.html
│   │   └── login_fixed.html
│   └── grafo/
│       └── visualizar.html
├── static/              # Archivos estáticos
│   ├── css/
│   ├── js/
│   ├── img/
│   └── adminlte/
└── utils/               # Utilidades
    └── __init__.py
```
└── static/                  # CSS, JS, imágenes
```

## 🚀 Instalación

### 1. Preparar Entorno
```bash
pip install -r requirements.txt
```

### 2. Configurar Base de Datos
```sql
# En phpMyAdmin o MySQL:
# 1. Crear base de datos: Final_project_flask_mysql
# 2. Importar: database_setup.sql
```

### 3. Configurar Variables
```bash
# Editar .env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=Final_project_flask_mysql
DB_USER=root
DB_PASSWORD=tu_password
```

### 4. Ejecutar
```bash
python app.py
```

## 🎮 Uso del Sistema

### 1. Acceder
- URL: http://localhost:5000
- Usuario: admin
- Contraseña: admin123

### 2. Crear Provincias
- Ir a "Gestión de Grafos" > "Provincias"
- Crear nueva provincia (ej: "Pichincha")

### 3. Agregar Ciudades
- Ir a "Gestión de Grafos" > "Ciudades"
- Seleccionar provincia
- Nombre de ciudad
- ¿Es costera? (Sí/No)

### 4. Registrar Rutas
- Ir a "Gestión de Grafos" > "Rutas"
- Seleccionar ciudad origen
- Seleccionar ciudad destino
- Ingresar peso/distancia

### 5. Encontrar Ruta Óptima
- Ir a "Gestión de Grafos" > "Ruta Óptima"
- Seleccionar origen y destino
- Ver resultado del algoritmo de Dijkstra
- El sistema mostrará:
  - Camino óptimo
  - Distancia total (suma de aristas)
  - Si pasa por ciudad costera

## 🧮 Algoritmo de Dijkstra

El sistema implementa el algoritmo de Dijkstra para encontrar la ruta más corta:

```python
def dijkstra_ruta_optima(origen_id, destino_id):
    # Crear grafo desde base de datos
    G = crear_grafo()
    
    # Encontrar camino más corto
    camino = nx.shortest_path(G, origen_id, destino_id, weight='weight')
    distancia = nx.shortest_path_length(G, origen_id, destino_id, weight='weight')
    
    # Verificar si pasa por ciudad costera
    pasa_por_costera = any(ciudad.es_costera for ciudad in camino)
    
    return camino, distancia, pasa_por_costera
```

## 📊 Base de Datos (Simplificada)

### Tablas Principales:
- **usuarios**: Gestión de usuarios
- **notas**: Notas personales
- **provincias**: Provincias (solo nombre)
- **ciudades**: Ciudades (nombre, es_costera, provincia_id)
- **rutas**: Rutas (peso, ciudad_origen_id, ciudad_destino_id)

### Características:
- Sin campos de tiempo o duración
- Solo peso/distancia en rutas
- Estructura clara y funcional

## 🎨 Interfaz de Usuario

- **Dashboard**: Estadísticas básicas
- **Formularios**: Simples y directos
- **Visualización**: Grafo con NetworkX/Matplotlib
- **Colores**: Azul para costeras, verde para interiores

## 📝 Credenciales de Acceso

### 🔐 ADMINISTRADOR
- **Usuario**: `admin`
- **Contraseña**: `admin123`
- **Acceso**: Todas las funcionalidades

### 👤 USUARIO NORMAL
- **Usuario**: `usuario`
- **Contraseña**: `admin123`
- **Acceso**: Funcionalidades básicas

### 🚀 Para Acceder:
1. Ejecutar: `python app.py`
2. Abrir: http://localhost:5000
3. Usar cualquiera de las credenciales de arriba

## 🔧 Características del Sistema

### ✅ Funcionalidades Básicas:
- [x] Crear provincias
- [x] Agregar ciudades (costera/interior)
- [x] Registrar rutas (solo peso)
- [x] Algoritmo de Dijkstra
- [x] Detección de rutas costeras
- [x] Visualización de grafo
- [x] CRUD de notas
- [x] Autenticación básica

### 🎯 Proceso de Trabajo:
1. Crear provincias
2. Agregar ciudades (pregunta si es costera)
3. Registrar rutas con peso/distancia
4. Usar Dijkstra para encontrar ruta óptima
5. Mostrar si pasa por ciudad costera

**¡Sistema básico y funcional!** 🎉

---
*Desarrollado para Programación IV - Cuarto Semestre*
*Sistema simplificado con funcionalidades esenciales*
