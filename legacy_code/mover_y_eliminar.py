#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para mover videos convertidos y eliminar originales
"""

import os


def main():
    # Verificar que los directorios existan
    if not os.path.exists("videos_originales"):
        print("Error: El directorio 'videos_originales' no existe.")
        return

    if not os.path.exists("videos_convertidos"):
        print("Error: El directorio 'videos_convertidos' no existe.")
        return

    # Obtener lista de videos convertidos
    videos_convertidos = []
    for archivo in os.listdir("videos_convertidos"):
        if archivo.endswith("_car_compatible.mp4"):
            videos_convertidos.append(archivo)

    if not videos_convertidos:
        print("No se encontraron videos convertidos.")
        return

    print(f"Se encontraron {len(videos_convertidos)} videos convertidos.")

    videos_eliminados = 0

    # Crear un diccionario para mapear nombres de videos convertidos a sus originales
    videos_originales = {}
    for archivo in os.listdir("videos_originales"):
        if archivo.endswith(".mp4") and not archivo.endswith("_car_compatible.mp4"):
            # Guardar el nombre sin extensión
            nombre_base = os.path.splitext(archivo)[0]
            videos_originales[nombre_base] = archivo

    # Procesar cada video convertido
    for video_convertido in videos_convertidos:
        # Obtener el nombre base del video convertido (sin el sufijo _car_compatible)
        nombre_base = video_convertido.replace("_car_compatible.mp4", "")

        # Buscar coincidencias exactas primero
        if nombre_base in videos_originales:
            archivo_original = videos_originales[nombre_base]
            ruta_original = os.path.join("videos_originales", archivo_original)
            print(
                f"Eliminando video original (coincidencia exacta): {archivo_original}"
            )
            try:
                os.remove(ruta_original)
                videos_eliminados += 1
                continue
            except Exception as e:
                print(f"Error al eliminar {archivo_original}: {str(e)}")

        # Si no hay coincidencia exacta, buscar coincidencias parciales
        for nombre_original, archivo_original in videos_originales.items():
            # Comparar ignorando mayúsculas/minúsculas y algunos caracteres especiales
            nombre_base_limpio = (
                nombre_base.lower().replace(" ", "").replace("-", "").replace("_", "")
            )
            nombre_original_limpio = (
                nombre_original.lower()
                .replace(" ", "")
                .replace("-", "")
                .replace("_", "")
            )

            # Verificar si el nombre original está contenido en el nombre convertido o viceversa
            if (
                nombre_base_limpio in nombre_original_limpio
                or nombre_original_limpio in nombre_base_limpio
            ):
                ruta_original = os.path.join("videos_originales", archivo_original)
                print(
                    f"Eliminando video original (coincidencia parcial): {archivo_original}"
                )
                try:
                    os.remove(ruta_original)
                    videos_eliminados += 1
                    break
                except Exception as e:
                    print(f"Error al eliminar {archivo_original}: {str(e)}")

    print(f"\nResumen:")
    print(f"  - Videos convertidos encontrados: {len(videos_convertidos)}")
    print(f"  - Videos originales eliminados: {videos_eliminados}")


if __name__ == "__main__":
    main()
