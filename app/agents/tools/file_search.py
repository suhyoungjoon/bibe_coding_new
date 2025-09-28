from pathlib import Path
from typing import List, Dict
import re
from rank_bm25 import BM25Okapi
DOC_EXTS = {".txt", ".md", ".java", ".py", ".json", ".csv", ".log", ".cfg", ".ini", ".yml", ".yaml", ".xml", ".html", ".htm", ".pdf"}
def _read_text(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        try:
            from pypdf import PdfReader
            reader = PdfReader(str(path))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception:
            return ""
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        try:
            return path.read_text(encoding="cp949", errors="ignore")
        except Exception:
            return ""
def _chunk_text(text: str, chunk_size: int = 1200, overlap: int = 120) -> List[str]:
    tokens = re.split(r"(?<=\n)", text)
    chunks = []
    buff = ""
    for t in tokens:
        if len(buff) + len(t) > chunk_size and buff:
            chunks.append(buff)
            buff = buff[-overlap:] + t
        else:
            buff += t
    if buff:
        chunks.append(buff)
    return chunks
class LocalBM25:
    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self.corpus: List[str] = []
        self.meta: List[Dict[str, str]] = []
        self._bm25 = None
    def index(self):
        files = [p for p in self.data_dir.rglob("*") if p.is_file() and p.suffix.lower() in DOC_EXTS]
        docs = []
        meta = []
        for p in files:
            text = _read_text(p)
            if not text.strip():
                continue
            for chunk in _chunk_text(text):
                docs.append(chunk)
                meta.append({"source": str(p), "chunk": chunk})
        tokenized = [d.lower().split() for d in docs]
        if not tokenized:
            self.corpus = []; self.meta = []; self._bm25 = None; return 0
        self._bm25 = BM25Okapi(tokenized)
        self.corpus = docs; self.meta = meta
        return len(docs)
    def search(self, query: str, k: int = 5):
        if not self._bm25 or not self.corpus:
            return []
        scores = self._bm25.get_scores(query.lower().split())
        idxs = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        out = []
        for i in idxs:
            out.append({"source": self.meta[i]["source"], "chunk": self.meta[i]["chunk"], "score": f"{scores[i]:.4f}"})
        return out
