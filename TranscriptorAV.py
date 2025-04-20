import os
import streamlit as st
from PIL import Image
import subprocess
import zipfile
import io
import shutil
import uuid
import time
import tempfile

# Importación condicional de moviepy para evitar errores en Streamlit Cloud
try:
    from moviepy.editor import VideoFileClip

    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    st.warning(
        "La biblioteca moviepy no está disponible. Algunas funcionalidades de procesamiento de video estarán limitadas."
    )

# Configuración de Streamlit / Streamlit Configuration
st.set_page_config(
    page_title="TranscriptorAV: Tu asistente para transcripciones de audio y video",
    page_icon="🎙️",
    initial_sidebar_state="collapsed",
    menu_items={
        "Get Help": "https://www.isabellaea.com",  # Actualiza con tu URL de ayuda si es necesario
        "Report a bug": None,  # Puedes agregar un enlace para reportar errores si lo deseas
        "About": (
            "TranscriptorAV es una herramienta avanzada para la transcripción automática "
            "de archivos de audio y video. Utiliza modelos de aprendizaje profundo para "
            "convertir con precisión contenido multimedia en texto, facilitando la accesibilidad y "
            "la comprensión del contenido. Esta herramienta es ideal para periodistas, estudiantes, "
            "profesionales de medios y cualquier persona que necesite transcribir contenido multimedia."
        ),
    },
)

# Carga y muestra el logo de la aplicación / Load and show the application logo
try:
    logo = Image.open("img/logo.png")
    st.image(logo, width=250)
except Exception as e:
    st.write("TranscriptorAV: Suite de Procesamiento de Audio y Video")


# Funciones de internacionalización y manejo de errores / Internationalization and error handling functions
def get_text(text_key, lang):
    texts = {
        "title": {
            "es": "TranscriptorAV: Suite de Procesamiento de Audio y Video",
            "en": "TranscriptorAV: Audio and Video Processing Suite",
        },
        "task_convert_for_car": {
            "es": "Convertir video para reproductor de carro",
            "en": "Convert video for car player",
        },
        "select_language": {"es": "Selecciona el idioma", "en": "Select the language"},
        "select_model": {
            "es": "Selecciona el modelo de Whisper",
            "en": "Select the Whisper model",
        },
        "upload_file": {
            "es": "Sube tu archivo de audio o video.",
            "en": "Upload your audio or video file.",
        },
        "choose_file": {"es": "Elige un archivo", "en": "Choose a file"},
        "file_uploaded": {"es": "Archivo cargado: ", "en": "File uploaded: "},
        "process": {"es": "Procesar", "en": "Process"},
        "download_file": {
            "es": "Descargar archivo",
            "en": "Download file",
        },
        "download_zip": {
            "es": "Descargar archivo comprimido",
            "en": "Download compressed file",
        },
        "error_file_write": {
            "es": "Error al escribir el archivo en el servidor.",
            "en": "Error writing the file to the server.",
        },
        "error_cmd_execution": {
            "es": "Error al ejecutar el comando.",
            "en": "Error executing command.",
        },
        "error_file_zip": {
            "es": "Error al comprimir los archivos.",
            "en": "Error compressing the files.",
        },
        "error_file_cleanup": {
            "es": "Error al limpiar los archivos temporales.",
            "en": "Error cleaning up temporary files.",
        },
        "file_processed_success": {
            "es": "Archivo procesado exitosamente.",
            "en": "File successfully processed.",
        },
        "created_by": {"es": "Creado por:", "en": "Created by:"},
        "agent_description": {
            "es": (
                "TranscriptorAV es una suite completa de procesamiento de audio y video. "
                "Ofrece funcionalidades para transcribir audio a texto, cambiar la resolución de videos, "
                "comprimir videos manteniendo la calidad, y convertir videos a diferentes formatos de audio. "
                "Todas estas herramientas están diseñadas para facilitar tu trabajo con archivos multimedia."
            ),
            "en": (
                "TranscriptorAV is a comprehensive audio and video processing suite. "
                "It offers functionalities to transcribe audio to text, change video resolution, "
                "compress videos while maintaining quality, and convert videos to different audio formats. "
                "All these tools are designed to facilitate your work with multimedia files."
            ),
        },
        "select_task": {
            "es": "Selecciona la tarea a realizar",
            "en": "Select the task to perform",
        },
        "task_transcribe": {
            "es": "Transcribir audio/video a texto",
            "en": "Transcribe audio/video to text",
        },
        "task_change_resolution": {
            "es": "Cambiar resolución de video",
            "en": "Change video resolution",
        },
        "task_compress_video": {
            "es": "Comprimir video",
            "en": "Compress video",
        },
        "task_convert_to_audio": {
            "es": "Convertir video a audio",
            "en": "Convert video to audio",
        },
        "select_resolution": {
            "es": "Selecciona la resolución deseada",
            "en": "Select the desired resolution",
        },
        "select_compression": {
            "es": "Selecciona el nivel de compresión",
            "en": "Select the compression level",
        },
        "compression_low": {
            "es": "Bajo (mejor calidad, archivo más grande)",
            "en": "Low (better quality, larger file)",
        },
        "compression_medium": {
            "es": "Medio (calidad equilibrada)",
            "en": "Medium (balanced quality)",
        },
        "compression_high": {
            "es": "Alto (menor calidad, archivo más pequeño)",
            "en": "High (lower quality, smaller file)",
        },
        "select_audio_format": {
            "es": "Selecciona el formato de audio",
            "en": "Select the audio format",
        },
    }
    return texts[text_key][lang]


