# -*- coding: utf-8 -*-
"""
TextoDesdeAudioVideo - Suite de Procesamiento de Audio y Video

Este script ofrece una suite completa de herramientas para el procesamiento de audio y video,
así como transcripción de audio.
"""

"""# Suite de Procesamiento de Audio y Video en Google Colab

Este script de Python para Google Colab ofrece una suite completa de herramientas para el procesamiento de audio y video, así como transcripción de audio. Las funcionalidades incluyen:

1. División de archivos de audio (mp3, wav, ogg) en segmentos de duración específica.
2. Mejora de la calidad del audio mediante normalización y realce de frecuencias.
3. Transcripción de audio utilizando varios modelos de Whisper de OpenAI.
4. Conversión de archivos de video a diferentes formatos de audio.

El script opera con archivos ubicados en el directorio '/content/' de Google Colab, facilitando la gestión de archivos. Todas las operaciones se realizan a través de un menú interactivo, permitiendo al usuario seleccionar archivos, especificar parámetros y elegir opciones de procesamiento según sea necesario. Los archivos procesados se guardan automáticamente en el mismo directorio con nombres descriptivos.

Características destacadas:
- Soporta múltiples formatos de entrada para audio y video.
- Permite seleccionar entre diferentes modelos de Whisper para la transcripción.
- Ofrece opciones de conversión de video a varios formatos de audio (mp3, wav, ogg).
- Divide archivos de audio en varios formatos soportados.

Instrucciones de uso:
1. Ejecute el script en un notebook de Google Colab.
2. Suba sus archivos de audio o video al directorio '/content/'.
3. Siga las instrucciones del menú para procesar sus archivos.

Nota: Asegúrese de tener una conexión estable a internet para la instalación de dependencias y el uso de los modelos de Whisper.
"""

import os
import argparse
import subprocess
from pydub import AudioSegment
import librosa
import soundfile as sf
import whisper
from moviepy.editor import VideoFileClip


# Función para listar archivos de audio y video en el directorio actual
def list_media_files(directory="."):
    media_files = [
        f
        for f in os.listdir(directory)
        if f.endswith((".mp3", ".wav", ".ogg", ".mp4", ".avi", ".mov", ".mkv"))
    ]
    return media_files


# Función para dividir el archivo de audio
def split_audio(input_file, split_time):
    audio = AudioSegment.from_file(input_file)
    duration = len(audio)
    split_ms = int(
        split_time * 60 * 1000
    )  # Convertir minutos a milisegundos y a entero

    base_name, extension = os.path.splitext(os.path.basename(input_file))

    for i, start in enumerate(range(0, duration, split_ms)):
        end = start + split_ms
        if end > duration:
            end = duration
        chunk = audio[start:end]
        output_file = f"{base_name}_part_{i+1}{extension}"
        chunk.export(output_file, format=extension[1:])
        print(f"Parte {i+1} guardada: {output_file}")


# Función para mejorar la calidad del audio
def enhance_audio(input_file):
    # Cargar el archivo de audio
    y, sr = librosa.load(input_file)

    # Aplicar normalización
    y_normalized = librosa.util.normalize(y)

    # Aplicar un filtro de realce de frecuencias
    y_enhanced = librosa.effects.preemphasis(y_normalized)

    # Generar el nombre del archivo de salida
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = f"{base_name}_enhanced.wav"

    # Guardar el audio mejorado
    sf.write(output_file, y_enhanced, sr)
    print(f"Audio mejorado guardado: {output_file}")


# Función para transcribir audio con Whisper
def transcribe_audio(input_file, model_name):
    model = whisper.load_model(model_name)
    result = model.transcribe(
        input_file, language="es"
    )  # Agregar el parámetro language='es' para español

    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = f"{base_name}_transcription.txt"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result["text"])

    print(f"Transcripción guardada: {output_file}")


# Función para convertir video a audio
def convert_video_to_audio(input_file, output_format):
    video = VideoFileClip(input_file)
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = f"{base_name}.{output_format}"

    if output_format == "mp3":
        video.audio.write_audiofile(output_file)
    elif output_format == "wav":
        video.audio.write_audiofile(output_file, codec="pcm_s16le")
    elif output_format == "ogg":
        video.audio.write_audiofile(output_file, codec="libvorbis")

    video.close()
    print(f"Audio extraído y guardado como: {output_file}")


# Interfaz para dividir audio
def split_audio_interface():
    audio_files = [
        f for f in list_media_files() if f.endswith((".mp3", ".wav", ".ogg"))
    ]
    if not audio_files:
        print("No se encontraron archivos de audio en el directorio actual")
        return

    print("Archivos de audio disponibles:")
    for i, file in enumerate(audio_files):
        print(f"{i+1}. {file}")

    file_index = int(input("Seleccione el número del archivo a dividir: ")) - 1
    if file_index < 0 or file_index >= len(audio_files):
        print("Selección no válida")
        return

    input_file = audio_files[file_index]
    split_time = float(input("Ingrese el tiempo de división en minutos: "))

    split_audio(input_file, split_time)


