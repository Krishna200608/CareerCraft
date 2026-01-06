import re
from typing import TypedDict, Optional

class EducationEntry(TypedDict):
    institution: Optional[str]
    degree: Optional[str]
    duration: Optional[str]

class ExperienceEntry(TypedDict):
    organization: Optional[str]
    role: Optional[str]
    duration: Optional[str]
    description: str

class ProjectEntry(TypedDict):
    title: Optional[str]
    date: Optional[str]          # single date (month/year or year)
    duration: Optional[str]      # only if real range exists
    tech_stack: list[str]
    description: str


SECTION_HEADERS = {
    "skills": "SKILLS",
    "education": "EDUCATION",
    "projects": "PROJECTS",
    "experience": "EXPERIENCE",
    "achievements": "ACHIEVEMENTS",
    "positions": "POSITIONS OF RESPONSIBILITY"
}

SKILL_VOCAB = {
    # languages
    "c", "c++", "c#", "python", "javascript", "sql", "kotlin",

    # frameworks / libraries
    "fastapi", "react", "flutter", "express", "node.js",

    # databases / infra
    "mongodb", "firebase", "aws",

    # tools
    "git", "github", "postman", "vs code", "docker", "faiss"
}

INSTITUTION_PATTERN = re.compile(
    r"(university|institute|college|school)",
    re.IGNORECASE
)

DEGREE_PATTERN = re.compile(
    r"(bachelor|b\.tech|btech|master|m\.tech|mtech|phd|secondary|senior secondary|high school)",
    re.IGNORECASE
)

DURATION_PATTERN = re.compile(
    r"""
    (                           # start date
        (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec|
           January|February|March|April|June|July|August|September|
           October|November|December)?
        \s*
        \d{4}
    )
    \s*
    (?:[-–]|to|\u2013|\u2014|\s{2,})
    \s*
    (                           # end date
        (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec|
           January|February|March|April|June|July|August|September|
           October|November|December)?
        \s*
        (?:\d{4}|Present|present)
    )
    """,
    re.IGNORECASE | re.VERBOSE
)

SINGLE_DATE_PATTERN = re.compile(
    r"""
    ^
    (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec|
       January|February|March|April|June|July|August|September|
       October|November|December)?
    \s*\d{4}
    $
    """,
    re.IGNORECASE | re.VERBOSE
)


ROLE_PATTERN = re.compile(
    r"(intern|engineer|developer|analyst|software|backend|frontend|full[- ]?stack)",
    re.IGNORECASE
)


def normalize(text: str) -> str:
    return (
        text.lower()
        .replace("&", "and")
        .replace(".", "")
        .replace("-", " ")
    )

def extract_skills_from_section(skills_text: str) -> list[str]:
    if not skills_text:
        return []

    normalized_text = normalize(skills_text)
    found = set()

    for skill in SKILL_VOCAB:
        if normalize(skill) in normalized_text:
            found.add(skill)

    return sorted(found)


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


def preprocess_lines(text: str) -> list[str]:
    return [
        l.strip()
        for l in text.splitlines()
        if l.strip()
    ]

def extract_education(education_text: str) -> list[EducationEntry]:
    if not education_text:
        return []

    lines = preprocess_lines(education_text)

    entries: list[EducationEntry] = []
    current: EducationEntry = {
        "institution": None,
        "degree": None,
        "duration": None
    }

    def flush():
        if current["institution"] or current["degree"]:
            entries.append(current.copy())

    for line in lines:
        # duration
        match = DURATION_PATTERN.search(line)
        if match:
            start = match.group(1).strip()
            end = match.group(2).strip()
            current["duration"] = f"{start} - {end}"
            continue

        # institution
        if INSTITUTION_PATTERN.search(line):
            if current["institution"] or current["degree"]:
                flush()
                current = {
                    "institution": None,
                    "degree": None,
                    "duration": None
                }
            current["institution"] = line
            continue

        # degree
        if DEGREE_PATTERN.search(line):
            current["degree"] = line
            continue

        # ignore scores
        if any(k in line.lower() for k in ["cgpa", "percentage", "%"]):
            continue

    flush()
    return entries


def extract_experience(experience_text: str) -> list[ExperienceEntry]:
    if not experience_text:
        return []

    lines = preprocess_lines(experience_text)

    entries: list[ExperienceEntry] = []
    current: ExperienceEntry = {
        "organization": None,
        "role": None,
        "duration": None,
        "description": ""
    }

    def flush():
        if current["organization"] or current["role"]:
            # normalize description spacing
            current["description"] = current["description"].strip()
            entries.append(current.copy())

    for line in lines:
        # duration
        match = DURATION_PATTERN.search(line)
        if match:
            start = match.group(1).strip()
            end = match.group(2).strip()
            current["duration"] = f"{start} - {end}"
            continue

        # role
        if ROLE_PATTERN.search(line):
            current["role"] = line
            continue

        # organization (short, non-sentence, before role)
        if (
            current["organization"] is None
            and current["role"] is None
            and len(line.split()) <= 4
        ):
            current["organization"] = line
            continue

        # description (fallback)
        if line:
            current["description"] += line + " "

    flush()
    return entries


def extract_tech_stack(line: str) -> list[str]:
    if not line.lower().startswith("tech"):
        return []

    normalized = normalize(line)
    found = []

    for skill in SKILL_VOCAB:
        # avoid single-letter skills unless standalone
        if len(skill) == 1:
            if f" {skill} " not in f" {normalized} ":
                continue

        if normalize(skill) in normalized:
            found.append(skill)

    return sorted(set(found))

def is_title_candidate(line: str) -> bool:
    words = line.split()

    # length constraint
    if len(words) > 10:
        return False

    lower = line.lower().strip()

    # never treat tech lines as title
    if lower.startswith("tech"):
        return False

    # never treat dates as titles
    if DURATION_PATTERN.search(line):
        return False

    if SINGLE_DATE_PATTERN.match(line):
        return False

    # sentence-like
    if line.endswith("."):
        return False

    return True


def extract_projects(projects_text: str) -> list[ProjectEntry]:
    if not projects_text:
        return []

    lines = preprocess_lines(projects_text)

    projects: list[ProjectEntry] = []
    current: Optional[ProjectEntry] = None

    def flush():
        nonlocal current
        if current and current["title"]:
            current["description"] = current["description"].strip()
            projects.append(current)
        current = None

    for line in lines:
        # -------- TITLE BOUNDARY --------
        if is_title_candidate(line):
            if current is None or current["description"]:
                flush()
                current = {
                    "title": line.replace("Github", "").strip(),
                    "date": None,
                    "duration": None,
                    "tech_stack": [],
                    "description": ""
                }
                continue

        if current is None:
            continue

        # -------- DURATION (range only) --------
        dur = DURATION_PATTERN.search(line)
        if dur:
            current["duration"] = f"{dur.group(1)} - {dur.group(2)}"
            continue

        # -------- SINGLE DATE --------
        if SINGLE_DATE_PATTERN.match(line):
            current["date"] = line.strip()
            continue

        # -------- TECH STACK --------
        if line.lower().startswith("tech"):
            current["tech_stack"] = extract_tech_stack(line)
            continue

        # -------- DESCRIPTION --------
        current["description"] += line + " "

    flush()
    return projects


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