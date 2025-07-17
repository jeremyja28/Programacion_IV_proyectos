# Sistema de Gestión de Rutas con Grafos

Un sistema web desarrollado en Flask para la gestión de rutas entre ciudades utilizando algoritmos de grafos. El sistema incluye autenticación de usuarios, roles (administrador/usuario regular) y funcionalidades CRUD para la gestión de ciudades y rutas.

## 🚀 Características

### Para Administradores:
- **Dashboard completo** con estadísticas del sistema
- **Gestión de ciudades**: Crear, editar, eliminar ciudades
- **Gestión de rutas**: Crear, editar, eliminar conexiones entre ciudades
- **Gestión de usuarios**: Administrar roles y permisos
- **Visualización del grafo**: Ver representación gráfica del sistema de rutas

### Para Usuarios Regulares:
- **Búsqueda de rutas óptimas**: Algoritmo de Dijkstra para encontrar el camino más económico
- **Validación de rutas costeras**: Verificación automática de rutas que pasan por ciudades costeras
- **Visualización del grafo**: Solo lectura
- **Interfaz intuitiva**: Fácil navegación y uso

### Funcionalidades Técnicas:
- **Autenticación segura**: Flask-Login con hash de contraseñas
- **Base de datos MySQL**: Almacenamiento persistente
- **Grafos dinámicos**: NetworkX para algoritmos de grafos
- **Interfaz moderna**: Bootstrap + AdminLTE
- **Validación de formularios**: WTForms
- **Visualización**: Matplotlib para generar gráficos

## 📋 Requisitos

- Python 3.8+
- MySQL 5.7+ o MariaDB
- Servidor web (desarrollo: servidor integrado de Flask)

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd Proyecto_final_grafo
```

### 2. Configurar la base de datos
1. Crear una base de datos MySQL:
```sql
CREATE DATABASE flask_practica_1;
```

2. Configurar las credenciales en `.env`:
```env
DB_HOST=localhost
DB_NAME=flask_practica_1
DB_USER=root
DB_PASSWORD=tu_password
DB_PORT=3306
SECRET_KEY=tu-clave-secreta-super-segura
```

### 3. Instalación automática (Windows)
```bash
install.bat
```

### 4. Instalación manual
```bash
# Instalar dependencias
pip install -r requirements.txt

# Inicializar la base de datos
python -c "from app import create_app; from models.models import db; app = create_app(); app.app_context().push(); db.create_all()"

# Cargar datos de ejemplo
python init_data.py

# Ejecutar la aplicación
python app.py
```

## 🎯 Uso del Sistema

### Acceso Inicial
- **URL**: http://localhost:4000
- **Admin**: Usuario: `admin`, Contraseña: `admin123`

### Flujo para Administradores

1. **Iniciar sesión** como administrador
2. **Acceder al Dashboard** desde el menú lateral
3. **Gestionar Ciudades**:
   - Agregar nuevas ciudades
   - Marcar ciudades como costeras
   - Definir coordenadas (opcional)
4. **Gestionar Rutas**:
   - Crear conexiones entre ciudades
   - Definir distancia, costo y tiempo estimado
   - Activar/desactivar rutas
5. **Gestionar Usuarios**:
   - Cambiar roles de usuario
   - Ver estadísticas de usuarios

### Flujo para Usuarios Regulares

1. **Registrarse** o **iniciar sesión**
2. **Buscar rutas**:
   - Seleccionar ciudad de origen
   - Seleccionar ciudad de destino
   - Obtener ruta óptima con validación costera
3. **Visualizar el grafo** (solo lectura)

## 🏗️ Arquitectura del Sistema

### Estructura de Archivos
```
Proyecto_final_grafo/
├── app.py                 # Aplicación principal
├── requirements.txt       # Dependencias
├── install.bat           # Script de instalación
├── init_data.py          # Datos de ejemplo
├── forms.py              # Formularios WTForms
├── .env                  # Configuración
├── models/
│   ├── models.py         # Modelos de base de datos
│   └── config.py         # Configuración de Flask
├── controllers/
│   └── grafo_utils.py    # Lógica de grafos
├── routes/
│   ├── __init__.py       # Registro de blueprints
│   ├── auth_routes.py    # Autenticación
│   ├── admin_routes.py   # Administración
│   ├── home_routes.py    # Páginas principales
│   ├── ruta_fija_routes.py
│   └── rutaeconomica_routes.py
├── templates/
│   ├── base.html         # Plantilla base
│   ├── auth/            # Plantillas de autenticación
│   ├── admin/           # Plantillas de administración
│   └── ...
└── static/              # Archivos estáticos
```

### Modelos de Base de Datos

#### User (Usuarios)
- `id`: Clave primaria
- `username`: Nombre de usuario único
- `email`: Email único
- `password_hash`: Contraseña hasheada
- `role`: 'admin' o 'user'
- `created_at`: Fecha de creación
- `is_active`: Estado del usuario

#### Ciudad
- `id`: Clave primaria
- `nombre`: Nombre único de la ciudad
- `es_costera`: Boolean para ciudades costeras
- `latitud`, `longitud`: Coordenadas opcionales
- `created_at`: Fecha de creación

#### Ruta
- `id`: Clave primaria
- `ciudad_origen_id`, `ciudad_destino_id`: Relaciones con Ciudad
- `distancia`: Distancia en kilómetros
- `costo`: Costo de la ruta
- `tiempo_estimado`: Tiempo en horas
- `estado`: 'activa', 'inactiva', 'mantenimiento'
- `created_by`: Usuario que creó la ruta
- `created_at`, `updated_at`: Fechas de control

### Control de Permisos

#### Decorador `@admin_required`
```python
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Acceso denegado. Se requieren permisos de administrador.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
```

#### Roles y Permisos:
- **Administrador**: Acceso completo a todas las funcionalidades
- **Usuario Regular**: Solo búsqueda y visualización de rutas

### Algoritmos de Grafos

#### Construcción del Grafo
```python
def construir_grafo():
    G = nx.DiGraph()
    rutas = Ruta.query.filter_by(estado='activa').all()
    
    for ruta in rutas:
        G.add_edge(
            ruta.ciudad_origen.nombre, 
            ruta.ciudad_destino.nombre, 
            weight=ruta.costo,
            distancia=ruta.distancia,
            tiempo=ruta.tiempo_estimado or 0
        )
    return G
