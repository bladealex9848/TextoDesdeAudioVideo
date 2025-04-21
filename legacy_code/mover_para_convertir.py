#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para mover videos de videos_restantes a videos_originales para su conversión
"""

import os
import shutil

def main():
    # Verificar que los directorios existan
    if not os.path.exists("videos_restantes"):
        print("Error: El directorio 'videos_restantes' no existe.")
        return
    
    if not os.path.exists("videos_originales"):
        print("Creando directorio 'videos_originales'...")
        os.makedirs("videos_originales")
    
    # Obtener lista de videos restantes
    videos_restantes = []
    for archivo in os.listdir("videos_restantes"):
        if archivo.endswith(".mp4") and not archivo.endswith("_car_compatible.mp4"):
            videos_restantes.append(archivo)
    
    if not videos_restantes:
        print("No se encontraron videos restantes.")
        return
    
    print(f"Se encontraron {len(videos_restantes)} videos restantes.")
    
    # Mover cada video restante al directorio de originales
    videos_movidos = 0
    for video in videos_restantes:
        origen = os.path.join("videos_restantes", video)
        destino = os.path.join("videos_originales", video)
        
        try:
            shutil.move(origen, destino)
            videos_movidos += 1
            print(f"Movido: {video}")
        except Exception as e:
            print(f"Error al mover {video}: {str(e)}")
    
    print(f"\nResumen:")
    print(f"  - Videos restantes encontrados: {len(videos_restantes)}")
    print(f"  - Videos movidos a 'videos_originales': {videos_movidos}")

if __name__ == "__main__":
    main()
