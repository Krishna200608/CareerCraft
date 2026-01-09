from typing import Dict, List
import re


class CoverLetterTextParser:
    """
    Deterministic parser for LLM-generated cover letters.
    Preserves paragraph structure whenever possible.
    """

    def parse_text_response(self, text: str) -> Dict:
        lines = [l.rstrip() for l in text.split("\n")]

        greeting = "Dear Hiring Manager,"
        closing = "I look forward to discussing this opportunity further."
        sign_off = "Sincerely"
        candidate_name = ""
        body: List[str] = []

        # Remove empty lines only at edges
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()

        #  Greeting
        if lines and lines[0].lower().startswith("dear"):
            greeting = lines.pop(0).strip()

        # Remove empty line after greeting
        if lines and not lines[0].strip():
            lines.pop(0)

        #  Sign-off + name (from bottom)
        if lines and lines[-1].strip() and not lines[-1].lower().startswith("sincerely"):
            candidate_name = lines.pop().strip()

        if lines and lines[-1].lower().startswith("sincerely"):
            sign_off = lines.pop().strip()

        # Remove empty line before closing
        while lines and not lines[-1].strip():
            lines.pop()

        #  Closing sentence
        if lines and "look forward" in lines[-1].lower():
            closing = lines.pop().strip()

        #  Body paragraphs (preserve blocks)
        body = self._extract_paragraphs(lines)

        return {
            "greeting": greeting,
            "body": body[:4],  # hard cap
            "closing": closing,
            "sign_off": sign_off,
            "candidate_name": candidate_name
        }

    def _extract_paragraphs(self, lines: List[str]) -> List[str]:
        paragraphs = []
        current = []

        for line in lines:
            if line.strip():
                # remove "Paragraph X:" labels safely
                clean = re.sub(r"^Paragraph\s*\d+:\s*", "", line).strip()
                current.append(clean)
            else:
                if current:
                    paragraphs.append(" ".join(current))
                    current = []

        if current:
            paragraphs.append(" ".join(current))

        # Fallback if model returned everything in one block
        if len(paragraphs) <= 1:
            paragraphs = self._fallback_sentence_split(" ".join(paragraphs))

        return [p for p in paragraphs if len(p) > 40]

    def _fallback_sentence_split(self, text: str) -> List[str]:
        sentences = re.split(r"(?<=[.!?])\s+", text)
        paras = []
        buf = []

        for s in sentences:
            buf.append(s)
            if len(" ".join(buf)) > 120:
                paras.append(" ".join(buf))
                buf = []

        if buf:
            paras.append(" ".join(buf))

        return paras
