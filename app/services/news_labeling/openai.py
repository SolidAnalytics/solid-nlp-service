import openai
from typing import Literal
from pydantic import BaseModel, Field

from .base import LabelingService, NewsData, LabeledNewsData


class NewsAnalysisResponse(BaseModel):
    is_entity_presented: bool = Field(description="Whether the entity is presented in the article")
    predicted_genre: str = Field(description="The most appropriate genre from the provided list")
    predicted_sentiment: Literal["positive", "negative", "neutral"] = Field(
        description="The sentiment of the news article"
    )


class OpenAILabelingService(LabelingService):
    system_prompt: str = """You are a news article analyzer. Your task is to:
1. Check if a specific company/entity is mentioned in the text
2. Determine the journalistic genre from the list above
3. Analyze the sentiment towards the company/topic
"""

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
            f"Analyze the following text regarding the company/entity '{news_data.company_name}':\n\n"
            f"{news_data.text}\n\n"
            f"Available journalistic genres: {', '.join(news_data.genre_list)}\n\n"
            "Please analyze the following aspects:\n"
            "1. Is the company/entity explicitly mentioned in the text?\n"
            "2. What is the most appropriate journalistic genre from the list above? "
            "If the text doesn't match any of the provided genres, return 'unknown'.\n"
            "3. What is the overall sentiment (positive, negative, or neutral)?\n\n"
            "Return your analysis in the following JSON format:\n"
            "{\n"
            '    "is_entity_presented": true/false,\n'
            '    "predicted_genre": "<genre or unknown>",\n'
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
            response_format=NewsAnalysisResponse
        )
        message = response.choices[0].message

        return LabeledNewsData(
            text=news_data.text,
            company_name=news_data.company_name,
            predicted_genre=message.parsed.predicted_genre,
            predicted_sentiment=message.parsed.predicted_sentiment,
            is_entity_presented=message.parsed.is_entity_presented
        )


