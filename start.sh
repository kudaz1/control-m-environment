#!/bin/bash

# Script para iniciar la API en Linux/Mac

echo "===================================="
echo "Iniciando API Control-M"
echo "===================================="
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 no está instalado"
    echo "Por favor instala Python 3.8 o superior"
    exit 1
fi

echo "Python encontrado!"
echo ""

# Verificar si las dependencias están instaladas
echo "Verificando dependencias..."
if ! python3 -c "import flask" &> /dev/null; then
    echo "Instalando dependencias..."
    pip3 install -r requirements.txt
else
    echo "Dependencias ya instaladas!"
fi

echo ""
echo "===================================="
echo "API Control-M iniciándose en:"
echo "http://localhost:5000"
echo "===================================="
echo ""
echo "Presiona Ctrl+C para detener la API"
echo ""

# Iniciar la API
python3 api_control_m.py


