import os
from typing import List, Dict
from .config import (
    LLM_PROVIDER, AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_VERSION, AZURE_OPENAI_DEPLOYMENT
)
class LLMClient:
    def __init__(self):
        self.provider = LLM_PROVIDER
        self.is_mock = False
        if self.provider == "azure":
            try:
                from openai import AzureOpenAI  # type: ignore
                if not (AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY):
                    self.is_mock = True
                    self.client = None
                else:
                    self.client = AzureOpenAI(
                        azure_endpoint=AZURE_OPENAI_ENDPOINT,
                        api_key=AZURE_OPENAI_API_KEY,
                        api_version=AZURE_OPENAI_API_VERSION,
                    )
            except Exception:
                self.is_mock = True
                self.client = None
        else:
            self.is_mock = True
            self.client = None
    def chat(self, messages: List[Dict[str, str]], system: str | None = None) -> str:
        if self.is_mock or self.client is None:
            last_user = next((m["content"] for m in reversed(messages) if m["role"]=="user"), "")
            plan = next((m["content"] for m in reversed(messages) if m["role"]=="assistant" and m["content"].startswith("Plan:")), "")
            return f"(MOCK) System: {system or 'N/A'}\nPlan/Notes: {plan}\n\nAnswer:\n- {last_user}\n\n(Set up Azure OpenAI env in .env to enable real answers.)"
        resp = self.client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=([{"role":"system","content":system}] if system else []) + messages,
            temperature=0.2,
        )
        return resp.choices[0].message.content
