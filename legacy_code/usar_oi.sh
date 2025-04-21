#!/bin/bash

# Activar el entorno virtual
source venv/bin/activate

# Verificar que Open Interpreter esté instalado
if ! command -v oi &> /dev/null; then
    echo "Instalando Open Interpreter..."
    pip install open-interpreter
fi

# Ejecutar Open Interpreter para mover y eliminar videos
echo "Ejecutando Open Interpreter para mover y eliminar videos..."
oi -y -v "Analiza los directorios 'videos_originales' y 'videos_convertidos'. Para cada video en 'videos_convertidos' que termine con '_car_compatible.mp4', busca el video original correspondiente en 'videos_originales' (sin el sufijo '_car_compatible') y elimínalo. Proporciona un resumen de cuántos videos originales fueron eliminados."
