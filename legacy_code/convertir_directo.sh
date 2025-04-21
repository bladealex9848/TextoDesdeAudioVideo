#!/bin/bash

# Activar el entorno virtual
source venv/bin/activate

# Ejecutar el script de conversión
echo "Ejecutando script de conversión..."
python convertir_todos_videos.py

# Verificar el resultado
echo "Verificando resultados..."
echo "Videos en 'videos_originales':"
ls -la videos_originales/
echo ""
echo "Videos en 'videos_convertidos':"
ls -la videos_convertidos/

echo "Proceso completado."
