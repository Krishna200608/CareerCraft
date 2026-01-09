from typing import Dict, Optional
from .llm_client import LLMClient
from .prompt_builder import CoverLetterPromptBuilder
from .text_parser import CoverLetterTextParser


class CoverLetterGenerator:
    def __init__(
        self,
        model_name: str = "gemma2:2b",
        ollama_url: str = "http://localhost:11434"
    ):
        self.llm_client = LLMClient(model_name, ollama_url)
        self.prompt_builder = CoverLetterPromptBuilder()
        self.text_parser = CoverLetterTextParser()

    def generate_cover_letter(
        self,
        resume_analysis: Dict,
        job_info: Dict,
        candidate_name: Optional[str] = ""
    ) -> Dict:

        if not resume_analysis or not job_info:
            raise ValueError("resume_analysis and job_info are required")

        if not self.llm_client.test_connection():
            raise ConnectionError("Ollama is not running or model is missing")

        prompt = self.prompt_builder.build_prompt(
            resume_analysis=resume_analysis,
            job_info=job_info,
            candidate_name=candidate_name
        )

        raw = self.llm_client.generate_text(
            prompt=prompt,
            temperature=0.7,
            max_tokens=1000
        )

        cover_letter = self.text_parser.parse_text_response(raw)
        return self._finalize(cover_letter, job_info, candidate_name)

    def _finalize(self, data: Dict, job_info: Dict, candidate_name: str) -> Dict:
        company = job_info.get("company_name", "")

        if company not in data.get("greeting", ""):
            data["greeting"] = f"Dear Hiring Manager at {company},"

        if not isinstance(data.get("body"), list):
            data["body"] = [str(data.get("body", ""))]

        data["candidate_name"] = candidate_name or ""
        return data
