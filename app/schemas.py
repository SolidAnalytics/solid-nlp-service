from pydantic import BaseModel

from app.services.news_labeling.base import NEWS_SENTIMENTS


class LabelingRequest(BaseModel):
    global_post_id: int
    post_text: str
    entity: str
    genre_list: list[str]


class LabelingResponse(BaseModel):
    global_post_id: int
    entity: str
    genre: str
    sentiment: NEWS_SENTIMENTS
    is_entity_presented: bool
