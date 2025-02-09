from app.workers.base_worker import BaseLabelingWorker
from app.schemas import LabelingRequest, LabelingResponse
from app.services.news_labeling import OpenAILabelingService, NewsData


class OpenAILabelingWorker(BaseLabelingWorker):
    service_name = "openai_news_labeling_worker"

    def __init__(self, model_name: str, openai_api_key: str):
        super().__init__()
        self.model_name = model_name
        self.openai_api_key = openai_api_key
        self.labeling_service = OpenAILabelingService(
            model_name=model_name, 
            openai_api_key=openai_api_key
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
