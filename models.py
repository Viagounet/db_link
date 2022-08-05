import datetime
from dataclasses import dataclass

from link import Link


@dataclass
class AnimeRecommendation(Link):
    title: str
    story: str
    mal_score: float
    similarity_score: float
    global_score: float


@dataclass
class StoryRequest(Link):
    story: str
    recommendations: list[AnimeRecommendation]
    date: datetime.datetime