from app.workers.base_worker import BaseLabelingWorker
from app.schemas import LabelingRequest, LabelingResponse
from app.services.news_labeling import OpenAILabelingService, NewsData
import app.config as config


class OpenAIWorker(BaseLabelingWorker):
    service_name = "openai_news_labeling_worker"
    queue_name = "labeling_worker_queue"
    actor_name = "labeling_worker"

    def __init__(self):
        self.labeling_service = OpenAILabelingService(
            model_name=config.OPENAI_MODEL_NAME, 
            openai_api_key=config.OPENAI_API_KEY
        )

    async def process(self, data: LabelingRequest) -> LabelingResponse:
        news_data = NewsData(
            text=data.post_text,
            company_name=data.entity,
            genre_list=data.genre_list
        )

        labeled_news = await self.labeling_service.label(news_data)

        return LabelingResponse(
            global_post_id=data.global_post_id,
            entity=data.entity,
            genre=labeled_news.predicted_genre,
            sentiment=labeled_news.predicted_sentiment
        )
