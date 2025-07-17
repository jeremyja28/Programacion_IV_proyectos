# 🚀 INSTALACIÓN RÁPIDA PARA LARAGON

## ⚡ Inicio Rápido (1 comando)

```bash
# Solo ejecuta esto y listo!
start_laragon.bat
```

## 📋 Requisitos Previos

1. **Laragon instalado** y ejecutándose
2. **Python 3.8+** instalado
3. **MySQL activo** en Laragon

## 🛠️ Instalación Paso a Paso

### 1. Preparar Laragon
```bash
# 1. Abre Laragon
# 2. Haz clic en "Start All"
# 3. Verifica que Apache y MySQL estén en verde
```

### 2. Instalar el Sistema
```bash
# Opción A: Instalación automática completa
install_complete.bat

# Opción B: Solo iniciar (si ya está instalado)
start_laragon.bat
```

### 3. Verificar Instalación
- **Aplicación**: http://localhost:4000
- **phpMyAdmin**: http://localhost/phpmyadmin
- **Base de datos**: `flask_rutas_grafo`

## 🔐 Credenciales

### Aplicación
- **Usuario**: `admin`
- **Contraseña**: `admin123`

### Base de Datos (Laragon)
- **Usuario**: `root`
- **Contraseña**: *(vacía)*
- **Host**: `localhost:3306`
- **Base de datos**: `flask_rutas_grafo`

## 📊 Datos Incluidos

### 8 Ciudades de Ecuador
- **Costeras**: Manta, Portoviejo, Guayaquil
- **Interior**: Ibarra, Quito, Santo Domingo, Cuenca, Loja

### 11 Rutas Interconectadas
- Ibarra → Quito (115km, $10)
- Quito → Santo Domingo (134km, $15)
- Quito → Manta (269km, $30)
- Santo Domingo → Manta (168km, $12)
- Manta → Portoviejo (35km, $5)
- Y más...

## 🚨 Solución de Problemas

### Error: "No se puede conectar a MySQL"
```bash
# 1. Abre Laragon
# 2. Reinicia MySQL (botón rojo → verde)
# 3. Vuelve a ejecutar el script
```

### Error: "Base de datos no encontrada"
```bash
# Ejecuta la instalación completa
install_complete.bat
```

### Error: "Módulo no encontrado"
```bash
# Instala dependencias manualmente
pip install -r requirements.txt
```

### Error: "NumPy incompatible"
```bash
# Ejecuta el script de limpieza
fix_numpy.bat
```

## 📱 Uso del Sistema

### Como Administrador
1. Ir a: http://localhost:4000
2. Login: `admin` / `admin123`
3. Acceder al "Panel Admin" desde el menú
4. Gestionar ciudades y rutas

### Como Usuario Regular
1. Registrarse en la aplicación
2. Buscar rutas óptimas
3. Ver visualización del grafo

## 🔧 Archivos Importantes

- `laragon_database.sql` - SQL para Laragon
- `start_laragon.bat` - Inicio rápido
- `install_complete.bat` - Instalación completa
- `.env` - Configuración (ya configurado para Laragon)

## ✅ Lista de Verificación

- [ ] Laragon ejecutándose (Apache + MySQL en verde)
- [ ] Python instalado y funcionando
- [ ] Ejecutar `start_laragon.bat`
- [ ] Abrir http://localhost:4000
- [ ] Login con admin/admin123
- [ ] ¡Listo para usar!

---

**¿Problemas?** Ejecuta `install_complete.bat` para una instalación completa desde cero.
