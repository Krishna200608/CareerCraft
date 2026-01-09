from typing import Dict, List


class CoverLetterPromptBuilder:
    """
    Prompt builder tuned specifically for Gemma 2B.
    Uses tight constraints, examples, and explicit bans.
    """

    def build_prompt(
        self,
        resume_analysis: Dict,
        job_info: Dict,
        candidate_name: str = ""
    ) -> str:
        company = job_info["company_name"]
        title = job_info["job_title"]
        tone = job_info.get("tone", "formal")

        skills = ", ".join(resume_analysis.get("skills", [])[:8])
        projects = self._format_projects(resume_analysis.get("projects", []))
        experience = self._format_experience(resume_analysis.get("experience", []))

        # 🔑 Extract only key requirements (first 3 lines max)
        jd = job_info.get("job_description", "")
        jd_lines = [l.strip() for l in jd.split("\n") if l.strip()]
        key_requirements = "\n".join(jd_lines[:3])

        return f"""
You are writing a REAL professional cover letter, not a template.

STRICT RULES (DO NOT BREAK):
- DO NOT write placeholders like "Paragraph 1", "Generated content", or labels
- DO NOT invent skills, experience, or education
- DO NOT repeat generic phrases
- DO NOT mention years of experience unless explicitly provided
- Write natural English, like a real applicant

JOB:
- Company: {company}
- Role: {title}
- Tone: {tone}

CANDIDATE FACTS (ONLY SOURCE OF TRUTH):
Skills: {skills}

Experience:
{experience}

Projects:
{projects}

KEY JOB REQUIREMENTS:
{key_requirements}

WRITE EXACTLY 4 PARAGRAPHS:

Paragraph 1:
Introduce the application. Mention the role and company. Keep it direct.

Paragraph 2:
Explain how the candidate’s skills match the role. Use 2–3 skills from the list.

Paragraph 3:
Describe 1–2 projects. Mention tools used and what was built.

Paragraph 4:
Explain why the candidate wants to work at {company}. Use ONLY job info.

FORMAT EXACTLY LIKE THIS (NO EXTRA TEXT):

Dear Hiring Manager at {company},

[Paragraph 1]

[Paragraph 2]

[Paragraph 3]

[Paragraph 4]

I look forward to discussing this opportunity further.

Sincerely,
{candidate_name}
""".strip()

    # --------------------------------------------------

    def _format_projects(self, projects: List[Dict]) -> str:
        if not projects:
            return "None"

        lines = []
        for p in projects[:2]:
            name = p.get("name", "")
            tech = ", ".join(p.get("technologies", []))
            desc = p.get("description", "")
            lines.append(f"- {name}: Built using {tech}. {desc}")
        return "\n".join(lines)

    def _format_experience(self, experience: List[Dict]) -> str:
        if not experience:
            return "None"

        lines = []
        for e in experience[:2]:
            role = e.get("title", "")
            company = e.get("company", "")
            if role and company:
                lines.append(f"- {role} at {company}")
        return "\n".join(lines)
