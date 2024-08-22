import os
import random
import multiprocessing
from concurrent.futures import ThreadPoolExecutor

from api import get_videos_from_youtube
from converter import convert_to_mp3, download_video
from globals import NUM_OF_VIDEOS_TO_DOWNLOAD


def process_video(video):
    try:
        mp4_file = download_video(video)
        if mp4_file:
            return convert_to_mp3(mp4_file)
    except Exception as e:
        print(f"Error processing video {video.title}: {e}")
    return None


def main():
    keywords = [
        "canción+de+farid+ortiz",
        "musica+de+farid+ortiz",
        "farid+ortiz",
        "canción+de+diomedes",
        "musica+de+diomedes",
    ]

    keyword = random.choice(keywords)

    videos = get_videos_from_youtube(keyword)
    if len(videos) == 0:
        print("No se encontraron videos en YouTube :(")
        return

    # Limita la cantidad de videos a descargar
    videos = videos[:NUM_OF_VIDEOS_TO_DOWNLOAD]

    max_workers = min(multiprocessing.cpu_count(), len(videos))
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        mp3_files = list(filter(None, executor.map(process_video, videos)))

    downloaded_audios = os.listdir("media")
    if len(downloaded_audios) < NUM_OF_VIDEOS_TO_DOWNLOAD:
        print("Buscando más videos...")
        main()

    return mp3_files


if __name__ == "__main__":
    main()
