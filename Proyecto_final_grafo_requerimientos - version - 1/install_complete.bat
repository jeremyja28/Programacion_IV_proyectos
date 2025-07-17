    @echo off
echo =========================================
echo INSTALACION PARA LARAGON
echo Sistema de Rutas con Grafos
echo =========================================
echo.

echo Este script configurara todo para Laragon
echo Asegurate de que Laragon este ejecutandose
echo.

echo [1/6] Verificando conexion a MySQL en Laragon (Puerto 3307)...
mysql -u root --port=3307 -e "SELECT 'Conexion exitosa a Laragon Puerto 3307' as resultado;" 2>nul

if %errorlevel% neq 0 (
    echo ERROR: No se pudo conectar a MySQL en puerto 3307
    echo.
    echo SOLUCION:
    echo 1. Abre Laragon
    echo 2. Verifica que MySQL este ejecutandose en puerto 3307
    echo 3. Reinicia MySQL en Laragon si es necesario
    echo 4. Vuelve a ejecutar este script
    echo.
    pause
    exit /b 1
)

echo ✅ Conexion a Laragon exitosa (Puerto 3307)
echo.

echo [2/6] Creando base de datos para Laragon (Puerto 3307)...
mysql -u root --port=3307 < laragon_database.sql

if %errorlevel% neq 0 (
    echo ERROR: Fallo al crear la base de datos en puerto 3307
    echo.
    echo POSIBLES SOLUCIONES:
    echo 1. Verifica que Laragon este ejecutandose
    echo 2. Abre phpMyAdmin en http://localhost/phpmyadmin
    echo 3. Importa manualmente el archivo: laragon_database.sql
    echo 4. Reinicia MySQL en Laragon
    echo.
    pause
    exit /b 1
)

echo ✅ Base de datos creada exitosamente
echo.

echo [3/6] Limpiando paquetes conflictivos de Python...
pip uninstall -y numpy matplotlib networkx 2>nul

echo.
echo [4/6] Instalando dependencias de Python...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ERROR: Fallo al instalar las dependencias
    echo.
    echo Intentando instalacion forzada...
    pip install --upgrade pip
    pip install --force-reinstall -r requirements.txt
    
    if %errorlevel% neq 0 (
        echo ERROR: Fallo en la instalacion de Python
        echo Verifica que Python este correctamente instalado
        pause
        exit /b 1
    )
)

echo.
echo [5/6] Verificando conexion de la aplicacion Flask...
python -c "from app import create_app; app = create_app(); print('✅ Aplicacion Flask configurada correctamente')"

if %errorlevel% neq 0 (
    echo ERROR: Fallo al configurar Flask
    echo Revisa los errores de Python arriba
    pause
    exit /b 1
)

echo.
echo [6/6] Verificando datos en Laragon (Puerto 3307)...
mysql -u root --port=3307 -D flask_rutas_grafo -e "SELECT COUNT(*) as total_ciudades FROM ciudades; SELECT COUNT(*) as total_rutas FROM rutas; SELECT COUNT(*) as total_usuarios FROM users;"

echo.
echo ==========================================
echo ✅ INSTALACION COMPLETADA PARA LARAGON!
echo ==========================================
echo.
echo CONFIGURACION:
echo - Base de datos: flask_rutas_grafo
echo - Servidor: Laragon (localhost:3307)
echo - Usuario MySQL: root (sin contraseña)
echo - Apache: Puerto 80
echo - MySQL: Puerto 3307
echo.
echo CREDENCIALES DE LA APLICACION:
echo - Usuario: admin
echo - Contraseña: admin123
echo ==========================================
echo.
echo COMO INICIAR:
echo 1. Asegurate que Laragon este ejecutandose
echo 2. Ejecuta: python app.py
echo 3. Abre: http://localhost:4000
echo.
echo ACCESO A phpMyAdmin: http://localhost/phpmyadmin
echo ==========================================
echo.
pause
