# 🚀 Sistema de Rutas de Ecuador - Proyecto Final

## 📋 Descripción
Sistema web desarrollado en Flask para gestionar rutas entre ciudades de Ecuador usando algoritmos de grafos (Dijkstra) para encontrar el camino más económico.

## 🎯 Funcionalidades Principales
- **Autenticación de usuarios** con roles (admin/usuario)
- **Búsqueda de rutas óptimas** entre ciudades
- **Panel de administración** completo (CRUD)
- **Visualización de grafos** de rutas
- **Ruta fija** Ibarra → Loja
- **Gestión de provincias, ciudades y rutas**

## 🗄️ Base de Datos
- **MySQL** en puerto 3307 (Laragon)
- **4 tablas**: usuarios, provincias, ciudades, rutas
- **Charset UTF-8** para soporte de acentos
- **6 provincias y ciudades principales de Ecuador**

## ⚡ Instalación y Uso

### 1. Requisitos
- Python 3.8+
- MySQL (Laragon recomendado)
- Dependencias: `pip install -r requirements.txt`

### 2. Configuración
```bash

# Ejecutar aplicación
python app.py
```

### 3. Acceso
- **URL**: http://localhost:4000
- **Admin**: admin / admin
- **Nuevo usuario**: Registrarse en la aplicación

## 🏗️ Arquitectura
- **Backend**: Flask + SQLAlchemy + NetworkX
- **Frontend**: AdminLTE + Bootstrap + jQuery
- **Algoritmo**: Dijkstra para rutas óptimas
- **Patrón**: MVC con principios SOLID

## 📁 Estructura Principal
```
proyecto_final_sql_flask_v2/
├── app.py                 # Aplicación principal
├── forms.py              # Formularios web
├── init_db.py           # Inicialización de BD
├── requirements.txt     # Dependencias
├── models/              # Modelos de base de datos
├── routes/              # Rutas web (blueprints)
├── controllers/         # Lógica de grafos
├── templates/           # Plantillas HTML
├── static/              # CSS, JS, imágenes
└── DOCUMENTACION_COMPLETA.md  # Documentación detallada
```
