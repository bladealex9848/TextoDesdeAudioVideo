#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para eliminar todos los videos originales que ya han sido convertidos
"""

import os
import re
import shutil


def obtener_nombre_base(nombre):
    """Extrae el nombre base del archivo sin información técnica."""
    # Eliminar extensión
    nombre = os.path.splitext(nombre)[0]

    # Eliminar sufijo _car_compatible
    nombre = nombre.replace("_car_compatible", "")

    # Eliminar información técnica entre paréntesis
    nombre = re.sub(r"\([^)]*\)", "", nombre)

    # Eliminar patrones de resolución y codec
    nombre = re.sub(r"\d+p_\d+fps_[^-_\s]*", "", nombre)

    return nombre.strip()


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

    # Obtener lista de videos originales
    videos_originales = []
    for archivo in os.listdir("videos_originales"):
        if archivo.endswith(".mp4") and not archivo.endswith("_car_compatible.mp4"):
            videos_originales.append(archivo)

    print(f"Se encontraron {len(videos_originales)} videos originales.")

    # Crear un mapa de nombres base a archivos
    mapa_convertidos = {}
    for video in videos_convertidos:
        nombre_base = obtener_nombre_base(video)
        mapa_convertidos[nombre_base.lower()] = video

    # Procesar cada video original
    videos_eliminados = 0
    for video_original in videos_originales:
        nombre_base = obtener_nombre_base(video_original)

        # Verificar si existe un video convertido con el mismo nombre base
        if nombre_base.lower() in mapa_convertidos:
            video_convertido = mapa_convertidos[nombre_base.lower()]
            print(f"Coincidencia encontrada:")
            print(f"  Original: {video_original}")
            print(f"  Convertido: {video_convertido}")

            # Eliminar el video original
            try:
                os.remove(os.path.join("videos_originales", video_original))
                videos_eliminados += 1
                print(f"  ✓ Video original eliminado")
            except Exception as e:
                print(f"  ✗ Error al eliminar: {str(e)}")

            print()

    # Verificar si hay videos originales que no tienen coincidencia
    print("\nBuscando coincidencias parciales para videos restantes...")

    # Obtener lista actualizada de videos originales
    videos_originales_restantes = []
    for archivo in os.listdir("videos_originales"):
        if archivo.endswith(".mp4") and not archivo.endswith("_car_compatible.mp4"):
            videos_originales_restantes.append(archivo)

    # Crear un mapa de palabras clave a videos convertidos
    mapa_palabras_clave = {}
    for video in videos_convertidos:
        nombre_base = obtener_nombre_base(video)
        palabras = re.findall(r"[A-Za-z0-9]+", nombre_base)
        for palabra in palabras:
            if len(palabra) > 3:  # Solo palabras significativas
                palabra = palabra.lower()
                if palabra not in mapa_palabras_clave:
                    mapa_palabras_clave[palabra] = []
                mapa_palabras_clave[palabra].append(video)

    # Buscar coincidencias parciales
    for video_original in videos_originales_restantes:
        nombre_base = obtener_nombre_base(video_original)
        palabras = re.findall(r"[A-Za-z0-9]+", nombre_base)

        # Contar coincidencias de palabras clave
        coincidencias = {}
        for palabra in palabras:
            if len(palabra) > 3:
                palabra = palabra.lower()
                if palabra in mapa_palabras_clave:
                    for video_convertido in mapa_palabras_clave[palabra]:
                        if video_convertido not in coincidencias:
                            coincidencias[video_convertido] = 0
                        coincidencias[video_convertido] += 1

        # Encontrar la mejor coincidencia
        mejor_video = None
        mejor_puntuacion = 0
        for video, puntuacion in coincidencias.items():
            if puntuacion > mejor_puntuacion:
                mejor_puntuacion = puntuacion
                mejor_video = video

        # Si hay una buena coincidencia, eliminar el video original
        if mejor_puntuacion >= 1:  # Al menos 1 palabra clave en común
            print(
                f"Coincidencia parcial encontrada ({mejor_puntuacion} palabras clave):"
            )
            print(f"  Original: {video_original}")
            print(f"  Convertido: {mejor_video}")

            # Eliminar el video original
            try:
                os.remove(os.path.join("videos_originales", video_original))
                videos_eliminados += 1
                print(f"  ✓ Video original eliminado")
            except Exception as e:
                print(f"  ✗ Error al eliminar: {str(e)}")

            print()

    print(f"\nResumen:")
    print(f"  - Videos convertidos encontrados: {len(videos_convertidos)}")
    print(f"  - Videos originales eliminados: {videos_eliminados}")

    # Verificar si quedan videos originales
    videos_restantes = len(
        [f for f in os.listdir("videos_originales") if f.endswith(".mp4")]
    )
    print(f"  - Videos originales restantes: {videos_restantes}")


if __name__ == "__main__":
    main()