# Función para cambiar la resolución de un video / Function to change video resolution
def change_video_resolution(uploaded_file, target_resolution, session_id, lang):
    if not MOVIEPY_AVAILABLE:
        return "Error: La biblioteca moviepy no está disponible", ""

    file_name_without_extension = os.path.splitext(uploaded_file.name)[0]
    file_extension = os.path.splitext(uploaded_file.name)[1]
    temp_dir = f"/tmp/{session_id}"
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, uploaded_file.name)

    try:
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    except Exception as e:
        return get_text("error_file_write", lang), str(e)

    # Definir el nuevo nombre de archivo con la resolución
    output_file_name = (
        f"{file_name_without_extension}_{target_resolution}{file_extension}"
    )
    output_file_path = os.path.join(temp_dir, output_file_name)

    # Extraer dimensiones de la resolución (formato: 1920x1080)
    width, height = map(int, target_resolution.split("x"))

    try:
        # Cargar el video y cambiar su resolución
        video = VideoFileClip(temp_file_path)
        resized_video = video.resize(newsize=(width, height))
        resized_video.write_videofile(output_file_path, codec="libx264")
        video.close()
        resized_video.close()
    except Exception as e:
        return get_text("error_cmd_execution", lang), str(e)

    return get_text("file_processed_success", lang), output_file_path


# Función para comprimir un video / Function to compress video
def compress_video(uploaded_file, compression_level, session_id, lang):
    file_name_without_extension = os.path.splitext(uploaded_file.name)[0]
    file_extension = os.path.splitext(uploaded_file.name)[1]
    temp_dir = f"/tmp/{session_id}"
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, uploaded_file.name)

    try:
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    except Exception as e:
        return get_text("error_file_write", lang), str(e)

    # Definir el nuevo nombre de archivo comprimido
    output_file_name = f"{file_name_without_extension}_compressed{file_extension}"
    output_file_path = os.path.join(temp_dir, output_file_name)

    # Configurar parámetros de compresión según el nivel
    if compression_level == "bajo":
        bitrate = "2000k"
    elif compression_level == "medio":
        bitrate = "1000k"
    else:  # alto
        bitrate = "500k"

    try:
        # Usar FFmpeg para comprimir el video
        cmd = f'ffmpeg -i "{temp_file_path}" -b:v {bitrate} -bufsize {bitrate} "{output_file_path}"'
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        return get_text("error_cmd_execution", lang), str(e)

    return get_text("file_processed_success", lang), output_file_path


