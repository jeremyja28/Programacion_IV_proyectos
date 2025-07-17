# 🚀 INSTALACIÓN PARA LARAGON - PUERTO 3307

## ⚙️ Tu Configuración Actual
- **Apache**: Puerto 80 ✅
- **MySQL**: Puerto 3307 ✅  
- **phpMyAdmin**: http://localhost/phpmyadmin

## 🎯 Instalación Rápida

### Opción 1: Script Automático (Recomendado)
```bash
# Ejecutar en la carpeta del proyecto
install_complete.bat
```

### Opción 2: Importar Manual en phpMyAdmin
1. Abre: http://localhost/phpmyadmin
2. Crear nueva base de datos: `flask_rutas_grafo`
3. Seleccionar la base de datos
4. Ir a "Importar" 
5. Subir archivo: `import_phpmyadmin.sql`
6. Hacer clic en "Continuar"

## 📁 Archivos SQL Disponibles

### `laragon_database.sql` - Para línea de comandos
```bash
mysql -u root --port=3307 < laragon_database.sql
```

### `import_phpmyadmin.sql` - Para phpMyAdmin
- Optimizado para importar desde la interfaz web
- Incluye DROP TABLE para limpiar datos anteriores
- Verificaciones automáticas

## 🔧 Configuración Actualizada

### `.env` - Ya configurado para puerto 3307
```env
DB_HOST=localhost
DB_NAME=flask_rutas_grafo
DB_USER=root
DB_PASSWORD=
DB_PORT=3307
```

### Scripts actualizados
- `install_complete.bat` - Usa puerto 3307
- `start_laragon.bat` - Verificaciones para puerto 3307

## 🚀 Iniciar el Proyecto

### Paso 1: Verificar Laragon
```
✅ Apache httpd-2.4.54-win64-VS16 started (Puerto 80)
✅ MySQL mysql-8.0.30-winx64 started (Puerto 3307)
```

### Paso 2: Ejecutar instalación
```bash
install_complete.bat
```

### Paso 3: Iniciar aplicación
```bash
# Opción A: Inicio automático
start_laragon.bat

# Opción B: Manual
python app.py
```

### Paso 4: Acceder
- **Aplicación**: http://localhost:4000
- **Login**: admin / admin123

## 🔍 Verificación Manual

### Conectar a MySQL
```bash
mysql -u root --port=3307
```

### Verificar base de datos
```sql
USE flask_rutas_grafo;
SELECT COUNT(*) FROM ciudades; -- Debe mostrar 8
SELECT COUNT(*) FROM rutas;    -- Debe mostrar 11
SELECT COUNT(*) FROM users;    -- Debe mostrar 1
```

## 🚨 Solución de Problemas

### Error: "No se puede conectar al puerto 3307"
1. Verificar que Laragon esté ejecutándose
2. Reiniciar MySQL en Laragon
3. Verificar que el puerto sea 3307 en Laragon

### Error: "Base de datos no existe"
1. Usar phpMyAdmin: http://localhost/phpmyadmin
2. Crear base de datos: `flask_rutas_grafo`
3. Importar: `import_phpmyadmin.sql`

### Error: "Dependencias de Python"
```bash
fix_numpy.bat
pip install -r requirements.txt
```

## ✅ Lista de Verificación Final

- [ ] Laragon ejecutándose (Apache Puerto 80 + MySQL Puerto 3307)
- [ ] Base de datos `flask_rutas_grafo` creada
- [ ] Tablas importadas (users, ciudades, rutas)
- [ ] Dependencias Python instaladas
- [ ] Aplicación iniciada: `python app.py`
- [ ] Acceso: http://localhost:4000
- [ ] Login: admin / admin123

---

**🎯 Todo está configurado específicamente para tu Laragon con Puerto 3307!**
