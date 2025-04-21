#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para convertir todos los videos de 'videos_originales' a formato compatible con reproductores de carro,
guardarlos en 'videos_convertidos' y eliminar los originales una vez convertidos exitosamente.
"""

import os
import subprocess
import shutil
import sys
from pathlib import Path


def obtener_info_video(video_path):
    """Obtiene información del codec, resolución y framerate de un video."""
    try:
        # Obtener codec
        codec_cmd = f'ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 "{video_path}"'
        codec = subprocess.check_output(codec_cmd, shell=True).decode("utf-8").strip()

        # Obtener resolución
        resolution_cmd = f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "{video_path}"'
        resolution = (
            subprocess.check_output(resolution_cmd, shell=True).decode("utf-8").strip()
        )

        # Obtener framerate
        fps_cmd = f'ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of default=noprint_wrappers=1:nokey=1 "{video_path}"'
        fps_raw = subprocess.check_output(fps_cmd, shell=True).decode("utf-8").strip()

        # Convertir framerate de formato "num/den" a decimal
        if "/" in fps_raw:
            num, den = map(int, fps_raw.split("/"))
            fps = round(num / den, 2)
        else:
            fps = float(fps_raw)

        return {"codec": codec, "resolution": resolution, "fps": fps}
    except Exception as e:
        print(f"Error al obtener información del video {video_path}: {str(e)}")
        return None


def es_compatible_con_carro(info_video):
    """Verifica si un video es compatible con reproductores de carro."""
    if not info_video:
        return False

    # Verificar codec (debe ser H.264)
    if info_video["codec"] != "h264":
        return False

    # Verificar resolución (no debe ser mayor a 1920x1080)
    width, height = map(int, info_video["resolution"].split("x"))
    if width > 1920 or height > 1080:
        return False

    # Verificar framerate (idealmente 25fps, pero aceptamos entre 24 y 30)
    if info_video["fps"] < 24 or info_video["fps"] > 30:
        return False

    return True


def convertir_video(input_path, output_path):
    """Convierte un video a formato compatible con reproductores de carro."""
    try:
        # Convertir el video a H.264 con resolución 1080p y framerate 25fps
        cmd = f'ffmpeg -i "{input_path}" -c:v libx264 -profile:v high -level:v 4.0 -preset medium -crf 23 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" -r 25 -c:a aac -b:a 128k "{output_path}"'
        subprocess.run(cmd, shell=True, check=True)
        return True
    except Exception as e:
        print(f"Error al convertir el video {input_path}: {str(e)}")
        return False


def procesar_videos(max_videos=None):
    """Procesa todos los videos en 'videos_originales', los convierte y mueve a 'videos_convertidos'.

    Args:
        max_videos: Número máximo de videos a procesar. Si es None, procesa todos.
    """
    # Crear directorios si no existen
    dir_originales = "videos_originales"
    dir_convertidos = "videos_convertidos"

    if not os.path.exists(dir_originales):
        os.makedirs(dir_originales)
        print(f"Directorio '{dir_originales}' creado.")

    if not os.path.exists(dir_convertidos):
        os.makedirs(dir_convertidos)
        print(f"Directorio '{dir_convertidos}' creado.")

    # Obtener lista de videos en el directorio de originales
    extensiones_video = [
        ".mp4",
        ".mkv",
        ".avi",
        ".mov",
        ".webm",
        ".flv",
        ".wmv",
        ".3gp",
    ]
    videos = []

    for ext in extensiones_video:
        videos.extend(list(Path(dir_originales).glob(f"*{ext}")))

    if not videos:
        print(f"No se encontraron videos en '{dir_originales}'.")
        return

    # Limitar el número de videos a procesar si se especifica
    if max_videos is not None and max_videos > 0:
        videos = videos[:max_videos]
        print(
            f"Se procesarán {len(videos)} de {len(list(Path(dir_originales).glob('*')))} videos."
        )
    else:
        print(f"Se encontraron {len(videos)} videos para procesar.")

    # Procesar cada video
    videos_procesados = 0
    videos_eliminados = 0

    for video_path in videos:
        video_path_str = str(video_path)
        video_name = video_path.name
        base_name = video_path.stem
        output_path = os.path.join(dir_convertidos, f"{base_name}_car_compatible.mp4")

        print(f"\nProcesando: {video_name}")

        # Verificar si el video ya existe en el directorio de convertidos
        if os.path.exists(output_path):
            print(
                f"El video ya existe en '{dir_convertidos}', verificando compatibilidad..."
            )
            info_convertido = obtener_info_video(output_path)

            if es_compatible_con_carro(info_convertido):
                print(f"El video convertido es compatible con reproductores de carro.")
                print(f"Eliminando original: {video_name}")
                os.remove(video_path_str)
                videos_eliminados += 1
                videos_procesados += 1
                continue
            else:
                print(f"El video convertido NO es compatible. Reconvirtiendo...")
                os.remove(output_path)

        # Obtener información del video original
        info_video = obtener_info_video(video_path_str)

        if info_video:
            print(f"Información del video original:")
            print(f"  - Codec: {info_video['codec']}")
            print(f"  - Resolución: {info_video['resolution']}")
            print(f"  - FPS: {info_video['fps']}")

            # Verificar si el video ya es compatible
            if es_compatible_con_carro(info_video):
                print(f"El video ya es compatible con reproductores de carro.")
                print(f"Copiando a '{dir_convertidos}'...")
                shutil.copy2(video_path_str, output_path)
                print(f"Eliminando original: {video_name}")
                os.remove(video_path_str)
                videos_eliminados += 1
                videos_procesados += 1
                continue

        # Convertir el video
        print(f"Convirtiendo video a formato compatible...")
        if convertir_video(video_path_str, output_path):
            print(f"Conversión exitosa: {output_path}")

            # Verificar que la conversión fue exitosa
            info_convertido = obtener_info_video(output_path)
            if es_compatible_con_carro(info_convertido):
                print(f"El video convertido es compatible con reproductores de carro.")
                print(f"Eliminando original: {video_name}")
                os.remove(video_path_str)
                videos_eliminados += 1
                videos_procesados += 1
            else:
                print(
                    f"ADVERTENCIA: El video convertido NO es compatible con reproductores de carro."
                )
                videos_procesados += 1
        else:
            print(f"Error al convertir el video: {video_name}")

    # Resumen
    print("\n" + "=" * 50)
    print(f"Resumen del procesamiento:")
    print(f"  - Videos procesados: {videos_procesados}/{len(videos)}")
    print(f"  - Videos originales eliminados: {videos_eliminados}")
    print("=" * 50)


if __name__ == "__main__":
    import argparse

    # Crear parser de argumentos
    parser = argparse.ArgumentParser(
        description="Convierte videos para reproductores de carro"
    )
    parser.add_argument("--max", type=int, help="Número máximo de videos a procesar")
    args = parser.parse_args()

    print("Iniciando procesamiento de videos...")
    procesar_videos(max_videos=args.max)
    print("Procesamiento completado.")
