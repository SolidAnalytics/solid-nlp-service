import dramatiq
from openai import OpenAI
from utils import extract_company_and_genre
from genres import genre_list
from dotenv import load_dotenv, find_dotenv
import requests
import os
from os import getenv
import logging
from logging_config import setup_logging
setup_logging()

# Настройка логирования
logger = logging.getLogger(__name__)

load_dotenv(find_dotenv())

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_PROXY_URL = os.getenv("OPENAI_PROXY_URL")
PROXY_USERNAME = os.getenv("PROXY_USERNAME")
PROXY_PASSWORD = os.getenv("PROXY_PASSWORD")




# Инициализация OpenAI
client = {
    "api_key": OPENAI_API_KEY,
    "proxy_url": f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{OPENAI_PROXY_URL}"
}

# Функция для запроса к GPT-4 через прокси
def query_gpt(prompt):
    logger.info("Querying GPT-4 with prompt.")
    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {client['api_key']}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-4o-mini",  # модель
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 150  # токены
    }


    # Отправляем запрос через прокси
    try:
        response = requests.post(url, headers=headers, json=data, proxies={"http": client["proxy_url"], "https": client["proxy_url"]})
        response.raise_for_status()  # Проверка на ошибки HTTP
        logger.info("Successfully queried GPT-4.")
        return response # Возвращаем JSON-ответ
    except requests.exceptions.RequestException as e:
        print(f"error: {e}")
        logger.error(f"Error querying GPT-4: {e}")
        return None

#бесполезный кусок кода, но без него ничего не работает
@dramatiq.actor
def process_post(global_post_id, post_text, prompt):
    logger.info(f"Processing post ID: {global_post_id}.")
    try:
        entity, genre_list = extract_company_and_genre(post_text, prompt)
        logger.info(f"Post ID: {global_post_id}, Entity: {entity}, Genre: {genre_list}.")
    except Exception as e:
        logger.critical(f"Critical error in processing post ID: {global_post_id}: {e}")
        logger.info("Critical error in process_post", str(e))

