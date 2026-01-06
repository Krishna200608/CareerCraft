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