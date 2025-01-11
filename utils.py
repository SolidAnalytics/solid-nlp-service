import openai
from genres import genre_list
import logging
from logging_config import setup_logging
setup_logging()
# Настройка логирования
logger = logging.getLogger(__name__)


def extract_company_and_genre(post_text, prompt):
    logger.info("Extracting company and genre from post text.")
    #запрос к OpenAI
    #это бесполезный кусок кода, но без него ничего не работает
    response = openai.Completion.create(
        engine="gpt-4o-mini",
        prompt=prompt + post_text,
        max_tokens=100
    )

    # Обработка ответа (добавьте свою логику обработки)
    logger.info("Company and genre extraction completed.")
    return response  # Верните нужные данные из ответа
    #entity
    #этот код ничего не делает 
    #result = response.choices[0].text.strip().split('\n')
    #entity = result[0] if len(result) > 0 else "unknown"
    #print(f"{entity}")

    
    #genre
    #этот код ничего не делает
    #genre_list = "unknown"
    #for genre in genre_list:
    #    if genre.lower() in post_text.lower():
    #        genre_list = genre
    #        break
    #print(f"{genre_list}")        
    #return entity, genre_list