# Interfaz para mejorar audio
def enhance_audio_interface():
    audio_files = [
        f for f in list_media_files() if f.endswith((".mp3", ".wav", ".ogg"))
    ]
    if not audio_files:
        print("No se encontraron archivos de audio en el directorio actual")
        return

    print("Archivos de audio disponibles:")
    for i, file in enumerate(audio_files):
        print(f"{i+1}. {file}")

    file_index = int(input("Seleccione el número del archivo a mejorar: ")) - 1
    if file_index < 0 or file_index >= len(audio_files):
        print("Selección no válida")
        return

    input_file = audio_files[file_index]
    enhance_audio(input_file)


# Interfaz para transcribir audio
def transcribe_audio_interface():
    audio_files = [
        f for f in list_media_files() if f.endswith((".mp3", ".wav", ".ogg"))
    ]
    if not audio_files:
        print("No se encontraron archivos de audio en el directorio actual")
        return

    print("Archivos de audio disponibles:")
    for i, file in enumerate(audio_files):
        print(f"{i+1}. {file}")

    file_index = int(input("Seleccione el número del archivo a transcribir: ")) - 1
    if file_index < 0 or file_index >= len(audio_files):
        print("Selección no válida")
        return

    input_file = audio_files[file_index]

    print("\nModelos de Whisper disponibles:")
    print("1. tiny")
    print("2. base")
    print("3. small")
    print("4. medium")
    print("5. large")

    model_choice = input("Seleccione el número del modelo a utilizar: ")
    model_names = ["tiny", "base", "small", "medium", "large"]
    model_name = model_names[int(model_choice) - 1]

    transcribe_audio(input_file, model_name)


# Interfaz para convertir video a audio
def convert_video_to_audio_interface():
    video_files = [
        f for f in list_media_files() if f.endswith((".mp4", ".avi", ".mov", ".mkv"))
    ]
    if not video_files:
        print("No se encontraron archivos de video en el directorio actual")
        return

    print("Archivos de video disponibles:")
    for i, file in enumerate(video_files):
        print(f"{i+1}. {file}")

    file_index = int(input("Seleccione el número del archivo a convertir: ")) - 1
    if file_index < 0 or file_index >= len(video_files):
        print("Selección no válida")
        return

    input_file = video_files[file_index]

    print("\nFormatos de audio disponibles:")
    print("1. mp3")
    print("2. wav")
    print("3. ogg")

    format_choice = input("Seleccione el número del formato de salida: ")
    output_formats = ["mp3", "wav", "ogg"]
    output_format = output_formats[int(format_choice) - 1]

    convert_video_to_audio(input_file, output_format)


def convert_video_for_car(input_file, output_file=None):
    """Convierte un video a formato compatible con reproductores de carro (H.264, 1080p, 25fps)"""
    if not os.path.exists(input_file):
        print(f"Error: El archivo {input_file} no existe")
        return

    # Si no se especifica un archivo de salida, crear uno con sufijo '_car_compatible'
    if output_file is None:
        file_name_without_extension = os.path.splitext(input_file)[0]
        file_extension = os.path.splitext(input_file)[1]
        output_file = f"{file_name_without_extension}_car_compatible{file_extension}"

    try:
        # Verificar si el video ya está en formato H.264
        probe_cmd = f'ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 "{input_file}"'
        codec = subprocess.check_output(probe_cmd, shell=True).decode("utf-8").strip()

        if codec == "h264":
            # Verificar la resolución
            resolution_cmd = f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "{input_file}"'
            resolution = (
                subprocess.check_output(resolution_cmd, shell=True)
                .decode("utf-8")
                .strip()
            )
            width, height = map(int, resolution.split("x"))

            if width <= 1920 and height <= 1080:
                # El video ya es compatible, solo copiarlo
                import shutil

                shutil.copy2(input_file, output_file)
                print(f"El video ya es compatible. Copiado a {output_file}")
                return

        # Convertir el video a H.264 con resolución 1080p y framerate 25fps
        cmd = f'ffmpeg -i "{input_file}" -c:v libx264 -profile:v high -level:v 4.0 -preset medium -crf 23 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" -r 25 -c:a aac -b:a 128k "{output_file}"'
        subprocess.run(cmd, shell=True, check=True)
        print(f"Video convertido exitosamente: {output_file}")
    except Exception as e:
        print(f"Error al convertir el video: {str(e)}")


