import os
import logging
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
log_path = os.path.join(basedir, "trace.log")

load_dotenv()

class Config:
    OPENAI_KEY = os.getenv('OPENAI_KEY')
    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_USER = os.getenv('REDIS_USER')
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
    REDIS_INDEX = os.getenv('REDIS_INDEX_NAME')
    FILES_PATH = os.getenv("FILES_PATH")

# logging para trazabilidad
def get_logger(name):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - [%(levelname)s] - %(message)s',
        handlers=[
            logging.FileHandler(log_path, encoding='utf-8'),
            #logging.StreamHandler()
        ]
    )
    return logging.getLogger(name)