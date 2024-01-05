import os
import streamlit as st
from PIL import Image
import subprocess
import zipfile
import io
import shutil
import uuid
import time

# Configuración de Streamlit / Streamlit Configuration
st.set_page_config(
    page_title="TranscriptorAV: Tu asistente para transcripciones de audio y video",
    page_icon="🎙️",
    initial_sidebar_state='collapsed',
    menu_items={
        'Get Help': 'https://www.isabellaea.com',  # Actualiza con tu URL de ayuda si es necesario
        'Report a bug': None,  # Puedes agregar un enlace para reportar errores si lo deseas
        'About': ("TranscriptorAV es una herramienta avanzada para la transcripción automática "
                  "de archivos de audio y video. Utiliza modelos de aprendizaje profundo para "
                  "convertir con precisión contenido multimedia en texto, facilitando la accesibilidad y "
                  "la comprensión del contenido. Esta herramienta es ideal para periodistas, estudiantes, "
                  "profesionales de medios y cualquier persona que necesite transcribir contenido multimedia.")
    }
)

# Carga y muestra el logo de la aplicación / Load and show the application logo
logo = Image.open('img/logo.png')
st.image(logo, width=250)

# Funciones de internacionalización y manejo de errores / Internationalization and error handling functions
def get_text(text_key, lang):
    texts = {
        "title": {
            "es": "TranscriptorAV: Tu asistente para transcripciones de audio y video",
            "en": "TranscriptorAV: Your assistant for audio and video transcriptions"
        },
        "select_language": {
            "es": "Selecciona el idioma",
            "en": "Select the language"
        },
        "select_model": {
            "es": "Selecciona el modelo de Whisper",
            "en": "Select the Whisper model"
        },
        "upload_file": {
            "es": "Sube tu archivo de audio o video.",
            "en": "Upload your audio or video file."
        },
        "choose_file": {
            "es": "Elige un archivo",
            "en": "Choose a file"
        },
        "file_uploaded": {
            "es": "Archivo cargado: ",
            "en": "File uploaded: "
        },
        "process": {
            "es": "Procesar",
            "en": "Process"
        },
        "download_zip": {
            "es": "Descargar archivo comprimido",
            "en": "Download compressed file"
        },
        "error_file_write": {
            "es": "Error al escribir el archivo en el servidor.",
            "en": "Error writing the file to the server."
        },
        "error_cmd_execution": {
            "es": "Error al ejecutar el comando.",
            "en": "Error executing command."
        },
        "error_file_zip": {
            "es": "Error al comprimir los archivos.",
            "en": "Error compressing the files."
        },
        "error_file_cleanup": {
            "es": "Error al limpiar los archivos temporales.",
            "en": "Error cleaning up temporary files."
        },
        "file_processed_success": {
            "es": "Archivo procesado exitosamente.",
            "en": "File successfully processed."
        },
        "created_by": {
            "es": "Creado por:",
            "en": "Created by:"
        },
        "agent_description": {
            "es": ("TranscriptorAV es tu asistente personalizado para la transcripción automática "
                   "de archivos de audio y video. Utilizando la tecnología de aprendizaje profundo de Whisper, "
                   "TranscriptorAV puede convertir con precisión tu contenido multimedia en texto en varios formatos, "
                   "facilitando la accesibilidad y la comprensión del contenido."),
            "en": ("TranscriptorAV is your personalized assistant for automatic transcription "
                   "of audio and video files. Leveraging the deep learning technology of Whisper, "
                   "TranscriptorAV can accurately convert your multimedia content into text in various formats, "
                   "enhancing accessibility and understanding of the content.")
        }
    }
    return texts[text_key][lang]

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

    cmd = f'whisper "{temp_file_path}" --model {model_choice} --language {language_code}'
    try:
        subprocess.run(cmd, shell=True, check=True, cwd=temp_dir)
    except subprocess.CalledProcessError as e:
        return get_text("error_cmd_execution", lang), str(e)

    zip_file_name = f"{temp_file_path}.zip"
    try:
        with zipfile.ZipFile(zip_file_name, 'w') as zipf:
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
            print(f"No se puede eliminar {temp_dir} porque está en uso. Reintentando...")
            time.sleep(delay)
    else:
        print(f"No se pudo eliminar el directorio temporal {temp_dir} después de {retries} reintentos.")

# Configuración de Streamlit / Streamlit configuration
def set_streamlit_config(lang):
    #st.set_page_config(page_title=get_text("title", lang), initial_sidebar_state='collapsed')
    st.title(get_text("title", lang))
    st.write(get_text("agent_description", lang))

# Configuración de la barra lateral / Sidebar configuration
def sidebar_config():
    language_choice = st.sidebar.selectbox(
        "Select the language / Selecciona el idioma",
        ("Español", "English")
    )
    lang = 'en' if language_choice == "English" else 'es'
    st.session_state['lang'] = lang

    model_choice = st.sidebar.selectbox(
        get_text("select_model", lang),
        ("small", "base", "tiny")
    )
    return lang, model_choice

# Función principal / Main function
def main():
    # Inicializar las claves de estado de sesión si no existen
    if 'cleanup_flag' not in st.session_state:
        st.session_state['cleanup_flag'] = False
    if 'lang' not in st.session_state:
        st.session_state['lang'] = 'es'
    if 'session_id' not in st.session_state:
        st.session_state['session_id'] = str(uuid.uuid4())

    # Configuración de la barra lateral para seleccionar el idioma y modelo
    lang, model_choice = sidebar_config()

    # Actualización del título y la descripción según el idioma seleccionado
    st.title(get_text("title", lang))
    st.write(get_text("agent_description", lang))

    # Agregar footer a la barra lateral / Add footer to the sidebar
    st.sidebar.markdown('---')  # Agrega una línea divisoria / Add a divider
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
    uploaded_file = st.file_uploader(
        get_text("choose_file", lang),
        type=["mp3", "wav", "flac", "m4a", "wma", "aac", "ogg", "ac3", "aiff", "amr", "au", "mka", "opus", "ra", "dts",
               "mp4", "mkv", "flv", "avi", "mov", "wmv", "3gp", "webm", "mpg", "m2v", "m4v", "3g2", "asf", "f4v", "mpe", "ts", "vob", "mpeg"],
        accept_multiple_files=False
    )

    if uploaded_file:
        st.session_state['cleanup_flag'] = True
        st.write(get_text("file_uploaded", lang), uploaded_file.name)
        if st.button(get_text("process", lang)):
            message, output_file_or_error = process_file(uploaded_file, model_choice, lang, st.session_state['session_id'], lang)
            if message == get_text("file_processed_success", lang):
                with open(output_file_or_error, 'rb') as f:
                    zip_bytes = io.BytesIO(f.read())
                    st.download_button(get_text("download_zip", lang), zip_bytes, file_name=os.path.basename(output_file_or_error))
            else:
                st.error(f"{message}: {output_file_or_error}")
                cleanup(os.path.dirname(output_file_or_error))
    else:
        # Limpieza condicional de archivos temporales
        if st.session_state['cleanup_flag']:
            temp_dir = f"/tmp/{st.session_state['session_id']}"
            cleanup(temp_dir)
            st.session_state['cleanup_flag'] = False

# Ejecutar la aplicación
if __name__ == "__main__":
    main()