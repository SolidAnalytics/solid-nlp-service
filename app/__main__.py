from __future__ import annotations

import argparse
from typing import Any

import dramatiq
from dramatiq.middleware.asyncio import AsyncIO
from dramatiq.brokers.rabbitmq import RabbitmqBroker

import app.config as config
from app.workers import BaseLabelingWorker, OpenAILabelingWorker


broker = RabbitmqBroker(url=config.INPUT_RABBIT_URL)
dramatiq.set_broker(broker)
dramatiq.get_broker().add_middleware(AsyncIO())


_WORKER: BaseLabelingWorker = None
async def get_worker() -> BaseLabelingWorker:
    global _WORKER

    if _WORKER is None:
        _WORKER = OpenAILabelingWorker(
            model_name=config.OPENAI_MODEL_NAME, 
            openai_api_key=config.OPENAI_API_KEY
        )

    return _WORKER


@dramatiq.actor(queue_name=config.INPUT_RABBIT_QUEUE, actor_name=config.INPUT_RABBIT_ACTOR)
async def run_task(input_data: dict[str, Any]) -> None:
    worker = await get_worker()
    await worker.process_request(input_data)


if __name__ == "__main__":
    res = run_task.send({
        'post_data': {
            'global_post_id': 1,
            'post_text': 'Брал недавно кредит в Сбербанке, очень доволен, все было очень быстро и просто',
            'entity': 'Сбербанк',
            'genre_list': ['статья', 'обзор', 'рекомендация', 'отзыв']
        }
    })
    res = run_task.send({
        'post_data': {
            'global_post_id': 2,
            'post_text': 'Заходил в офис сбера, хотел оформить карту, но там было очень долго, сотрудники были не очень вежливые и не подошли даже в течение 20 минут!!!',
            'entity': 'Сбербанк',
            'genre_list': ['статья', 'обзор', 'рекомендация', 'отзыв']
        }
    })