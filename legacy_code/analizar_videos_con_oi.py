#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para analizar videos con Open Interpreter y proporcionar recomendaciones
"""

import os
import subprocess
import json
from pathlib import Path

def obtener_info_video(video_path):
    """Obtiene información detallada del video usando ffprobe."""
    try:
        cmd = f'ffprobe -v quiet -print_format json -show_format -show_streams "{video_path}"'
        result = subprocess.check_output(cmd, shell=True).decode('utf-8')
        return json.loads(result)
    except Exception as e:
        print(f"Error al obtener información del video {video_path}: {str(e)}")
        return None

def analizar_directorio(directorio):
    """Analiza todos los videos en un directorio y genera un informe."""
    if not os.path.exists(directorio):
        print(f"El directorio {directorio} no existe.")
        return []
    
    # Obtener lista de videos
    extensiones_video = ['.mp4', '.mkv', '.avi', '.mov', '.webm', '.flv', '.wmv', '.3gp']
    videos = []
    
    for ext in extensiones_video:
        videos.extend(list(Path(directorio).glob(f'*{ext}')))
    
    if not videos:
        print(f"No se encontraron videos en {directorio}.")
        return []
    
    print(f"Analizando {len(videos)} videos en {directorio}...")
    
    resultados = []
    for video_path in videos:
        video_path_str = str(video_path)
        print(f"Analizando: {video_path.name}")
        
        info = obtener_info_video(video_path_str)
        if info:
            video_info = {
                'nombre': video_path.name,
                'ruta': video_path_str,
                'info': info
            }
            resultados.append(video_info)
    
    return resultados

def guardar_informe(resultados, archivo_salida):
    """Guarda los resultados del análisis en un archivo JSON."""
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    print(f"Informe guardado en {archivo_salida}")

def main():
    # Analizar videos originales
    print("=== Analizando videos originales ===")
    resultados_originales = analizar_directorio('videos_originales')
    guardar_informe(resultados_originales, 'informe_videos_originales.json')
    
    # Analizar videos convertidos
    print("\n=== Analizando videos convertidos ===")
    resultados_convertidos = analizar_directorio('videos_convertidos')
    guardar_informe(resultados_convertidos, 'informe_videos_convertidos.json')
    
    print("\nAnálisis completado. Utilice Open Interpreter para analizar los informes.")

if __name__ == "__main__":
    main()
