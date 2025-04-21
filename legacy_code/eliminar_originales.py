#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para eliminar videos originales que ya han sido convertidos
"""

import os
import re


def limpiar_nombre(nombre):
    """Limpia un nombre de archivo para comparación."""
    # Eliminar extensión si existe
    nombre = os.path.splitext(nombre)[0]

    # Eliminar sufijo _car_compatible si existe
    nombre = nombre.replace("_car_compatible", "")

    # Eliminar información de resolución y codec (patrones comunes)
    nombre = re.sub(r"\([^)]*p_[^)]*\)", "", nombre)
    nombre = re.sub(r"\([^)]*fps_[^)]*\)", "", nombre)
    nombre = re.sub(r"\d+p_\d+fps_[^-_\s]*", "", nombre)

    # Convertir a minúsculas
    nombre = nombre.lower()

    # Eliminar caracteres especiales y espacios
    nombre = re.sub(r"[^a-z0-9]", "", nombre)

    return nombre


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

    # Crear un diccionario para mapear nombres limpios a archivos originales
    videos_originales = {}
    for archivo in os.listdir("videos_originales"):
        if archivo.endswith(".mp4") and not archivo.endswith("_car_compatible.mp4"):
            nombre_limpio = limpiar_nombre(archivo)
            videos_originales[nombre_limpio] = archivo

    print(f"Se encontraron {len(videos_originales)} videos originales.")

    # Procesar cada video convertido
    videos_eliminados = 0
    for video_convertido in videos_convertidos:
        nombre_convertido_limpio = limpiar_nombre(video_convertido)

        # Buscar coincidencias exactas primero
        if nombre_convertido_limpio in videos_originales:
            archivo_original = videos_originales[nombre_convertido_limpio]
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
        mejor_coincidencia = None
        mejor_puntuacion = 0

        for nombre_original_limpio, archivo_original in list(videos_originales.items()):
            # Calcular puntuación de coincidencia
            puntuacion = 0

            # Si uno contiene al otro completamente
            if nombre_convertido_limpio in nombre_original_limpio:
                puntuacion = (
                    len(nombre_convertido_limpio) / len(nombre_original_limpio) * 100
                )
            elif nombre_original_limpio in nombre_convertido_limpio:
                puntuacion = (
                    len(nombre_original_limpio) / len(nombre_convertido_limpio) * 100
                )
            else:
                # Contar caracteres comunes
                caracteres_comunes = sum(
                    1 for c in nombre_convertido_limpio if c in nombre_original_limpio
                )
                puntuacion = (
                    caracteres_comunes
                    / max(len(nombre_convertido_limpio), len(nombre_original_limpio))
                    * 50
                )

            if puntuacion > mejor_puntuacion and puntuacion > 50:  # Umbral de 50%
                mejor_puntuacion = puntuacion
                mejor_coincidencia = archivo_original

        if mejor_coincidencia:
            ruta_original = os.path.join("videos_originales", mejor_coincidencia)
            print(
                f"Eliminando video original (coincidencia {mejor_puntuacion:.1f}%): {mejor_coincidencia}"
            )
            try:
                os.remove(ruta_original)
                videos_eliminados += 1
                # Eliminar del diccionario para evitar eliminar el mismo archivo más de una vez
                del videos_originales[limpiar_nombre(mejor_coincidencia)]
            except Exception as e:
                print(f"Error al eliminar {mejor_coincidencia}: {str(e)}")

    print(f"\nResumen:")
    print(f"  - Videos convertidos encontrados: {len(videos_convertidos)}")
    print(f"  - Videos originales eliminados: {videos_eliminados}")


if __name__ == "__main__":
    main()
