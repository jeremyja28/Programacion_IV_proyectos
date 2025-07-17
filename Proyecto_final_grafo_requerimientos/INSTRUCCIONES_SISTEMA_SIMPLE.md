# Sistema de Rutas Simplificado - Instrucciones de Instalación

## 📋 Cambios Realizados

### ✅ Modelo de Datos Simplificado
- **Provincias**: Solo nombre y código
- **Ciudades**: Solo nombre, provincia y campo costera (booleano)
- **Rutas**: Solo origen, destino y peso/distancia
- **Usuarios**: Tabla básica para administración

### ✅ Funcionalidades Implementadas

#### Dashboard Administrador:
- Gestión completa de provincias (crear, editar, eliminar)
- Gestión completa de ciudades (crear, editar, eliminar)
- Gestión completa de rutas (crear, editar, eliminar)
- Estadísticas del sistema y grafo

#### Dashboard Usuario:
- Visualización del grafo
- Búsqueda de rutas entre ciudades
- Solo lectura (no puede editar)

## 🗄️ Base de Datos

### Nombre de la base de datos: `final_project_PrograIV`
### Puerto: 3307 (Laragon)

### Tablas principales:
1. **provincias** - Información básica de provincias
2. **ciudades** - Ciudades con provincia y si es costera
3. **rutas** - Conexiones entre ciudades con peso
4. **users** - Usuarios del sistema (opcional)

## 🚀 Instalación

### 1. Importar Base de Datos
```bash
# En phpMyAdmin de Laragon (puerto 3307):
# 1. Crear base de datos llamada: final_project_PrograIV
# 2. Importar archivo: sistema_rutas_simple.sql
```

### 2. Configurar Variables de Entorno
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env si es necesario (por defecto está configurado para Laragon)
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Resetear Base de Datos (Opcional)
```bash
python reset_database_simple.py
```

### 5. Ejecutar Aplicación
```bash
python app.py
```

## 🔐 Credenciales por Defecto

**Usuario Administrador:**
- Usuario: `admin`
- Contraseña: `admin123`

## 📊 Datos de Ejemplo

### Provincias Incluidas:
- Pichincha, Guayas, Azuay, Manabí, El Oro, Loja, Imbabura, Tungurahua, Cañar, Chimborazo

### Ciudades Incluidas:
- **Costeras**: Guayaquil, Durán, Manta, Bahía de Caráquez, Machala
- **Interior**: Quito, Sangolquí, Cayambe, Cuenca, Girón, Portoviejo, Pasaje, Loja, Catamayo, Ibarra, Otavalo, Ambato, Baños, Azogues, Riobamba

### Rutas:
- Más de 40 rutas bidireccionales conectando las principales ciudades
- Pesos basados en distancias aproximadas reales

## 🌟 Características Eliminadas

### ❌ Campos Removidos:
- Latitud y longitud de ciudades
- Costo, tiempo estimado y estado en rutas
- Campos como "soles", "tiempos", "estado" en rutas
- Relaciones complejas innecesarias

### ❌ Funcionalidades Removidas:
- Gestión de estados de rutas (activa/inactiva)
- Campos geográficos complejos
- Rutas activas/inactivas (todas las rutas son válidas)

## 🔧 Archivos Principales

- `app.py` - Aplicación principal
- `sistema_rutas_simple.sql` - Base de datos completa
- `reset_database_simple.py` - Script para resetear BD
- `models/models.py` - Modelos simplificados
- `models/config.py` - Configuración actualizada
- `routes/admin_routes.py` - Rutas de administración
- `templates/admin/` - Templates actualizados

## 📝 Notas Importantes

1. **Puerto 3307**: Configurado específicamente para Laragon
2. **Base de Datos**: Nombre fijo `sistema_rutas_simple`
3. **Simplicidad**: Eliminados todos los campos innecesarios
4. **Funcionalidad**: Mantiene las características esenciales del grafo
5. **Administración**: Panel completo para CRUD de provincias, ciudades y rutas

## 🚨 Solución de Problemas

### Error de Conexión BD:
1. Verificar que Laragon esté ejecutándose
2. Confirmar puerto 3307 en MySQL
3. Verificar nombre de base de datos: `final_project_PrograIV`

### Error de Importación:
1. Usar phpMyAdmin en puerto 3307
2. Importar archivo `sistema_rutas_simple.sql`
3. Verificar que todas las tablas se crearon correctamente

### Error de Dependencias:
```bash
pip install flask flask-sqlalchemy flask-login flask-bcrypt pymysql python-dotenv matplotlib networkx
```

## 🎯 Acceso al Sistema

1. **URL**: http://localhost:4000
2. **Login**: Página de inicio
3. **Admin**: Panel completo de administración
4. **Usuario**: Solo visualización y búsqueda

El sistema está ahora completamente simplificado según tus requerimientos!