# Función para procesar el archivo / Function to process the file
def process_file(uploaded_file, model_choice, language_code, session_id, lang):
    file_name_without_extension = os.path.splitext(uploaded_file.name)[0]
    temp_dir = f"/tmp/{session_id}"
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, file_name_without_extension)

    try:
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    except Exception as e:
        return get_text("error_file_write", lang), str(e)

    cmd = (
        f'whisper "{temp_file_path}" --model {model_choice} --language {language_code}'
    )
    try:
        subprocess.run(cmd, shell=True, check=True, cwd=temp_dir)
    except subprocess.CalledProcessError as e:
        return get_text("error_cmd_execution", lang), str(e)

    zip_file_name = f"{temp_file_path}.zip"
    try:
        with zipfile.ZipFile(zip_file_name, "w") as zipf:
            for ext in ["json", "srt", "tsv", "txt", "vtt"]:
                file_to_zip = f"{temp_file_path}.{ext}"
                if os.path.exists(file_to_zip):
                    zipf.write(file_to_zip, arcname=os.path.basename(file_to_zip))
    except Exception as e:
        return get_text("error_file_zip", lang), str(e)

    return get_text("file_processed_success", lang), zip_file_name


# Función para eliminar el directorio temporal / Function to cleanup the temporary directory
def cleanup(temp_dir, retries=5, delay=1):
    """Intenta eliminar el directorio temporal con reintentos.

    Args:
        temp_dir (str): La ruta del directorio temporal a eliminar.
        retries (int): Número de reintentos para eliminar el directorio.
        delay (int): Tiempo de espera entre reintentos en segundos.
    """
    for i in range(retries):
        try:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                print(f"El directorio temporal {temp_dir} ha sido eliminado.")
                break
        except PermissionError as e:
            print(
                f"No se puede eliminar {temp_dir} porque está en uso. Reintentando..."
            )
            time.sleep(delay)
    else:
        print(
            f"No se pudo eliminar el directorio temporal {temp_dir} después de {retries} reintentos."
        )


# Configuración de Streamlit / Streamlit configuration
def set_streamlit_config(lang):
    # st.set_page_config(page_title=get_text("title", lang), initial_sidebar_state='collapsed')
    st.title(get_text("title", lang))
    st.write(get_text("agent_description", lang))


# Configuración de la barra lateral / Sidebar configuration
def sidebar_config():
    language_choice = st.sidebar.selectbox(
        "Select the language / Selecciona el idioma", ("Español", "English")
    )
    lang = "en" if language_choice == "English" else "es"
    st.session_state["lang"] = lang

    model_choice = st.sidebar.selectbox(
        get_text("select_model", lang), ("small", "base", "tiny")
    )
    return lang, model_choice


# Función para convertir video para reproductores de carro / Function to convert video for car players
def convert_video_for_car(uploaded_file, session_id, lang):
    file_name_without_extension = os.path.splitext(uploaded_file.name)[0]
    file_extension = os.path.splitext(uploaded_file.name)[1]
    temp_dir = f"/tmp/{session_id}"
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, uploaded_file.name)

    try:
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    except Exception as e:
        return get_text("error_file_write", lang), str(e)

    # Definir el nuevo nombre de archivo compatible con reproductores de carro
    output_file_name = f"{file_name_without_extension}_car_compatible{file_extension}"
    output_file_path = os.path.join(temp_dir, output_file_name)

    try:
        # Convertir el video a H.264 con resolución 1080p y framerate 25fps
        cmd = f'ffmpeg -i "{temp_file_path}" -c:v libx264 -profile:v high -level:v 4.0 -preset medium -crf 23 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" -r 25 -c:a aac -b:a 128k "{output_file_path}"'
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        return get_text("error_cmd_execution", lang), str(e)

    return get_text("file_processed_success", lang), output_file_path


