@echo off
echo =========================================
echo LIMPIEZA E INSTALACION DESDE CERO
echo =========================================
echo.
echo Este script resolvera los conflictos de NumPy/Matplotlib
echo.

echo [1/3] Desinstalando todos los paquetes problematicos...
pip uninstall -y numpy matplotlib networkx scipy pandas pillow 

echo.
echo [2/3] Limpiando cache de pip...
pip cache purge

echo.
echo [3/3] Instalando desde cero con versiones compatibles...
pip install --no-cache-dir numpy==1.24.4
pip install --no-cache-dir matplotlib==3.8.4
pip install --no-cache-dir networkx==3.1

echo.
echo Ahora instalando el resto de dependencias...
pip install --no-cache-dir flask==2.3.3
pip install --no-cache-dir flask-sqlalchemy==3.1.1
pip install --no-cache-dir flask-login==0.6.3
pip install --no-cache-dir flask-bcrypt==1.0.1
pip install --no-cache-dir flask-wtf==1.1.1
pip install --no-cache-dir wtforms==3.0.1
pip install --no-cache-dir pymysql==1.1.0
pip install --no-cache-dir python-dotenv==1.0.0

echo.
echo =========================================
echo LIMPIEZA COMPLETADA
echo =========================================
echo.
echo Ahora ejecuta: install.bat
echo.
pause
