#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para limpiar directorios después de la conversión
"""

import os
import shutil

def main():
    # Verificar que los directorios existan
    if os.path.exists("videos_restantes"):
        print(f"Eliminando directorio 'videos_restantes'...")
        try:
            shutil.rmtree("videos_restantes")
            print(f"Directorio 'videos_restantes' eliminado correctamente.")
        except Exception as e:
            print(f"Error al eliminar directorio 'videos_restantes': {str(e)}")
    else:
        print("El directorio 'videos_restantes' no existe.")
    
    # Verificar si hay videos en videos_originales
    if os.path.exists("videos_originales"):
        videos_originales = [f for f in os.listdir("videos_originales") if f.endswith(".mp4")]
        if videos_originales:
            print(f"Aún hay {len(videos_originales)} videos en 'videos_originales'.")
            print("Estos videos deben ser procesados antes de eliminar el directorio.")
        else:
            print("No hay videos en 'videos_originales'.")
    else:
        print("El directorio 'videos_originales' no existe.")
    
    # Verificar videos convertidos
    if os.path.exists("videos_convertidos"):
        videos_convertidos = [f for f in os.listdir("videos_convertidos") if f.endswith("_car_compatible.mp4")]
        print(f"Hay {len(videos_convertidos)} videos convertidos en 'videos_convertidos'.")
    else:
        print("El directorio 'videos_convertidos' no existe.")

if __name__ == "__main__":
    main()
