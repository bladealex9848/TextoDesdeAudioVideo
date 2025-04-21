#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para finalizar el proceso de conversión
"""

import os
import shutil
import time
from datetime import datetime

def main():
    print(f"Iniciando proceso de finalización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Verificar que los directorios existan
    if not os.path.exists("videos_originales"):
        print("Error: El directorio 'videos_originales' no existe.")
        return
    
    if not os.path.exists("videos_convertidos"):
        print("Error: El directorio 'videos_convertidos' no existe.")
        return
    
    # Esperar a que se complete la conversión
    while True:
        # Verificar si hay videos en videos_originales
        videos_originales = [f for f in os.listdir("videos_originales") if f.endswith(".mp4")]
        
        if not videos_originales:
            print("No hay videos en 'videos_originales'. La conversión ha terminado.")
            break
        
        print(f"Aún hay {len(videos_originales)} videos en 'videos_originales'. Esperando...")
        time.sleep(60)  # Esperar 1 minuto antes de verificar nuevamente
    
    # Eliminar directorio videos_restantes
    if os.path.exists("videos_restantes"):
        print(f"Eliminando directorio 'videos_restantes'...")
        try:
            shutil.rmtree("videos_restantes")
            print(f"Directorio 'videos_restantes' eliminado correctamente.")
        except Exception as e:
            print(f"Error al eliminar directorio 'videos_restantes': {str(e)}")
    else:
        print("El directorio 'videos_restantes' no existe.")
    
    # Verificar videos convertidos
    if os.path.exists("videos_convertidos"):
        videos_convertidos = [f for f in os.listdir("videos_convertidos") if f.endswith("_car_compatible.mp4")]
        print(f"Hay {len(videos_convertidos)} videos convertidos en 'videos_convertidos'.")
    else:
        print("El directorio 'videos_convertidos' no existe.")
    
    print(f"Proceso finalizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
