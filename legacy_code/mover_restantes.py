#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para mover los videos originales restantes a un directorio separado
"""

import os
import shutil

def main():
    # Verificar que los directorios existan
    if not os.path.exists("videos_originales"):
        print("Error: El directorio 'videos_originales' no existe.")
        return
    
    # Crear directorio para videos restantes
    directorio_restantes = "videos_restantes"
    if not os.path.exists(directorio_restantes):
        os.makedirs(directorio_restantes)
        print(f"Directorio '{directorio_restantes}' creado.")
    
    # Obtener lista de videos originales
    videos_originales = []
    for archivo in os.listdir("videos_originales"):
        if archivo.endswith(".mp4") and not archivo.endswith("_car_compatible.mp4"):
            videos_originales.append(archivo)
    
    if not videos_originales:
        print("No se encontraron videos originales.")
        return
    
    print(f"Se encontraron {len(videos_originales)} videos originales.")
    
    # Mover cada video original al directorio de restantes
    videos_movidos = 0
    for video in videos_originales:
        origen = os.path.join("videos_originales", video)
        destino = os.path.join(directorio_restantes, video)
        
        try:
            shutil.move(origen, destino)
            videos_movidos += 1
            print(f"Movido: {video}")
        except Exception as e:
            print(f"Error al mover {video}: {str(e)}")
    
    print(f"\nResumen:")
    print(f"  - Videos originales encontrados: {len(videos_originales)}")
    print(f"  - Videos movidos a '{directorio_restantes}': {videos_movidos}")
    
    # Verificar si quedan videos originales
    videos_restantes = len([f for f in os.listdir("videos_originales") if f.endswith(".mp4")])
    print(f"  - Videos originales restantes: {videos_restantes}")

if __name__ == "__main__":
    main()
