#!/bin/bash

# Activar el entorno virtual
source venv/bin/activate

# Verificar que Open Interpreter esté instalado
if ! command -v oi &> /dev/null; then
    echo "Instalando Open Interpreter..."
    pip install open-interpreter
fi

# Ejecutar el script de conversión con Open Interpreter
echo "Ejecutando script de conversión con Open Interpreter..."
oi -y -v "Analiza y ejecuta el script 'convertir_todos_videos.py' que convierte videos de 'videos_originales' a formato compatible con reproductores de carro, los guarda en 'videos_convertidos' y elimina los originales. Proporciona un análisis detallado de cada paso y muestra estadísticas sobre los videos procesados. Si hay algún error, sugiere soluciones."

# Verificar el resultado
echo "Verificando resultados..."
echo "Videos en 'videos_originales':"
ls -la videos_originales/
echo ""
echo "Videos en 'videos_convertidos':"
ls -la videos_convertidos/

echo "Proceso completado."
