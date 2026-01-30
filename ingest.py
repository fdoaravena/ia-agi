from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Redis
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from pathlib import Path
from config import Config

gpt_key=Config.OPENAI_KEY
redis_host=Config.REDIS_HOST
redis_port=Config.REDIS_PORT
redis_username=Config.REDIS_USER
redis_password=Config.REDIS_PASSWORD
redis_index=Config.REDIS_INDEX
files_path=Config.FILES_PATH

embeddings = OpenAIEmbeddings(
    openai_api_key=gpt_key
)

path = Path(files_path)

if not path.exists() or not path.is_dir():
    raise ValueError(f"La ruta no existe o no es un directorio: {path}")

documents = []
for txt_file in path.glob("*.txt"):
    loader = TextLoader(txt_file, encoding="utf-8")
    documents.extend(loader.load())

if not documents:
    raise ValueError("No se encontraron archivos .txt en la carpeta")

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

vectorstore = Redis.from_documents(
    docs,
    embeddings,
    redis_url=f"redis://{redis_username}:{redis_password}@{redis_host}:{redis_port}/0",
    index_name=redis_index
)

print(f"procesados {len(documents)} archivos")