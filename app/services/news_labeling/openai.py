import openai
from typing import Literal
from pydantic import BaseModel, Field

from .base import LabelingService, NewsData, LabeledNewsData


class NewsAnalysisResponse(BaseModel):
    predicted_genre: str = Field(description="The most appropriate genre from the provided list")
    predicted_sentiment: Literal["positive", "negative", "neutral"] = Field(
        description="The sentiment of the news article"
    )


class OpenAILabelingService(LabelingService):
    system_prompt: str = "You are a news article analyzer."

    def __init__(
        self, 
        model_name: str,
        openai_api_key: str
    ):
        self.model_name = model_name
        self.openai_api_key = openai_api_key
        self.client = openai.AsyncOpenAI(api_key=self.openai_api_key)

    async def label(self, news_data: NewsData) -> LabeledNewsData:
        prompt = (
            f"Analyze the following news article for the company '{news_data.company_name}':\n\n"
            f"{news_data.text}\n\n"
            f"Available genres: {', '.join(news_data.genre_list)}\n\n"
            "Please determine the most appropriate genre from the list above, and classify the overall sentiment "
            "of the article as one of the following: positive, negative, or neutral.\n"
            "Return your analysis in the following JSON format:\n"
            "{\n"
            '    "predicted_genre": "<genre>",\n'
            '    "predicted_sentiment": "<sentiment>"\n'
            "}\n"
            "Ensure that the JSON response is valid and parsable."
        )
        response = await self.client.beta.chat.completions.parse(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            response_model=NewsAnalysisResponse
        )
        message = response.choices[0].message

        return LabeledNewsData(
            text=news_data.text,
            company_name=news_data.company_name,
            predicted_genre=message.parsed.predicted_genre,
            predicted_sentiment=message.parsed.predicted_sentiment
        )


