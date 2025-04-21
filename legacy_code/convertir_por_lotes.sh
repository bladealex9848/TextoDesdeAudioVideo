#!/bin/bash

# Activar el entorno virtual
source venv/bin/activate

# Número de videos a procesar en cada lote
BATCH_SIZE=5

# Función para mostrar el progreso
mostrar_progreso() {
    ORIGINALES=$(find videos_originales -name "*.mp4" | wc -l)
    CONVERTIDOS=$(find videos_convertidos -name "*_car_compatible.mp4" | wc -l)
    TOTAL=$((ORIGINALES + CONVERTIDOS))
    PORCENTAJE=$((CONVERTIDOS * 100 / TOTAL))

    echo "=== PROGRESO DE CONVERSIÓN ==="
    echo "Videos originales restantes: $ORIGINALES"
    echo "Videos convertidos: $CONVERTIDOS"
    echo "Total de videos: $TOTAL"
    echo "Progreso: $PORCENTAJE%"
    echo "==============================="
}

# Obtener el número total de videos en el directorio de originales
TOTAL_VIDEOS=$(find videos_originales -name "*.mp4" | wc -l)
echo "Total de videos a procesar: $TOTAL_VIDEOS"

# Procesar videos en lotes
while true; do
    # Verificar si quedan videos por procesar
    VIDEOS_RESTANTES=$(find videos_originales -name "*.mp4" | wc -l)
    if [ "$VIDEOS_RESTANTES" -eq 0 ]; then
        echo "No quedan videos por procesar."
        break
    fi

    # Mostrar progreso actual
    mostrar_progreso

    # Procesar el siguiente lote
    echo "Procesando lote de $BATCH_SIZE videos..."
    python convertir_todos_videos.py --max $BATCH_SIZE

    # Ejecutar el script para eliminar los videos originales
    python mover_y_eliminar.py

    # Esperar un momento antes de continuar con el siguiente lote
    echo "Esperando 5 segundos antes de continuar con el siguiente lote..."
    sleep 5
done

# Mostrar progreso final
mostrar_progreso

echo "Proceso completado. Todos los videos han sido convertidos y los originales eliminados."
