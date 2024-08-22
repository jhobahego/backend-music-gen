import os

import yt_dlp
from pydub import AudioSegment

from schemas.youtube_result import YoutubeResult
from globals import NUM_OF_VIDEOS_TO_DOWNLOAD


def convert_to_mp3(video_file) -> str | None:
    _, ext = os.path.splitext(video_file)
    if ext != ".mp4":
        print("Formato de archivo no soportado")
        return None

    # Convierte el archivo descargado a mp3 usando pydub
    base, ext = os.path.splitext(video_file)
    mp3_file = base + ".mp3"
    if ext == ".mp4":
        audio = AudioSegment.from_file(video_file)
        audio.export(mp3_file, format="mp3")

    # Opcional: elimina el archivo de video después de la conversión
    os.remove(video_file)

    if os.path.exists(mp3_file):
        if os.path.isfile(mp3_file) and mp3_file.endswith(".mp3"):
            print(f"Archivo mp3 creado: {os.path.basename(mp3_file)}")
        else:
            print("Error: el archivo convertido no es un mp3")
            return None

    return mp3_file


def download_video(video: YoutubeResult) -> str | None:
    downloaded_audios = os.listdir("media")
    if len(downloaded_audios) == NUM_OF_VIDEOS_TO_DOWNLOAD:
        return

    ruta_actual: str = os.path.join(os.getcwd(), "media")
    goal_file = os.path.join(ruta_actual, video.title) + ".mp3"

    if os.path.exists(goal_file):
        print(f"El video ya existe: {video.title}")
        return None

    ydl_opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
        "outtmpl": f"{ruta_actual}/%(title)s.%(ext)s",
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video.url])
    except Exception as e:
        print(f"Error al descargar el video: {e}")
        return None

    return goal_file
