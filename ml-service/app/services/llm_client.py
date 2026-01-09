import requests
import logging

logger = logging.getLogger(__name__)


class LLMClient:
    """
    Ollama-based LLM client optimized for low-RAM systems.
    Designed for TEXT generation only (NO JSON).
    """

    def __init__(
        self,
        model_name: str = "gemma2:2b",
        base_url: str = "http://localhost:11434",
    ):
        self.model_name = model_name
        self.base_url = base_url.rstrip("/")
        self.generate_url = f"{self.base_url}/api/generate"

    # -----------------------------------------------------

    def test_connection(self) -> bool:
        try:
            resp = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if resp.status_code != 200:
                return False
            models = resp.json().get("models", [])
            return any(self.model_name == m.get("name") for m in models)
        except Exception as e:
            logger.error(f"Ollama connection failed: {e}")
            return False

    # -----------------------------------------------------

    def generate_text(
        self,
        prompt: str,
        temperature: float = 0.4,
        max_tokens: int = 600,
    ) -> str:
        """
        Generate plain English text from the LLM.
        NEVER expects JSON.
        """

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
                # Remove stop tokens to let LLM complete thoughts
                "stop": [],
            },
        }

        try:
            resp = requests.post(
                self.generate_url,
                json=payload,
                timeout=60,
            )
            resp.raise_for_status()

            text = resp.json().get("response", "").strip()
            return text

        except Exception as e:
            logger.error(f"Ollama generation failed: {e}")
            raise RuntimeError("LLM generation failed")