# Función para procesar un directorio de videos y convertirlos para reproductores de carro
def batch_convert_videos_for_car(input_dir, output_dir, lang):
    # Verificar que los directorios existan
    if not os.path.exists(input_dir):
        return f"El directorio de entrada {input_dir} no existe"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Obtener todos los archivos de video en el directorio de entrada
    video_files = [
        f
        for f in os.listdir(input_dir)
        if f.endswith((".mp4", ".mkv", ".avi", ".mov", ".webm"))
    ]

    results = []
    for video_file in video_files:
        input_path = os.path.join(input_dir, video_file)
        file_name_without_extension = os.path.splitext(video_file)[0]
        output_path = os.path.join(
            output_dir, f"{file_name_without_extension}_car_compatible.mp4"
        )

        # Verificar si el archivo ya existe en el directorio de salida
        if os.path.exists(output_path):
            results.append(f"{video_file}: Ya convertido anteriormente")
            continue

        try:
            # Verificar si el video ya está en formato H.264
            probe_cmd = f'ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 "{input_path}"'
            codec = (
                subprocess.check_output(probe_cmd, shell=True).decode("utf-8").strip()
            )

            if codec == "h264":
                # Verificar la resolución
                resolution_cmd = f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "{input_path}"'
                resolution = (
                    subprocess.check_output(resolution_cmd, shell=True)
                    .decode("utf-8")
                    .strip()
                )
                width, height = map(int, resolution.split("x"))

                if width <= 1920 and height <= 1080:
                    # El video ya es compatible, solo copiarlo
                    shutil.copy2(input_path, output_path)
                    results.append(f"{video_file}: Ya compatible, copiado")
                    continue

            # Convertir el video a H.264 con resolución 1080p y framerate 25fps
            cmd = f'ffmpeg -i "{input_path}" -c:v libx264 -profile:v high -level:v 4.0 -preset medium -crf 23 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" -r 25 -c:a aac -b:a 128k "{output_path}"'
            subprocess.run(cmd, shell=True, check=True)
            results.append(f"{video_file}: Convertido exitosamente")
        except Exception as e:
            results.append(f"{video_file}: Error - {str(e)}")

    return "\n".join(results)


# Función para convertir video a audio / Function to convert video to audio
def convert_video_to_audio(uploaded_file, output_format, session_id, lang):
    if not MOVIEPY_AVAILABLE:
        return "Error: La biblioteca moviepy no está disponible", ""

    file_name_without_extension = os.path.splitext(uploaded_file.name)[0]
    temp_dir = f"/tmp/{session_id}"
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, uploaded_file.name)

    try:
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    except Exception as e:
        return get_text("error_file_write", lang), str(e)

    # Definir el nuevo nombre de archivo de audio
    output_file_name = f"{file_name_without_extension}.{output_format}"
    output_file_path = os.path.join(temp_dir, output_file_name)

    try:
        # Cargar el video y extraer el audio
        video = VideoFileClip(temp_file_path)

        if output_format == "mp3":
            video.audio.write_audiofile(output_file_path)
        elif output_format == "wav":
            video.audio.write_audiofile(output_file_path, codec="pcm_s16le")
        elif output_format == "ogg":
            video.audio.write_audiofile(output_file_path, codec="libvorbis")

        video.close()
    except Exception as e:
        return get_text("error_cmd_execution", lang), str(e)

    return get_text("file_processed_success", lang), output_file_path


