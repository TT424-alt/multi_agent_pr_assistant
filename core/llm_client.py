from typing import List, Dict, Any
import requests
from config import Config

class LLMClient:
    def __init__(self, backend: str = None):
        self.backend = backend or Config.LLM_BACKEND
        self.model = Config.MODEL_MAP.get(self.backend, "gpt-5.5")

    def chat_completion(self, messages: List[Dict[str, str]], temperature: float = 0.3) -> str:
        if self.backend == "openai":
            return self._openai_chat(messages, temperature)
        elif self.backend == "anthropic":
            return self._anthropic_chat(messages, temperature)
        elif self.backend == "deepseek":
            return self._deepseek_chat(messages, temperature)
        else:
            raise ValueError(f"Unsupported backend: {self.backend}")

    # ---------- OpenAI ----------
    def _openai_chat(self, messages, temperature):
        from openai import OpenAI
        client = OpenAI(api_key=Config.OPENAI_API_KEY, base_url=Config.OPENAI_BASE_URL)
        resp = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
        )
        return resp.choices[0].message.content

    # ---------- Anthropic ----------
    def _anthropic_chat(self, messages, temperature):
        import anthropic
        client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        # Convert messages to Claude format
        system = None
        user_content = ""
        for m in messages:
            if m["role"] == "system":
                system = m["content"]
            else:
                user_content += f"{m['role']}: {m['content']}\n"
        resp = client.messages.create(
            model=self.model,
            system=system,
            messages=[{"role": "user", "content": user_content}],
            temperature=temperature,
            max_tokens=4096,
        )
        return resp.content[0].text

    # ---------- DeepSeek (OpenAI compatible) ----------
    def _deepseek_chat(self, messages, temperature):
        from openai import OpenAI
        client = OpenAI(api_key=Config.DEEPSEEK_API_KEY, base_url=Config.DEEPSEEK_BASE_URL)
        resp = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
        )
        return resp.choices[0].message.content
