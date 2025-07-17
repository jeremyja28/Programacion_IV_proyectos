@echo off
echo ================================
echo INSTALACION DEL SISTEMA DE RUTAS
echo ================================
echo.

echo [1/6] Desinstalando paquetes conflictivos...
pip uninstall -y numpy matplotlib networkx 2>nul

echo.
echo [2/6] Instalando dependencias de Python...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ERROR: Fallo al instalar las dependencias
    echo.
    echo Intentando con metodo alternativo...
    pip install --upgrade pip
    pip install --force-reinstall -r requirements.txt
    
    if %errorlevel% neq 0 (
        echo ERROR: Fallo en ambos metodos de instalacion
        pause
        exit /b 1
    )
)

echo.
echo [3/6] Verificando conexion a la base de datos...
python -c "from app import create_app; app = create_app(); print('✅ Conexion a la base de datos exitosa')"

if %errorlevel% neq 0 (
    echo ERROR: No se pudo conectar a la base de datos
    echo Verifica que MySQL este ejecutandose y que las credenciales en .env sean correctas
    pause
    exit /b 1
)

echo.
echo [4/6] Creando tablas de la base de datos...
python -c "from app import create_app; from models.models import db; app = create_app(); app.app_context().push(); db.create_all(); print('✅ Tablas creadas exitosamente')"

echo.
echo [5/6] Inicializando datos de ejemplo...
python init_data.py

echo.
echo [6/6] Instalacion completada!
echo.
echo ================================
echo CREDENCIALES DE ADMINISTRADOR:
echo Usuario: admin
echo Contraseña: admin123
echo ================================
echo.
echo Para iniciar la aplicacion ejecuta: python app.py
echo La aplicacion estara disponible en: http://localhost:4000
echo.
pause
