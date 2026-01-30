#from langchain.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings

#from langchain.vectorstores.redis import Redis
from langchain_community.vectorstores import Redis

#from langchain.document_loaders import TextLoader
from langchain_community.document_loaders import TextLoader

#from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.embeddings import SentenceTransformerEmbeddings

#from langchain.text_splitter import CharacterTextSplitter
from langchain_text_splitters import CharacterTextSplitter

import numpy as np
import openai
from redis.commands.search.query import Query
import redis
from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

gpt_key=os.getenv('OPENAI_KEY')
redis_host=os.getenv('REDIS_HOST')
redis_port=int(os.getenv('REDIS_PORT'))
redis_username=os.getenv('REDIS_USER')
redis_password=os.getenv('REDIS_PASSWORD')
redis_index=os.getenv('REDIS_INDEX_NAME')
files_path = os.environ.get("FILES_PATH")

embeddings = OpenAIEmbeddings(
    openai_api_key=gpt_key
)



if not files_path:
    raise ValueError("La variable de entorno FILES_PATH no está definida")

path = Path(files_path)

if not path.exists() or not path.is_dir():
    raise ValueError(f"La ruta no existe o no es un directorio: {path}")

# Cargar todos los .txt
documents = []
for txt_file in path.glob("*.txt"):
    loader = TextLoader(txt_file, encoding="utf-8")
    documents.extend(loader.load())

if not documents:
    raise ValueError("No se encontraron archivos .txt en la carpeta")

text_splitter = CharacterTextSplitter(chunk_size=10000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

vectorstore = Redis.from_documents(
    docs,
    embeddings,
    redis_url=f"redis://{redis_username}:{redis_password}@{redis_host}:{redis_port}/0",
    index_name=redis_index
)




def search(question):
    # Conexión a Redis
    r = redis.Redis(
        host=redis_host,
        port=redis_port,
        db=0,
        username=redis_username,
        password=redis_password
    )

    print(question)

    VECTOR_FIELD_NAME = "content_vector"

    # Cliente OpenAI con nuevo SDK
    client = OpenAI(api_key=gpt_key)

    # Crear embedding con nueva API
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=question,
    )

    embedded_query = np.array(response.data[0].embedding, dtype=np.float32).tobytes()

    # Armar consulta Redis para vector search
    q = (
        Query(f'*=>[KNN 1 @{VECTOR_FIELD_NAME} $vec_param AS vector_score]')
        .sort_by('vector_score')
        .paging(0, 3)
        .return_fields('filename', 'text_chunk', 'text_chunk_index', 'content', 'vector_score')
        .dialect(2)
    )

    params_dict = {"vec_param": embedded_query}
    results = r.ft(redis_index).search(q, query_params=params_dict)

    print(VECTOR_FIELD_NAME)

    return results


#preg = "cual es el control que tiene relacion con autenticacion de doble factor?"
preg = "¿cual es la mejor banda de rock?"
results = search(preg)
print(results.docs[0].vector_score)
print("----------------------------------")
print(results.docs[0].content)