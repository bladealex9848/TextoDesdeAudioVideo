#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar que todos los videos estén convertidos
"""

import os
import re

def obtener_nombre_base(nombre):
    """Extrae el nombre base del archivo sin información técnica."""
    # Eliminar extensión
    nombre = os.path.splitext(nombre)[0]
    
    # Eliminar sufijo _car_compatible
    nombre = nombre.replace("_car_compatible", "")
    
    # Eliminar información técnica entre paréntesis
    nombre = re.sub(r'\([^)]*\)', '', nombre)
    
    # Eliminar patrones de resolución y codec
    nombre = re.sub(r'\d+p_\d+fps_[^-_\s]*', '', nombre)
    
    return nombre.strip()

def main():
    # Verificar que los directorios existan
    if not os.path.exists("videos_originales"):
        print("Error: El directorio 'videos_originales' no existe.")
        return
    
    if not os.path.exists("videos_convertidos"):
        print("Error: El directorio 'videos_convertidos' no existe.")
        return
    
    # Obtener lista de videos originales
    videos_originales = []
    for archivo in os.listdir("videos_originales"):
        if archivo.endswith(".mp4") and not archivo.endswith("_car_compatible.mp4"):
            videos_originales.append(archivo)
    
    # Obtener lista de videos convertidos
    videos_convertidos = []
    for archivo in os.listdir("videos_convertidos"):
        if archivo.endswith("_car_compatible.mp4"):
            videos_convertidos.append(archivo)
    
    # Crear un mapa de nombres base a archivos convertidos
    mapa_convertidos = {}
    for video in videos_convertidos:
        nombre_base = obtener_nombre_base(video).lower()
        mapa_convertidos[nombre_base] = video
    
    # Verificar qué videos originales aún no han sido convertidos
    videos_pendientes = []
    for video_original in videos_originales:
        nombre_base = obtener_nombre_base(video_original).lower()
        
        # Verificar si existe un video convertido con el mismo nombre base
        if nombre_base not in mapa_convertidos:
            videos_pendientes.append(video_original)
    
    # Mostrar resumen
    print(f"\nResumen de conversión:")
    print(f"  - Videos originales: {len(videos_originales)}")
    print(f"  - Videos convertidos: {len(videos_convertidos)}")
    print(f"  - Videos pendientes: {len(videos_pendientes)}")
    
    # Mostrar porcentaje de progreso
    if videos_originales:
        progreso = (len(videos_originales) - len(videos_pendientes)) / len(videos_originales) * 100
        print(f"  - Progreso: {progreso:.1f}%")
    
    # Mostrar los videos pendientes
    if videos_pendientes:
        print("\nVideos pendientes de conversión:")
        for video in videos_pendientes[:10]:  # Mostrar solo los primeros 10
            print(f"  - {video}")
        
        if len(videos_pendientes) > 10:
            print(f"  ... y {len(videos_pendientes) - 10} más")
    else:
        print("\n¡Todos los videos han sido convertidos!")

if __name__ == "__main__":
    main()
