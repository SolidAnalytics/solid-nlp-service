import os

from dotenv import load_dotenv

load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")
OPENAI_PROXY = os.getenv("OPENAI_PROXY", None)

INPUT_RABBIT_URL = os.getenv("INPUT_RABBIT_URL")
INPUT_RABBIT_QUEUE = os.getenv("INPUT_RABBIT_QUEUE")
INPUT_RABBIT_ACTOR = os.getenv("INPUT_RABBIT_ACTOR")

RESULT_RABBIT_URL = os.getenv("RESULT_RABBIT_URL")
RESULT_RABBIT_QUEUE = os.getenv("RESULT_RABBIT_QUEUE")
RESULT_RABBIT_ACTOR = os.getenv("RESULT_RABBIT_ACTOR")

ERROR_RABBIT_URL = os.getenv("ERROR_RABBIT_URL")
ERROR_RABBIT_QUEUE = os.getenv("ERROR_RABBIT_QUEUE")
ERROR_RABBIT_ACTOR = os.getenv("ERROR_RABBIT_ACTOR")
