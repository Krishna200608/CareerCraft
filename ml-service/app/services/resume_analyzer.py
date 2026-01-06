from app.services.skill_extractor import extract_skills_from_section
from app.services.education_extractor import extract_education
from app.services.experience_extractor import extract_experience
from app.services.project_extractor import extract_projects

SECTION_HEADERS = {
    "skills": "SKILLS",
    "education": "EDUCATION",
    "projects": "PROJECTS",
    "experience": "EXPERIENCE",
    "achievements": "ACHIEVEMENTS",
    "positions": "POSITIONS OF RESPONSIBILITY"
}


def detect_sections(text: str) -> dict:
    upper = text.upper()
    return {
        key: header in upper
        for key, header in SECTION_HEADERS.items()
    }

def extract_raw_sections(text: str) -> dict:
    lines = text.splitlines()
    section_indices = {}

    # find line indices of each section header
    for i, line in enumerate(lines):
        normalized = line.strip().upper()
        for key, header in SECTION_HEADERS.items():
            if normalized == header:
                section_indices[key] = i

    # sort sections by appearance
    ordered = sorted(section_indices.items(), key=lambda x: x[1])

    raw_sections = {}

    for idx, (section, start) in enumerate(ordered):
        end = (
            ordered[idx + 1][1]
            if idx + 1 < len(ordered)
            else len(lines)
        )

        raw_text = "\n".join(lines[start + 1 : end]).strip()
        raw_sections[section] = raw_text

    return raw_sections


def get_analysis(content: str):

    sections_present = detect_sections(content)
    raw_sections = extract_raw_sections(content)

    skills = extract_skills_from_section(raw_sections.get("skills", ""))

    education = extract_education(raw_sections.get("education", ""))
    experience = extract_experience(raw_sections.get("experience", ""))
    projects = extract_projects(raw_sections.get("projects", ""))

    return {
        "sections": sections_present,
        "raw_sections": raw_sections,
        "skills": skills,
        "education": education,
        "experience": experience,
        "projects": projects,
    }