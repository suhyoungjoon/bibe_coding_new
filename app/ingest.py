from .vectorstore.faiss_store import FaissStore
def rebuild_index():
    fs = FaissStore()
    return fs.build()
