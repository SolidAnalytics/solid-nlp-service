from abc import ABC, abstractmethod

from pydantic import BaseModel
from typing import Literal


NEWS_SENTIMENTS = Literal["positive", "negative", "neutral"]


class NewsData(BaseModel):
    text: str
    company_name: str
    genre_list: list[str]


class LabeledNewsData(BaseModel):
    text: str
    company_name: str
    predicted_genre: str
    predicted_sentiment: NEWS_SENTIMENTS


class LabelingService:

    @abstractmethod
    async def label(self, news_data: NewsData) -> LabeledNewsData:
        pass
