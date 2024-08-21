from pydantic import BaseModel


class YoutubeResult(BaseModel):
    url: str
    title: str
    description: str
