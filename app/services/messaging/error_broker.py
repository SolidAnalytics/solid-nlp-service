from typing import Any
from dramatiq import Broker, Message
from dramatiq.brokers.rabbitmq import RabbitmqBroker

import app.config as config


_ERROR_BROKER: Broker = None
def get_error_broker() -> Broker:
    global _ERROR_BROKER

    if not _ERROR_BROKER:
        _ERROR_BROKER = RabbitmqBroker(url=config.ERROR_RABBIT_URL)
    return _ERROR_BROKER


def send_error(
    broker: Broker,
    error: dict[str, Any]
) -> None:
    queue_name = config.ERROR_RABBIT_QUEUE
    actor_name = config.ERROR_RABBIT_ACTOR

    broker.enqueue(Message(
        queue_name=queue_name,
        actor_name=actor_name,
        args=(error,), 
        kwargs={}, 
        options={},
    ))