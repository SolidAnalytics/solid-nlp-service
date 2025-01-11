# main.py

from dotenv import load_dotenv, find_dotenv
from os import getenv
import dramatiq
import asyncio
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq.middleware.asyncio import AsyncIO
from logging_config import setup_logging
import logging

# Настройка логирования
setup_logging()

load_dotenv(find_dotenv())
RABBITMQ_URL = getenv("RABBITMQ_URL")

# RabbitMQ
rabbitmq_broker = RabbitmqBroker(url=RABBITMQ_URL) 
rabbitmq_broker.add_middleware(AsyncIO()) 
dramatiq.set_broker(rabbitmq_broker)

if __name__ == "__main__":
    
    logging.info("Starting RabbitMQ broker...")
    rabbitmq_broker.run()
    logging.info("RabbitMQ broker has started.")

