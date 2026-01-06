from typing import TypedDict, Optional
import re

class ExperienceEntry(TypedDict):
    organization: Optional[str]
    role: Optional[str]
    duration: Optional[str]
    description: str

ROLE_PATTERN = re.compile(
    r"(intern|engineer|developer|analyst|software|backend|frontend|full[- ]?stack)",
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


def preprocess_lines(text: str) -> list[str]:
    return [
        l.strip()
        for l in text.splitlines()
        if l.strip()
    ]


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
