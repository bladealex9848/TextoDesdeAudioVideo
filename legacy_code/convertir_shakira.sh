#!/bin/bash

# Activar el entorno virtual
source venv/bin/activate

# Definir archivos
VIDEO_ORIGINAL="videos_originales/Shakira - Soltera (Official Video) (2160p_30fps_AV1-128kbit_AAC).mp4"
VIDEO_CONVERTIDO="videos_convertidos/Shakira - Soltera (Official Video) (2160p_30fps_AV1-128kbit_AAC)_car_compatible.mp4"

# Verificar que el archivo original existe
if [ ! -f "$VIDEO_ORIGINAL" ]; then
    echo "Error: El archivo original no existe: $VIDEO_ORIGINAL"
    exit 1
fi

# Convertir el video
echo "Convirtiendo video de Shakira a formato compatible con reproductores de carro..."
ffmpeg -i "$VIDEO_ORIGINAL" -c:v libx264 -profile:v high -level:v 4.0 -preset medium -crf 23 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" -r 25 -c:a aac -b:a 128k "$VIDEO_CONVERTIDO"

# Verificar si la conversión fue exitosa
if [ $? -eq 0 ]; then
    echo "Conversión exitosa. Eliminando archivo original..."
    rm "$VIDEO_ORIGINAL"
    echo "Archivo original eliminado."
    echo "Video convertido guardado en: $VIDEO_CONVERTIDO"
else
    echo "Error en la conversión. El archivo original no ha sido eliminado."
fi
