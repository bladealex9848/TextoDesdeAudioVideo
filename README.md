# TranscriptorAV: Suite de Procesamiento de Audio y Video

TranscriptorAV es una suite completa de procesamiento de audio y video desarrollada con Streamlit. Ofrece múltiples funcionalidades para trabajar con archivos multimedia, desde transcripción de audio hasta compresión y cambio de resolución de videos.

## Configuración

Para ejecutar este proyecto, instale las dependencias usando pip:

```bash
pip install -r requirements.txt
```

Asegúrese de tener instalado FFmpeg en su sistema, ya que es necesario para el procesamiento de video:

### En macOS (usando Homebrew):
```bash
brew install ffmpeg
```

### En Ubuntu/Debian:
```bash
sudo apt update && sudo apt install ffmpeg
```

### En Windows:
Descargue FFmpeg desde [ffmpeg.org](https://ffmpeg.org/download.html) y añádalo al PATH del sistema.

## Uso

### Interfaz gráfica con Streamlit

Para iniciar la aplicación con interfaz gráfica, ejecute:

```bash
streamlit run TranscriptorAV.py
```

### Línea de comandos

También puede usar la herramienta desde la línea de comandos:

```bash
# Transcribir un archivo de audio/video
python textodesdeaudiovideo.py --mode transcribe --input archivo.mp4 --model small

# Convertir un video para reproductores de carro
python textodesdeaudiovideo.py --mode convert-car --input video.mp4

# Procesar todos los videos en el directorio videos_originales
python textodesdeaudiovideo.py --mode batch-convert-car

# Modo interactivo
python textodesdeaudiovideo.py
```

### Estructura de directorios

El proyecto utiliza la siguiente estructura de directorios:

- `videos_originales/`: Coloque aquí los videos originales que desea procesar
- `videos_convertidos/`: Aquí se guardarán los videos convertidos para reproductores de carro


## Características

### Transcripción de Audio y Video
- Subida de archivos de audio y video para transcripción.
- Transcripción automática usando Whisper de OpenAI.
- Descarga de transcripciones en múltiples formatos (txt, srt, vtt, json, tsv).

### Procesamiento de Video
- Cambio de resolución de videos (1080p, 720p, 480p, 360p, 240p).
- Compresión de videos con diferentes niveles de calidad.
- Conversión de videos a formatos de audio (mp3, wav, ogg).
- **Conversión de videos para reproductores de carro** (H.264, 1080p, 25fps).
- Procesamiento por lotes de videos para compatibilidad con reproductores de carro.

### Interfaz de Usuario
- Interfaz intuitiva y fácil de usar con Streamlit.
- Soporte para múltiples idiomas (Español e Inglés).
- Organización por tareas para un flujo de trabajo eficiente.
- Opción para procesar directorios completos de videos.

## Contribución

Las contribuciones son bienvenidas. Si desea contribuir al proyecto, por favor, forkee el repositorio y haga una solicitud de extracción con sus cambios.

## Licencia

Este proyecto está bajo una licencia MIT. Vea el archivo LICENSE para más detalles.