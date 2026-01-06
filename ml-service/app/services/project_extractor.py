from typing import TypedDict, Optional
import re


class ProjectEntry(TypedDict):
    title: Optional[str]
    date: Optional[str]          # single date (month/year or year)
    duration: Optional[str]      # only if real range exists
    tech_stack: list[str]
    description: str


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
    (?:[-]|to|\u2013|\u2014|\s{2,})
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


def normalize(text: str) -> str:
    return (
        text.lower()
        .replace("&", "and")
        .replace(".", "")
        .replace("-", " ")
    )

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

def preprocess_lines(text: str) -> list[str]:
    return [
        l.strip()
        for l in text.splitlines()
        if l.strip()
    ]

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