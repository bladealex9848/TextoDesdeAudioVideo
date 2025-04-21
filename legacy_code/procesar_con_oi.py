#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para procesar videos con Open Interpreter
"""

import os
import sys
import subprocess

def main():
    # Verificar que Open Interpreter esté instalado
    try:
        subprocess.check_call(["which", "oi"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("Open Interpreter no está instalado. Instalándolo...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "open-interpreter"])
    
    # Crear directorios si no existen
    if not os.path.exists("videos_originales"):
        os.makedirs("videos_originales")
        print("Directorio 'videos_originales' creado.")
    
    if not os.path.exists("videos_convertidos"):
        os.makedirs("videos_convertidos")
        print("Directorio 'videos_convertidos' creado.")
    
    # Ejecutar Open Interpreter para convertir videos
    print("Ejecutando Open Interpreter para convertir videos...")
    comando_oi = """
    Analiza los videos en el directorio 'videos_originales' y conviértelos a formato compatible con reproductores de carro siguiendo estos pasos:
    
    1. Para cada video en 'videos_originales':
       a. Analiza sus características (codec, resolución, framerate)
       b. Si no es compatible con reproductores de carro (debe ser H.264, 1080p, 25fps), conviértelo
       c. Guarda el video convertido en 'videos_convertidos' con el sufijo '_car_compatible'
       d. Elimina el video original
    
    2. Usa ffmpeg con estos parámetros para la conversión:
       - Codec de video: H.264 (libx264)
       - Resolución: 1920x1080
       - Framerate: 25fps
       - Codec de audio: AAC
       - Bitrate de audio: 128k
    
    3. Proporciona un resumen de los videos procesados
    """
    
    subprocess.call(["oi", "-y", "-v", comando_oi])

if __name__ == "__main__":
    main()
