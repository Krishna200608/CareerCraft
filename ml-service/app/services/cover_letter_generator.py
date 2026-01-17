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

    def _generate_mock_cover_letter(
        self,
        job_info: Dict,
        candidate_name: str = ""
    ) -> Dict:
        """Generate a mock cover letter when Ollama is unavailable (for testing)."""
        company = job_info.get("company_name", "the company")
        job_title = job_info.get("job_title", "the position")
        
        return {
            "greeting": f"Dear Hiring Manager at {company},",
            "body": [
                f"I am writing to express my strong interest in the {job_title} position at {company}. With my technical background and passion for building impactful software, I am confident I would be a valuable addition to your team.",
                "Throughout my experience, I have developed strong skills in modern web technologies including React, Node.js, and database management. I have successfully delivered multiple projects that demonstrate my ability to write clean, maintainable code and collaborate effectively with cross-functional teams.",
                f"I am particularly drawn to {company}'s commitment to innovation and would welcome the opportunity to contribute to your mission. I am eager to bring my problem-solving abilities and technical expertise to help drive the success of your engineering team.",
                "Thank you for considering my application. I look forward to the opportunity to discuss how my skills and experience align with your needs."
            ],
            "closing": "Sincerely,",
            "sign_off": candidate_name or "Applicant",
            "candidate_name": candidate_name or ""
        }

    def generate_cover_letter(
        self,
        resume_analysis: Dict,
        job_info: Dict,
        candidate_name: Optional[str] = ""
    ) -> Dict:

        if not resume_analysis or not job_info:
            raise ValueError("resume_analysis and job_info are required")

        # Check if Ollama is available
        if not self.llm_client.test_connection():
            # Return mock data for testing when Ollama is unavailable
            import logging
            logging.warning("Ollama not available - returning mock cover letter for testing")
            return self._generate_mock_cover_letter(job_info, candidate_name or "")

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
    
    def health_check(self) -> Dict:
        """Check if the LLM service is healthy."""
        connected = self.llm_client.test_connection()
        return {
            "status": "healthy" if connected else "degraded (using mock)",
            "llm_connected": connected,
            "model": self.llm_client.model_name if connected else None,
            "supported_models": self.get_supported_models() if connected else None,
            "error": None if connected else "Ollama not available - mock mode enabled"
        }
    
    def get_supported_models(self):
        """Get list of supported models."""
        return ["gemma2:2b", "llama2", "mistral"]
