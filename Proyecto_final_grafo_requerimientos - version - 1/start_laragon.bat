@echo off
echo ==========================================
echo INICIO RAPIDO - LARAGON
echo Sistema de Rutas con Grafos
echo ==========================================
echo.

echo Verificando Laragon (Puerto 3307)...
mysql -u root --port=3307 -e "SELECT 'Laragon OK en Puerto 3307' as status;" 2>nul

if %errorlevel% neq 0 (
    echo ❌ ERROR: Laragon no esta ejecutandose en puerto 3307
    echo.
    echo SOLUCION:
    echo 1. Abre Laragon
    echo 2. Verifica que MySQL este en puerto 3307
    echo 3. Haz clic en "Start All"
    echo 4. Vuelve a ejecutar este script
    echo.
    pause
    exit /b 1
)

echo ✅ Laragon ejecutandose correctamente (Puerto 3307)
echo.

echo Verificando base de datos...
mysql -u root --port=3307 -D flask_rutas_grafo -e "SELECT COUNT(*) FROM users;" 2>nul

if %errorlevel% neq 0 (
    echo ❌ Base de datos no encontrada
    echo.
    echo Ejecutando instalacion automatica...
    call install_complete.bat
    exit /b %errorlevel%
)

echo ✅ Base de datos OK
echo.

echo Verificando dependencias de Python...
python -c "import flask, networkx, matplotlib" 2>nul

if %errorlevel% neq 0 (
    echo ❌ Dependencias faltantes
    echo Instalando dependencias...
    pip install -r requirements.txt
    
    if %errorlevel% neq 0 (
        echo ERROR: No se pudieron instalar las dependencias
        pause
        exit /b 1
    )
)

echo ✅ Dependencias OK
echo.

echo ==========================================
echo 🚀 INICIANDO APLICACION...
echo ==========================================
echo.
echo La aplicacion se abrira en: http://localhost:4000
echo.
echo CREDENCIALES:
echo Usuario: admin
echo Contraseña: admin123
echo.
echo Para detener presiona Ctrl+C
echo ==========================================
echo.

timeout /t 3 >nul
python app.py
