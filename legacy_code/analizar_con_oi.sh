#!/bin/bash

# Activar el entorno virtual
source venv/bin/activate

# Verificar que Open Interpreter esté instalado
if ! command -v oi &> /dev/null; then
    echo "Instalando Open Interpreter..."
    pip install open-interpreter
fi

# Ejecutar el script de análisis
echo "Ejecutando script de análisis de videos..."
python analizar_videos_con_oi.py

# Analizar los informes con Open Interpreter
echo "Analizando informes con Open Interpreter..."
oi -y -v "Analiza los archivos 'informe_videos_originales.json' y 'informe_videos_convertidos.json'. Identifica las diferencias clave entre los videos originales y convertidos, especialmente en términos de codec, resolución, framerate y tamaño. Explica por qué algunos videos son compatibles con reproductores de carro y otros no. Proporciona recomendaciones para optimizar la conversión de videos."

echo "Proceso completado."
