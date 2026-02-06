@echo off
REM Ejecutar tests de la API (la API debe estar corriendo en http://localhost:5000)

echo ====================================
echo Tests API Control-M
echo ====================================
echo.

if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

echo Asegurate de tener la API corriendo (start.bat) en otra ventana.
echo.
python test_api.py
echo.
pause
