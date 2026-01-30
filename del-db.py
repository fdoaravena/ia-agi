import redis
from config import Config

r = redis.Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    username=Config.REDIS_USER,
    password=Config.REDIS_PASSWORD,
    db=0
)

try:
    r.ft(Config.REDIS_INDEX).dropindex(delete_documents=True)
    print("indice y documentos eliminados")
except:
    print("indice no existe")