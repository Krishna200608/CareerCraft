from typing import TypedDict, Optional
import re


class EducationEntry(TypedDict):
    institution: Optional[str]
    degree: Optional[str]
    duration: Optional[str]


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

INSTITUTION_PATTERN = re.compile(
    r"(university|institute|college|school)",
    re.IGNORECASE
)


DEGREE_PATTERN = re.compile(
    r"(bachelor|b\.tech|btech|master|m\.tech|mtech|phd|secondary|senior secondary|high school)",
    re.IGNORECASE
)


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

