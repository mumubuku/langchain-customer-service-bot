from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from app.knowledge_loader import load_documents, get_latest_doc_timestamp
from app.config import *
import os
import time
import json

vectorstore = None
retriever = None
qa_chain = None


def init_pipeline(force_refresh: bool = False):
    global vectorstore, retriever, qa_chain

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    rebuild_required = force_refresh
    latest_doc_time = get_latest_doc_timestamp(DOCS_PATH)

    if not os.path.exists(VECTORSTORE_PATH):
        print("No vectorstore found. Will build new index.")
        rebuild_required = True
    elif not os.path.exists(TIMESTAMP_FILE):
        print("No timestamp record found. Will rebuild index.")
        rebuild_required = True
    else:
        with open(TIMESTAMP_FILE, 'r') as f:
            last_index_time = float(f.read().strip())
        if latest_doc_time > last_index_time:
            print("Newer documents detected. Rebuilding index...")
            rebuild_required = True

    if rebuild_required:
        docs = load_documents(DOCS_PATH)
        vectorstore = FAISS.from_documents(docs, embeddings)
        vectorstore.save_local(VECTORSTORE_PATH)
        os.makedirs(os.path.dirname(TIMESTAMP_FILE), exist_ok=True)
        with open(TIMESTAMP_FILE, 'w') as f:
            f.write(str(time.time()))
    else:
        print("Loading existing FAISS index...")
        vectorstore = FAISS.load_local(VECTORSTORE_PATH, embeddings, allow_dangerous_deserialization=True)

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    llm = ChatOpenAI(
        openai_api_key=DEEPSEEK_API_KEY,
        openai_api_base=DEEPSEEK_API_BASE,
        model_name=DEEPSEEK_MODEL_NAME,
        temperature=0.3
    )

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )


def log_interaction(user_id, question, answer):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    log_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": user_id,
        "question": question,
        "answer": answer
    }
    with open(HISTORY_FILE, 'a') as f:
        f.write(json.dumps(log_data, ensure_ascii=False) + "\n")


def get_history_by_user(user_id):
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, 'r') as f:
        return [json.loads(line) for line in f if json.loads(line).get("user_id") == user_id]


def ask_question(question: str, user_id: str = "anonymous"):
    if not qa_chain:
        init_pipeline()
    chat_history = MEMORY_CACHE.get(user_id, [])
    result = qa_chain.invoke({"question": question, "chat_history": chat_history})
    MEMORY_CACHE[user_id] = chat_history + [(question, result["answer"])]
    answer = result["answer"]
    sources = [doc.metadata for doc in result.get("source_documents", [])]
    log_interaction(user_id, question, answer)
    return {"answer": answer, "sources": sources}
