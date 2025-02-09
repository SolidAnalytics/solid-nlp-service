from typing import Any
from abc import abstractmethod
import traceback
import copy
from loguru import logger

from app.services.messaging import get_error_broker, get_result_broker, send_error, send_result
from app.schemas import LabelingRequest, LabelingResponse

from .utils import get_error_message


class BaseLabelingWorker:
    service_name: str = ""

    def __init__(self):
        pass

    @abstractmethod
    async def process(self, data: LabelingRequest) -> LabelingResponse:
        pass

    async def process_request(self, input_data: dict[str, Any]) -> None:
        input_data = copy.deepcopy(input_data)
        try:
            data = input_data["post_data"]
            data = LabelingRequest.model_validate(data)
        except Exception as err:
            # handle error
            error_broker = get_error_broker()
            logger.exception(f"Error during getting input data: {err}")
            send_error(
                error_broker, 
                get_error_message(
                    self.service_name, 
                    input_data, 
                    err, 
                    traceback.format_exc()
                )
            )
            return

        try:
            result = await self.process(data)
        except Exception as err:
            # handle error
            error_broker = get_error_broker()
            logger.exception(f"Error during parsing: {err}")
            send_error(
                error_broker, 
                get_error_message(
                    self.service_name, 
                    input_data, 
                    err, 
                    traceback.format_exc()
                )
            )
            return
        
        if "sentiment_data" not in input_data:
            input_data["sentiment_data"] = {}
        input_data["sentiment_data"]["result"] = result.model_dump()
        result_broker = get_result_broker()
        send_result(result_broker, input_data)