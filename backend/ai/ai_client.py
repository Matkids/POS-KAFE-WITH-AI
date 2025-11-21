import os
import re
from typing import Any, Dict, List, Optional

from common.exceptions import AIClientError
from common.utils import parse_json

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - optional dependency
    OpenAI = None


SYSTEM_PROMPT = """
You help café staff convert natural-language instructions into structured menu items.
Always respond with strict JSON using this shape:
{
  "items": [
    {"name": "", "category": "", "price": 0, "stock": 0}
  ]
}
- price must be integer in rupiah (no currency symbols)
- stock must be integer ≥ 0
- include category if present, otherwise empty string
- never add commentary or markdown
"""


class AIClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model_name = os.getenv("OPENAI_MODEL", "glm-4.6")
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", "0"))
        self.base_url = os.getenv("OPENAI_BASE_URL") or os.getenv("GLM_BASE_URL") or "https://open.bigmodel.cn/api/paas/v4"
        self.last_request: Optional[Dict[str, Any]] = None
        if self.api_key and OpenAI:
            kwargs = {"api_key": self.api_key}
            if self.base_url:
                kwargs["base_url"] = self.base_url
            self.client = OpenAI(**kwargs)
        else:
            self.client = None

    def generate_products(self, instruction: str) -> Dict[str, Any]:
        if not instruction or not instruction.strip():
            raise AIClientError("Instruction is required")

        if self.client:
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": instruction},
            ]
            self.last_request = {"messages": messages, "model": self.model_name}
            try:
                completion = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=self.temperature,
                    response_format={"type": "json_object"},
                )
                content = completion.choices[0].message.content
                return parse_json(content)
            except Exception as exc:  # pragma: no cover - depends on network
                raise AIClientError(f"AI request failed: {exc}")

        # Fallback rule-based parser for environments without an API key
        return {"items": self._rule_based_parse(instruction)}

    def _rule_based_parse(self, instruction: str) -> List[Dict[str, Any]]:
        chunks = [chunk.strip() for chunk in re.split(r"[,;]\s*", instruction) if chunk.strip()]
        items: List[Dict[str, Any]] = []
        for idx, chunk in enumerate(chunks, start=1):
            lower = chunk.lower()
            price_match = re.search(r"(\d+(?:\.\d+)?)(k)?", lower)
            stock_match = re.search(r"stock\s*(\d+)", lower)

            price: Optional[int] = None
            if price_match:
                number = float(price_match.group(1))
                multiplier = 1000 if price_match.group(2) else 1
                price = int(number * multiplier)

            stock = int(stock_match.group(1)) if stock_match else 0
            name = re.sub(r"(stock\s*\d+)|([0-9]+k?)", "", chunk, flags=re.IGNORECASE).strip(" -")
            name = name or f"Item {idx}"

            items.append({"name": name, "category": "", "price": price or 0, "stock": stock})
        return items
