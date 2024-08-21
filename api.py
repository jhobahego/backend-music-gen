import re

import googleapiclient.discovery
from googleapiclient.errors import HttpError
from decouple import config

from schemas.youtube_result import YoutubeResult


def get_videos_from_youtube(keyword: str) -> list[YoutubeResult]:
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = config("API_KEY")

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY
    )

    response = {
        "items": [],
    }
    try:
        request = youtube.search().list(
            part="snippet",
            maxResults=20,
            q=keyword,
        )
        response = request.execute()
    except HttpError as e:
        if e.status_code == 403:
            print("Se excedió el límite de la API")
            return []

    if not response["items"]:
        print("No se encontraron videos")
        return []

    youtube_videos = []
    for item in response["items"]:
        is_video = (
            item["id"]["kind"] == "youtube#video"
            and item["snippet"]["liveBroadcastContent"] == "none"
        )
        if not is_video:
            continue

        video_id = item["id"]["videoId"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        try:
            request_video = youtube.videos().list(
                part="snippet,contentDetails", id=video_id
            )
        except Exception as e:
            print(f"Error ln59: {e}")
            continue

        raw_response_video = request_video.execute()
        if not raw_response_video["items"]:
            print(f"No se encontró información del video: {video_url}")
            continue

        response_video = raw_response_video["items"][0]
        duration = response_video["contentDetails"]["duration"]
        if str(duration).__contains__("H"):
            print(f"El video es muy largo: {duration}")
            continue

        minutes = 0
        seconds = 0
        try:
            match = re.match(r"PT(\d+)M(\d+)S", duration)
            minutes = int(match.group(1))
            seconds = int(match.group(2))
        except AttributeError:
            print(f"El video es muy largo: {duration}")
            continue

        if minutes > 5 or (minutes == 5 and seconds > 40):
            print(f"El video es muy largo: {minutes} min: {seconds}seg")
            continue

        youtube_result = YoutubeResult(
            url=video_url,
            title=response_video["snippet"]["title"],
            description=response_video["snippet"]["description"],
        )
        youtube_videos.append(youtube_result)

    return youtube_videos