```

#### Búsqueda de Ruta Óptima
```python
def camino_optimo_con_costera(ciudad_origen_id, ciudad_destino_id):
    G = construir_grafo()
    # Algoritmo de Dijkstra para encontrar el camino más corto
    camino = nx.dijkstra_path(G, origen, destino, weight='weight')
    costo = nx.dijkstra_path_length(G, origen, destino, weight='weight')
    
    # Validación de ciudades costeras
    ciudades_costeras = {c.nombre for c in Ciudad.query.filter_by(es_costera=True).all()}
    contiene_costera = any(ciudad in ciudades_costeras for ciudad in camino)
    
    return {
        "camino": camino,
        "costo": costo,
        "valido": contiene_costera,
        "ciudades_costeras": list(ciudades_costeras.intersection(set(camino)))
    }
```

## 🔧 Configuración Avanzada

### Variables de Entorno
```env
# Flask
FLASK_ENV=development
SECRET_KEY=tu-clave-secreta-cambiar-en-produccion

# Base de datos
DB_HOST=localhost
DB_NAME=flask_practica_1
DB_USER=root
DB_PASSWORD=tu_password
DB_PORT=3306
```

### Personalización

#### Agregar Nuevos Campos a Ciudad
1. Modificar el modelo en `models/models.py`
2. Actualizar el formulario en `forms.py`
3. Agregar campos a las plantillas
4. Ejecutar migración de base de datos

#### Nuevos Algoritmos de Grafos
1. Agregar funciones en `controllers/grafo_utils.py`
2. Crear nuevas rutas en `routes/`
3. Actualizar las plantillas según sea necesario

## 🚀 Despliegue en Producción

### Consideraciones de Seguridad
1. **Cambiar SECRET_KEY** en producción
2. **Usar HTTPS** para todas las comunicaciones
3. **Configurar firewall** de base de datos
4. **Limitar intentos de login**
5. **Backup regular** de la base de datos

### Configuración del Servidor
```bash
# Usar un servidor WSGI como Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Variables de Entorno de Producción
```env
FLASK_ENV=production
SECRET_KEY=clave-super-secura-produccion
DB_HOST=servidor-produccion
DB_PASSWORD=password-seguro
```

## 🧪 Testing

### Ejecutar Tests (cuando se implementen)
```bash
python -m pytest tests/
```

### Datos de Prueba
El script `init_data.py` carga:
- 8 ciudades (3 costeras, 5 interiores)
- 11 rutas interconectadas
- Usuario administrador por defecto

## 📊 Monitoreo y Mantenimiento

### Logs de la Aplicación
- Flask automáticamente registra errores
- Revisar logs para problemas de rendimiento
- Monitorear conexiones de base de datos

### Backup de Base de Datos
```bash
mysqldump -u root -p flask_practica_1 > backup_rutas.sql
```

### Restaurar Base de Datos
```bash
mysql -u root -p flask_practica_1 < backup_rutas.sql
```

## 🤝 Contribución

1. Fork del proyecto
2. Crear branch para nueva funcionalidad
3. Commit de cambios
4. Push al branch
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🙋‍♂️ Soporte

Para soporte técnico:
- **Email**: jeremyjacome0@gmail.com
- **WhatsApp**: +593 99 540 8705
- **GitHub Issues**: Para reportar bugs o solicitar funcionalidades

---

## 🔄 Actualizaciones Futuras

### Funcionalidades Planificadas:
- [ ] API REST para integración externa
- [ ] Exportación de rutas a PDF/Excel
- [ ] Notificaciones en tiempo real
- [ ] Historial de búsquedas por usuario
- [ ] Análisis avanzado de rutas (cuellos de botella, rutas alternativas)
- [ ] Integración con mapas (Google Maps, OpenStreetMap)
- [ ] App móvil con React Native/Flutter

### Mejoras Técnicas:
- [ ] Cache con Redis para consultas frecuentes
- [ ] Tests unitarios e integración
- [ ] Documentación de API con Swagger
- [ ] Containerización con Docker
- [ ] CI/CD con GitHub Actions