# Función principal / Main function
def main():
    # Inicializar las claves de estado de sesión si no existen
    if "cleanup_flag" not in st.session_state:
        st.session_state["cleanup_flag"] = False
    if "lang" not in st.session_state:
        st.session_state["lang"] = "es"
    if "session_id" not in st.session_state:
        st.session_state["session_id"] = str(uuid.uuid4())
    if "task" not in st.session_state:
        st.session_state["task"] = "transcribe"

    # Configuración de la barra lateral para seleccionar el idioma y modelo
    lang, model_choice = sidebar_config()

    # Actualización del título y la descripción según el idioma seleccionado
    st.title(get_text("title", lang))
    st.write(get_text("agent_description", lang))

    # Selección de tarea en la barra lateral
    task = st.sidebar.radio(
        get_text("select_task", lang),
        [
            "transcribe",
            "change_resolution",
            "compress_video",
            "convert_to_audio",
            "convert_for_car",
        ],
        format_func=lambda x: get_text(f"task_{x}", lang),
    )
    st.session_state["task"] = task

    # Agregar footer a la barra lateral / Add footer to the sidebar
    st.sidebar.markdown("---")  # Agrega una línea divisoria / Add a divider
    st.sidebar.subheader(get_text("created_by", lang))
    st.sidebar.markdown(
        "Alexander Oviedo Fadul\n"
        "[GitHub](https://github.com/bladealex9848) | "
        "[Website](https://alexander.oviedo.isabellaea.com/) | "
        "[Instagram](https://www.instagram.com/alexander.oviedo.fadul) | "
        "[Twitter](https://twitter.com/alexanderofadul) | "
        "[Facebook](https://www.facebook.com/alexanderof/) | "
        "[WhatsApp](https://api.whatsapp.com/send?phone=573015930519&text=Hola%20!Quiero%20conversar%20contigo!%20)"
    )

    # Campo para subir el archivo / Field to upload the file
    st.write(get_text("upload_file", lang))

    # Definir tipos de archivo según la tarea seleccionada
    if task == "transcribe":
        file_types = [
            "mp3",
            "wav",
            "flac",
            "m4a",
            "wma",
            "aac",
            "ogg",
            "ac3",
            "aiff",
            "amr",
            "au",
            "mka",
            "opus",
            "ra",
            "dts",
            "mp4",
            "mkv",
            "flv",
            "avi",
            "mov",
            "wmv",
            "3gp",
            "webm",
            "mpg",
            "m2v",
            "m4v",
            "3g2",
            "asf",
            "f4v",
            "mpe",
            "ts",
            "vob",
            "mpeg",
        ]
    elif task in ["change_resolution", "compress_video", "convert_for_car"]:
        file_types = [
            "mp4",
            "mkv",
            "flv",
            "avi",
            "mov",
            "wmv",
            "3gp",
            "webm",
            "mpg",
            "m2v",
            "m4v",
            "3g2",
            "asf",
            "f4v",
            "mpe",
            "ts",
            "vob",
            "mpeg",
        ]
    elif task == "convert_to_audio":
        file_types = [
            "mp4",
            "mkv",
            "flv",
            "avi",
            "mov",
            "wmv",
            "3gp",
            "webm",
            "mpg",
            "m2v",
            "m4v",
            "3g2",
            "asf",
            "f4v",
            "mpe",
            "ts",
            "vob",
            "mpeg",
        ]

    uploaded_file = st.file_uploader(
        get_text("choose_file", lang),
        type=file_types,
        accept_multiple_files=False,
    )

    if uploaded_file:
        st.session_state["cleanup_flag"] = True
        st.write(get_text("file_uploaded", lang), uploaded_file.name)

        # Opciones específicas para cada tarea
        if task == "change_resolution":
            # Opciones de resolución para videos
            resolution = st.selectbox(
                get_text("select_resolution", lang),
                ["1920x1080", "1280x720", "854x480", "640x360", "426x240"],
            )

            if st.button(get_text("process", lang)):
                message, output_file_or_error = change_video_resolution(
                    uploaded_file, resolution, st.session_state["session_id"], lang
                )
                if message == get_text("file_processed_success", lang):
                    with open(output_file_or_error, "rb") as f:
                        file_bytes = io.BytesIO(f.read())
                        st.download_button(
                            get_text("download_file", lang),
                            file_bytes,
                            file_name=os.path.basename(output_file_or_error),
                        )
                else:
                    st.error(f"{message}: {output_file_or_error}")
                    cleanup(os.path.dirname(output_file_or_error))

        elif task == "compress_video":
            # Opciones de compresión para videos
            compression_level = st.selectbox(
                get_text("select_compression", lang),
                ["bajo", "medio", "alto"],
                format_func=lambda x: (
                    get_text(f"compression_{x}", lang)
                    if x in ["bajo", "medio", "alto"]
                    else x
                ),
            )

            if st.button(get_text("process", lang)):
                message, output_file_or_error = compress_video(
                    uploaded_file,
                    compression_level,
                    st.session_state["session_id"],
                    lang,
                )
                if message == get_text("file_processed_success", lang):
                    with open(output_file_or_error, "rb") as f:
                        file_bytes = io.BytesIO(f.read())
                        st.download_button(
                            get_text("download_file", lang),
                            file_bytes,
                            file_name=os.path.basename(output_file_or_error),
                        )
                else:
                    st.error(f"{message}: {output_file_or_error}")
                    cleanup(os.path.dirname(output_file_or_error))

        elif task == "convert_to_audio":
            # Opciones de formato de audio
            audio_format = st.selectbox(
                get_text("select_audio_format", lang), ["mp3", "wav", "ogg"]
            )

            if st.button(get_text("process", lang)):
                message, output_file_or_error = convert_video_to_audio(
                    uploaded_file, audio_format, st.session_state["session_id"], lang
                )
                if message == get_text("file_processed_success", lang):
                    with open(output_file_or_error, "rb") as f:
                        file_bytes = io.BytesIO(f.read())
                        st.download_button(
                            get_text("download_file", lang),
                            file_bytes,
                            file_name=os.path.basename(output_file_or_error),
                        )
                else:
                    st.error(f"{message}: {output_file_or_error}")
                    cleanup(os.path.dirname(output_file_or_error))

        elif task == "convert_for_car":
            # Opción para convertir video para reproductores de carro
            st.info(
                "Esta opción convertirá el video a formato H.264 con resolución 1080p y 25fps, compatible con la mayoría de reproductores de carro."
            )

            if st.button(get_text("process", lang)):
                message, output_file_or_error = convert_video_for_car(
                    uploaded_file, st.session_state["session_id"], lang
                )
                if message == get_text("file_processed_success", lang):
                    with open(output_file_or_error, "rb") as f:
                        file_bytes = io.BytesIO(f.read())
                        st.download_button(
                            get_text("download_file", lang),
                            file_bytes,
                            file_name=os.path.basename(output_file_or_error),
                        )
                else:
                    st.error(f"{message}: {output_file_or_error}")
                    cleanup(os.path.dirname(output_file_or_error))

            # Opción para procesar todos los videos en el directorio
            st.markdown("---")
            st.subheader("Procesar directorio completo")
            st.info(
                "Esta opción convertirá todos los videos en el directorio 'videos_originales' y guardará los resultados en 'videos_convertidos'."
            )

            if st.button("Procesar todos los videos"):
                with st.spinner(
                    "Procesando videos... Esto puede tardar varios minutos."
                ):
                    results = batch_convert_videos_for_car(
                        "videos_originales", "videos_convertidos", lang
                    )
                    st.success("Procesamiento completado")
                    st.text_area("Resultados", results, height=300)

        elif task == "transcribe":
            if st.button(get_text("process", lang)):
                message, output_file_or_error = process_file(
                    uploaded_file,
                    model_choice,
                    lang,
                    st.session_state["session_id"],
                    lang,
                )
                if message == get_text("file_processed_success", lang):
                    with open(output_file_or_error, "rb") as f:
                        zip_bytes = io.BytesIO(f.read())
                        st.download_button(
                            get_text("download_zip", lang),
                            zip_bytes,
                            file_name=os.path.basename(output_file_or_error),
                        )
                else:
                    st.error(f"{message}: {output_file_or_error}")
                    cleanup(os.path.dirname(output_file_or_error))
    else:
        # Limpieza condicional de archivos temporales
        if st.session_state["cleanup_flag"]:
            temp_dir = f"/tmp/{st.session_state['session_id']}"
            cleanup(temp_dir)
            st.session_state["cleanup_flag"] = False


# Ejecutar la aplicación
if __name__ == "__main__":
    main()
