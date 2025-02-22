from typing import Any
from dramatiq import Broker, Message
from dramatiq.brokers.rabbitmq import RabbitmqBroker

import app.config as config


_RESULT_BROKER: Broker = None
def get_result_broker() -> Broker:
    global _RESULT_BROKER

    if not _RESULT_BROKER:
        _RESULT_BROKER = RabbitmqBroker(url=config.RESULT_RABBIT_URL)
    return _RESULT_BROKER


def send_result(
    broker: Broker,
    data: dict[str, Any]
) -> None:
    queue_name = config.RESULT_RABBIT_QUEUE
    actor_name = config.RESULT_RABBIT_ACTOR

    broker.enqueue(Message(
        queue_name=queue_name,
        actor_name=actor_name,
        args=(data,), 
        kwargs={}, 
        options={},
    ))