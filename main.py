import os
import json
import asyncio
import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from aio_pika import connect_robust, IncomingMessage, Message
from openai import AsyncOpenAI

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY не установлен!")
else:
    logger.debug(f"OPENAI_API_KEY загружен длиной {len(OPENAI_API_KEY)} символов.")

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()

INPUT_QUEUE_NAME = "input_queue"
OUTPUT_QUEUE_NAME = "output_queue"
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost/")
logger.debug(f"RABBITMQ_URL: {RABBITMQ_URL}")

async def load_system_prompt(filename="system_prompt.txt"):
    logger.debug("Загрузка системного промпта...")
    try:
        with open(filename, "r", encoding="utf-8") as file:
            prompt = file.read().strip()
            logger.info("Системный промпт успешно загружен.")
            return prompt
    except FileNotFoundError as e:
        error_message = f"Файл {filename} не найден."
        logger.error(error_message)
        raise Exception(error_message) from e

async def send_request_to_openai(news_id: str, news_text: str, company: str):
    logger.debug(f"Отправляем запрос к OpenAI. news_id={news_id}, company={company}")
    system_prompt = await load_system_prompt()
    user_content = f"Новость:\n{news_text}\n\nКомпания: {company}\nВыведи строго один вариант: Positive или Neutral или Negative."
    
    try:
        logger.debug("Отправляем запрос в OpenAI chat.completions.acreate")
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_content
                }
            ]
        )
        logger.debug(f"Ответ от OpenAI получен: {response}")

        assistant_message = response.choices[0].message.content.strip()
        logger.debug(f"OpenAI вернул: {assistant_message}")

        if assistant_message not in ["Positive", "Neutral", "Negative"]:
            if "positive" in assistant_message.lower():
                sentiment = "Positive"
            elif "neutral" in assistant_message.lower():
                sentiment = "Neutral"
            elif "negative" in assistant_message.lower():
                sentiment = "Negative"
            else:
                sentiment = "Neutral"
        else:
            sentiment = assistant_message
            
        logger.info(f"Определён сентимент: {sentiment} для новости {news_id}")
        return [news_id, sentiment]
    except Exception as e:
        logger.error(f"Ошибка при запросе к OpenAI: {e}")
        return [news_id, "Neutral"]  # fallback


async def on_message(message: IncomingMessage, channel):
    logger.debug(f"Получено новое сообщение: {message.body}")
    async with message.process():
        try:
            data = json.loads(message.body)
            logger.debug(f"Сообщение раскодировано: {data}")
            # Ожидаемый формат: [id_новости, текст_новости, компания]
            if len(data) != 3:
                logger.error(f"Некорректный формат сообщения: {data}")
                return
            news_id, news_text, company = data
            logger.debug(f"Обработка новости {news_id} для компании {company}")
            result = await send_request_to_openai(news_id, news_text, company)

            logger.debug(f"Отправляем результат в выходную очередь: {result}")
            await channel.default_exchange.publish(
                Message(body=json.dumps(result).encode()),
                routing_key=OUTPUT_QUEUE_NAME,
            )
            logger.info(f"Результат отправлен в {OUTPUT_QUEUE_NAME}: {result}")
        except Exception as e:
            logger.error(f"Ошибка обработки сообщения: {e}")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

async def main():
    logger.info("Подключаемся к RabbitMQ...")
    connection = await connect_robust(RABBITMQ_URL)
    logger.info("Подключение к RabbitMQ установлено.")
    channel = await connection.channel()

    logger.info(f"Объявляем очередь {INPUT_QUEUE_NAME}")
    await channel.declare_queue(INPUT_QUEUE_NAME, durable=True)
    logger.info(f"Объявляем очередь {OUTPUT_QUEUE_NAME}")
    await channel.declare_queue(OUTPUT_QUEUE_NAME, durable=True)

    await channel.set_qos(prefetch_count=1)
    input_queue = await channel.get_queue(INPUT_QUEUE_NAME)

    # Начинаем слушать входящую очередь
    logger.info(f"Начинаем прослушивание очереди {INPUT_QUEUE_NAME}...")
    await input_queue.consume(lambda msg: on_message(msg, channel))


@app.on_event("startup")
async def startup_event():
    # Запускаем main при старте приложения
    logger.info("Запуск подписки на очередь при старте приложения...")
    await main()

if __name__ == "__main__":
    import uvicorn
    logger.info("Запускаем сервис на порту 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
