@echo off
REM Script para iniciar la API en Windows

echo ====================================
echo Iniciando API Control-M
echo ====================================
echo.

REM Usar entorno virtual si existe
if exist ".venv\Scripts\activate.bat" (
    echo Activando entorno virtual .venv...
    call .venv\Scripts\activate.bat
)

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo Por favor instala Python 3.8 o superior
    pause
    exit /b 1
)

echo Python encontrado!
echo.

REM Verificar si las dependencias están instaladas
echo Verificando dependencias...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias...
    pip install -r requirements.txt
) else (
    echo Dependencias ya instaladas!
)

echo.
echo ====================================
echo API Control-M iniciandose en:
echo http://localhost:5000
echo ====================================
echo.
echo Presiona Ctrl+C para detener la API
echo.

REM Iniciar la API
python api_control_m.py

pause


