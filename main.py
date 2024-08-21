import os
import random

from api import get_videos_from_youtube
from converter import convert_to_mp3, download_video
from globals import NUM_OF_VIDEOS_TO_DOWNLOAD


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

    mp3_files = []
    for video in videos:
        # Descarga el video usando yt-dlp con subprocess
        downloaded_video = download_video(video)
        if downloaded_video is None:
            continue

        mp3_file = convert_to_mp3(downloaded_video)
        if mp3_file is None:
            continue

        mp3_files.append(mp3_file)

    downloaded_audios = os.listdir("media")
    if len(downloaded_audios) < NUM_OF_VIDEOS_TO_DOWNLOAD:
        print("Buscando más videos...")
        main()

    return mp3_files


if __name__ == "__main__":
    main()
