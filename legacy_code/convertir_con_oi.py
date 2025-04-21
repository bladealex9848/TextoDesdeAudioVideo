#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para convertir videos con Open Interpreter
"""

import os
import sys

def main():
    # Verificar que Open Interpreter esté instalado
    try:
        import open_interpreter
    except ImportError:
        print("Open Interpreter no está instalado. Instalándolo...")
        os.system("pip install open-interpreter")
    
    # Crear directorios si no existen
    if not os.path.exists("videos_originales"):
        os.makedirs("videos_originales")
        print("Directorio 'videos_originales' creado.")
    
    if not os.path.exists("videos_convertidos"):
        os.makedirs("videos_convertidos")
        print("Directorio 'videos_convertidos' creado.")
    
    # Ejecutar Open Interpreter
    comando_oi = """
    Necesito convertir todos los videos en el directorio 'videos_originales' a un formato compatible con reproductores de carro y guardarlos en 'videos_convertidos'. Luego, quiero eliminar los videos originales que ya han sido convertidos exitosamente.

    Sigue estos pasos:
    1. Analiza los videos en 'videos_originales' para identificar cuáles necesitan ser convertidos.
    2. Convierte cada video a formato H.264 con resolución 1080p y 25fps.
    3. Guarda los videos convertidos en 'videos_convertidos' con el sufijo '_car_compatible'.
    4. Verifica que la conversión fue exitosa.
    5. Elimina el video original solo si la conversión fue exitosa.
    6. Proporciona un resumen de los videos procesados.

    Usa ffmpeg para la conversión con estos parámetros:
    - Codec de video: H.264 (libx264)
    - Resolución: 1920x1080
    - Framerate: 25fps
    - Codec de audio: AAC
    - Bitrate de audio: 128k
    """
    
    os.system(f'oi -y -v "{comando_oi}"')

if __name__ == "__main__":
    main()
