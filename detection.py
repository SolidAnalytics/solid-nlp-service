from __future__ import annotations
import httpx
import asyncio
from openai import OpenAI
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv, find_dotenv
from os import getenv
import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq.middleware.asyncio import AsyncIO
from logging_config import setup_logging
import logging
import inspect




load_dotenv()
setup_logging()

# .env
OPENAI_API_KEY = getenv("OPENAI_API_KEY")
proxy_url = getenv('OPENAI_PROXY_URL')  
RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"

http_client = httpx.Client(proxy=proxy_url)
client = OpenAI(api_key=OPENAI_API_KEY, http_client=http_client)


# RabbitMQ
rabbitmq_broker = RabbitmqBroker(url=RABBITMQ_URL) 
rabbitmq_broker.add_middleware(AsyncIO()) 
dramatiq.set_broker(rabbitmq_broker)

class ResearchPaperExtraction(BaseModel):
    matching_entity: bool
    genre: str
    sentiment: str

completion = "2123rfa"


# input
entity = "Blue Origin"
sentiment_values = ["positive", "neutral", "negative"]
genre_values = ["article", "news", "ad"]
post = """
Blue Origin впервые запустила ракету на орбиту, но не смогла приземлить разгонный блок
            Космическая компания Джеффа Безоса Blue Origin впервые совершила успешный запуск ракеты на орбиту. Утром в четверг ее аппарат New Glenn стартовал с космодрома во Флориде и вышел в космос.
            Однако Blue Origin не удалось посадить на океанскую платформу свой разгонный блок, компания сообщила, что после отделения от ракеты он был потерян.
            Запуск ракеты New Glenn должен был состояться еще в понедельник, но был отложен по техническим причинам.
            Безос, главный бизнес которого — компания Amazon, стремится конкурировать на рынке частных космических перевозок с Илоном Маском и его SpaceX. Последняя постоянно запускает ракеты в космос и стала главным партнером американского космического агентства НАСА по доставке грузов на Международную космическую станцию.
            SpaceX также постоянно совершает посадку своих разгонных блоков на водную платформу: это позволяет снова использовать их после перезаправки и таким образом значительно снижает стоимость запусков.
            Blue Origin начинала одновременно со Space X и, хотя и совершила 27 успешных запусков, до этого ни разу не выводила корабли на орбиту.
            Впрочем, ракета New Glenn не только достаточно мощна для того, чтобы выйти на околоземную орбиту (она более чем вдвое мощнее ракеты Falcon 9 от SpaceX), но и потенциально способна отправиться на Луну.
"""

async def fetch_completion(post: str, entity: str) -> ResearchPaperExtraction:
    global completion
    logging.info(f"Fetching completion for entity: {entity}")
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": f"""
                Post content:
                {post}
                Instruction:
                Check if "{entity}" is mentioned as a company in the text. If it is, determine the genre of the post and its sentiment regarding {entity}.
                Return the following structure:
                matching_entity: (a boolean value (True or False) indicating whether "{entity}" is used here as a company)
                genre: (one of these values: {genre_values}; if none matches, use "unknown")
                sentiment: (one of these values: {sentiment_values})
                """
            }
            
        ],
        
        response_format=ResearchPaperExtraction,
        
    )
    response = completion.choices[0].message.parsed  
    logging.info(f"Received response for entity: {entity}")    
    return completion, response


@dramatiq.actor
async def coro():
    await fetch_completion(post, entity)
    return completion

async def main():  
    logging.info("Starting main process...")  # Логирование начала процесса
    await fetch_completion(post, entity)
    coro.send()
    genre = completion.choices[0].message.parsed.genre
    sentiment = completion.choices[0].message.parsed.sentiment
    matching_entity = completion.choices[0].message.parsed.matching_entity
    # a wheelchair 
    if matching_entity:
        logging.info(f"Entity found: {entity}")  # Логирование, если сущность найдена
        print("--- Post details ---")
        print(f"Entity: {entity}")
        print(f"Matching Entity: {matching_entity}")
        print(f"Genre: {genre}")
        print(f"Sentiment: {sentiment}")
        
    else:
        logging.warning(f"The entity '{entity}' was not found in the post.")  # Логирование, если сущность не найдена
        print(f"The entity '{entity}' was not found in the post.")

#inspect.iscoroutinefunction(main())
#inspect.iscoroutinefunction(fetch_completion(post, entity))
#inspect.iscoroutinefunction(response_1())


print(inspect.iscoroutinefunction(main))  # returns True if coroutine
print(inspect.iscoroutinefunction(coro))
if __name__ == "__main__":
    asyncio.run(main())
