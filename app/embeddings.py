import numpy as np
from typing import List
from .config import (
    AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_VERSION, AZURE_OPENAI_EMBEDDING_DEPLOYMENT
)
class EmbeddingClient:
    def __init__(self):
        from openai import AzureOpenAI  # type: ignore
        if not (AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY):
            self.is_mock = True
            self.client = None
        else:
            self.is_mock = False
            self.client = AzureOpenAI(
                azure_endpoint=AZURE_OPENAI_ENDPOINT,
                api_key=AZURE_OPENAI_API_KEY,
                api_version=AZURE_OPENAI_API_VERSION,
            )
        self.deployment = AZURE_OPENAI_EMBEDDING_DEPLOYMENT
    
    def embed(self, texts: List[str]):
        if self.is_mock or self.client is None:
            # Mock 모드: 랜덤 벡터 생성
            import numpy as np
            dim = 1536  # text-embedding-3-small 차원
            vecs = np.random.rand(len(texts), dim).astype(np.float32)
            # 정규화
            norms = np.linalg.norm(vecs, axis=1, keepdims=True)
            vecs = vecs / (norms + 1e-8)
            return vecs
        else:
            resp = self.client.embeddings.create(model=self.deployment, input=texts)
            vecs = [d.embedding for d in resp.data]
            import numpy as np
            return np.array(vecs, dtype="float32")
