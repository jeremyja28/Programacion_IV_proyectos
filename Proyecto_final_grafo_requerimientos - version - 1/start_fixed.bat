@echo off
echo =========================================
echo        PROYECTO FINAL - SISTEMA DE RUTAS
echo =========================================
echo.

echo Verificando el entorno virtual...
if exist ".venv" (
    echo [OK] Entorno virtual encontrado
) else (
    echo [ERROR] No se encontró el entorno virtual
    echo Creando entorno virtual...
    python -m venv .venv
    echo [OK] Entorno virtual creado
)

echo.
echo Activando entorno virtual...
call .venv\Scripts\activate

echo.
echo Verificando dependencias...
pip install -r requirements.txt --quiet

echo.
echo Verificando variables de entorno...
if exist ".env" (
    echo [OK] Archivo .env encontrado
) else (
    echo [ADVERTENCIA] No se encontró archivo .env
    echo Creando archivo .env con configuración por defecto...
    (
        echo FLASK_APP=app.py
        echo FLASK_ENV=development
        echo SECRET_KEY=tu_clave_secreta_aqui
        echo DATABASE_URL=mysql+pymysql://root:@localhost:3307/proyecto_rutas
        echo MYSQL_HOST=localhost
        echo MYSQL_PORT=3307
        echo MYSQL_USER=root
        echo MYSQL_PASSWORD=
        echo MYSQL_DATABASE=proyecto_rutas
    ) > .env
    echo [OK] Archivo .env creado
)

echo.
echo Verificando estado de la base de datos...
echo =========================================
echo Si es la primera vez que ejecutas la aplicación
echo o si hay problemas con la base de datos,
echo ejecuta: python reset_database.py
echo =========================================
echo.

echo Iniciando la aplicación...
echo.
echo =========================================
echo Aplicación ejecutándose en: http://localhost:4000
echo Usuario administrador: admin / admin123
echo.
echo NOTAS IMPORTANTES:
echo - La aplicación inicia siempre en el login
echo - Solo el admin puede modificar rutas/ciudades
echo - En la esquina superior derecha aparece el usuario
echo - Haz clic en el nombre para cerrar sesión
echo.
echo Presiona Ctrl+C para detener la aplicación
echo =========================================
echo.

python app.py
