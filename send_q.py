import dramatiq
from dotenv import load_dotenv
from tasks import process_post
from dotenv import load_dotenv, find_dotenv
from os import getenv
import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq.middleware.asyncio import AsyncIO
from tasks import query_gpt
from genres import genre_list
import logging
from logging_config import setup_logging
setup_logging()

# Настройка логирования
logger = logging.getLogger(__name__)


load_dotenv(find_dotenv())
RABBITMQ_URL = getenv("RABBITMQ_URL")


#RabbitMQ
rabbitmq_broker = RabbitmqBroker(url=RABBITMQ_URL) 
rabbitmq_broker.add_middleware(AsyncIO()) 
dramatiq.set_broker(rabbitmq_broker)

#тут считывается текст поста
global_post_id = 12
post_text = "Компания OpenAI анонсировала новую модель GPT-4, которая обещает быть еще более мощной."
prompt = "В тексте ниже найдите название компании и жанр поста. Если компания не упоминается, верните 'unknown'.\n Жанры:" + genre_list + "Если жанр не соответствует ни одному из указанных, верните 'unknown'.\n\nТекст: " + post_text


def send_post_task(global_post_id, post_text):
    # Формируем промпт для обработки
    
    global_post_id = global_post_id
    post_text = post_text
    get_prompt = prompt
    logger.info(f"Sending task for post ID: {global_post_id}.")

    # Отправляем задачу в очередь
    process_post.send(global_post_id, post_text, get_prompt)
    return post_text, get_prompt
      

if __name__ == "__main__":
    # данные для отправки

    global_post_id = global_post_id
    post_text = post_text
    get_prompt = prompt

    # Отправка задачи
    logger.info("Sending post task.")
    send_post_task(global_post_id, post_text)
    print(f"Task sent for post ID: {global_post_id}")
    logger.info(f"Task sent for post ID: {global_post_id}.")
    response = query_gpt(get_prompt)
    #print("Текст ответа:", response.text) #полный ответ

    if response:
        #print("JSON ответ:")
        try:
            # Преобразуем текст ответа в JSON
            json_response = response.json()  # для получения JSON
            #print(json_response)

            # Извлекаем ответ от модели
            if "choices" in json_response and len(json_response["choices"]) != 0:
                # Проверяем, что структура ответа соответствует ожиданиям
                content = json_response["choices"][0]["message"]["content"]
                
                entity = content[0] if len(content) > 0 else "unknown"
                #print(f"{entity}") # пока хз, эта строка выводит не компанию, а букву К
                logger.info("Received response from GPT-4.")
                print("Ответ от GPT-4o-mini:", content)  # Печатаем ответ от модели
            else:
                print("Нет ответа от модели.")
                logger.warning("No response from model.")
        except ValueError:
            print("Ошибка при преобразовании ответа в JSON.")
            logger.error("Error parsing response to JSON.")
    else:
        print("Ошибка при получении ответа.")
        logger.error("Error retrieving response.")