def batch_convert_videos_for_car(input_dir, output_dir):
    """Convierte todos los videos en un directorio a formato compatible con reproductores de carro"""
    # Verificar que los directorios existan
    if not os.path.exists(input_dir):
        print(f"Error: El directorio de entrada {input_dir} no existe")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Obtener todos los archivos de video en el directorio de entrada
    video_files = [
        f
        for f in os.listdir(input_dir)
        if f.endswith((".mp4", ".mkv", ".avi", ".mov", ".webm"))
    ]

    if not video_files:
        print(f"No se encontraron archivos de video en {input_dir}")
        return

    print(f"Se encontraron {len(video_files)} archivos de video para procesar")

    for video_file in video_files:
        input_path = os.path.join(input_dir, video_file)
        file_name_without_extension = os.path.splitext(video_file)[0]
        output_path = os.path.join(
            output_dir, f"{file_name_without_extension}_car_compatible.mp4"
        )

        # Verificar si el archivo ya existe en el directorio de salida
        if os.path.exists(output_path):
            print(f"{video_file}: Ya convertido anteriormente")
            continue

        print(f"Procesando: {video_file}")
        convert_video_for_car(input_path, output_path)


def main():
    parser = argparse.ArgumentParser(
        description="Suite de Procesamiento de Audio y Video"
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=[
            "split",
            "enhance",
            "transcribe",
            "convert",
            "convert-car",
            "batch-convert-car",
            "interactive",
        ],
        default="interactive",
        help="Modo de operación",
    )
    parser.add_argument("--input", type=str, help="Archivo de entrada")
    parser.add_argument(
        "--split-time", type=float, help="Tiempo de división en minutos"
    )
    parser.add_argument(
        "--model",
        type=str,
        choices=["tiny", "base", "small", "medium", "large"],
        default="small",
        help="Modelo de Whisper para transcripción",
    )
    parser.add_argument(
        "--language", type=str, default="es", help="Idioma para transcripción"
    )
    parser.add_argument(
        "--output-format",
        type=str,
        choices=["mp3", "wav", "ogg"],
        default="mp3",
        help="Formato de salida para conversión de video a audio",
    )

    args = parser.parse_args()

    if args.mode == "interactive":
        # Menú principal interactivo
        while True:
            print("\n1. Dividir archivo de audio")
            print("2. Mejorar calidad de audio")
            print("3. Transcribir audio")
            print("4. Convertir video a audio")
            print("5. Convertir video para reproductor de carro")
            print("6. Procesar todos los videos para reproductores de carro")
            print("7. Salir")
            choice = input("Seleccione una opción (1-7): ")

            if choice == "1":
                split_audio_interface()
            elif choice == "2":
                enhance_audio_interface()
            elif choice == "3":
                transcribe_audio_interface()
            elif choice == "4":
                convert_video_to_audio_interface()
            elif choice == "5":
                # Interfaz para convertir video para reproductor de carro
                video_files = [
                    f
                    for f in list_media_files()
                    if f.endswith((".mp4", ".mkv", ".avi", ".mov", ".webm"))
                ]
                if not video_files:
                    print("No se encontraron archivos de video en el directorio actual")
                    continue

                print("Archivos de video disponibles:")
                for i, file in enumerate(video_files):
                    print(f"{i+1}. {file}")

                file_index = (
                    int(input("Seleccione el número del archivo a convertir: ")) - 1
                )
                if file_index < 0 or file_index >= len(video_files):
                    print("Selección no válida")
                    continue

                input_file = video_files[file_index]
                convert_video_for_car(input_file)
            elif choice == "6":
                # Procesar todos los videos para reproductores de carro
                input_dir = (
                    input(
                        "Directorio de entrada (presione Enter para usar 'videos_originales'): "
                    )
                    or "videos_originales"
                )
                output_dir = (
                    input(
                        "Directorio de salida (presione Enter para usar 'videos_convertidos'): "
                    )
                    or "videos_convertidos"
                )
                batch_convert_videos_for_car(input_dir, output_dir)
            elif choice == "7":
                break
            else:
                print("Opción no válida. Por favor, intente de nuevo.")

        print(
            "Gracias por usar la Suite de Procesamiento de Audio y Video. ¡Hasta la próxima!"
        )

    elif args.mode == "split":
        if not args.input or not args.split_time:
            print("Error: Se requiere --input y --split-time para el modo 'split'")
            return
        split_audio(args.input, args.split_time)

    elif args.mode == "enhance":
        if not args.input:
            print("Error: Se requiere --input para el modo 'enhance'")
            return
        enhance_audio(args.input)

    elif args.mode == "transcribe":
        if not args.input:
            print("Error: Se requiere --input para el modo 'transcribe'")
            return
        transcribe_audio(args.input, args.model)

    elif args.mode == "convert":
        if not args.input:
            print("Error: Se requiere --input para el modo 'convert'")
            return
        convert_video_to_audio(args.input, args.output_format)

    elif args.mode == "convert-car":
        if not args.input:
            print("Error: Se requiere --input para el modo 'convert-car'")
            return
        convert_video_for_car(args.input)

    elif args.mode == "batch-convert-car":
        input_dir = args.input if args.input else "videos_originales"
        output_dir = "videos_convertidos"
        batch_convert_videos_for_car(input_dir, output_dir)


if __name__ == "__main__":
    main()
