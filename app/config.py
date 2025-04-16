import os

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "32e23c6d-8a87-4bb8-90bd-e9a554b6cbab")
DEEPSEEK_API_BASE = "https://ark.cn-beijing.volces.com/api/v3"
DEEPSEEK_MODEL_NAME = "deepseek-r1-250120"

DOCS_PATH = "data/docs"
VECTORSTORE_PATH = "data/vectorstore/index.faiss"
EMBEDDING_MODEL_NAME = "BAAI/bge-small-zh-v1.5"
TIMESTAMP_FILE = "data/vectorstore/last_update.txt"
HISTORY_FILE = "data/logs/history.log"
MEMORY_CACHE = {}