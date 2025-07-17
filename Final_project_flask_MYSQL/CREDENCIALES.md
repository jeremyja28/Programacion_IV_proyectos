# 🎯 CREDENCIALES FINALES - Sistema de Rutas

## 🔐 ACCESO AL SISTEMA

### **ADMINISTRADOR**
- **Usuario**: `admin`
- **Contraseña**: `admin123`
- **Permisos**: Acceso completo a todas las funcionalidades

### **USUARIO NORMAL**
- **Usuario**: `usuario`
- **Contraseña**: `admin123`
- **Permisos**: Acceso a funcionalidades básicas

## 🚀 CÓMO USAR

### 1. Iniciar el Sistema
```bash
# Asegúrate de estar en el directorio del proyecto
cd Final_project_flask_MYSQL

# Ejecutar la aplicación
python app.py
```

### 2. Acceder al Sistema
- **URL**: http://localhost:5000
- **Login**: Usar cualquiera de las credenciales de arriba
- **Interfaz**: Las credenciales aparecen en la pantalla de login

### 3. Funcionalidades Disponibles
- ✅ **Crear Provincias**: Formulario simple
- ✅ **Agregar Ciudades**: Seleccionar provincia + ¿Es costera?
- ✅ **Registrar Rutas**: Solo peso/distancia
- ✅ **Algoritmo de Dijkstra**: Ruta más corta
- ✅ **Detección Costera**: Indica si pasa por ciudad costera
- ✅ **Gestión de Notas**: CRUD básico
- ✅ **Visualización de Grafo**: Con matplotlib

## 🔧 CONFIGURACIÓN

### Base de Datos (Laragon)
```env
DB_HOST=localhost
DB_PORT=3307
DB_NAME=Final_project_flask_mysql
DB_USER=root
DB_PASSWORD=
```

### Verificación
```bash
# Probar conexión a BD
python test_connection.py

# Probar credenciales
python test_credentials.py
```

## 📋 PROCESO DE TRABAJO

1. **Login** con `admin` / `admin123`
2. **Crear Provincias**: "Pichincha", "Guayas", etc.
3. **Agregar Ciudades**: 
   - Provincia: "Pichincha" → Ciudad: "Quito" → Costera: "No"
   - Provincia: "Guayas" → Ciudad: "Guayaquil" → Costera: "Sí"
4. **Registrar Rutas**: Quito → Guayaquil con peso 450
5. **Buscar Ruta Óptima**: Algoritmo de Dijkstra
6. **Resultado**: Camino + distancia + si pasa por costera

## 🎯 CARACTERÍSTICAS

- **Simple y Funcional**: Sin complejidades innecesarias
- **Credenciales Fijas**: No hay registro de usuarios
- **Algoritmo de Dijkstra**: Implementado correctamente
- **Detección Costera**: Automática en las rutas
- **Interfaz Clara**: AdminLTE con credenciales visibles

## ⚠️ IMPORTANTE

- Las credenciales están **hardcodeadas** en el sistema
- No hay opción de registro de nuevos usuarios
- Solo existen 2 usuarios: `admin` y `usuario`
- Ambos usan la misma contraseña: `admin123`

**¡Sistema listo para usar!** 🎉

---
*Credenciales siempre visibles en la pantalla de login*
*Sistema básico pero completamente funcional*
