from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import re
import textstat


# --- SECTION ---
def score_section_completeness(analysis: dict) -> float:
    REQUIRED_SECTIONS = ["skills", "education", "experience", "projects"]

    score = 0.0

    for section in REQUIRED_SECTIONS:
        # section detected?
        if analysis["sections"].get(section):
            content = analysis.get(section)

            # non-empty structured content
            if content and isinstance(content, list) and len(content) > 0:
                score += 7.5
            # raw section exists but poorly populated
            elif analysis["raw_sections"].get(section):
                score += 3.5

    return score

# --- SKILLS ---
def score_skill_count(skills: list[str]) -> float:
    n = len(skills)

    if n < 6:
        return 5
    elif n < 10:
        return 10
    elif n < 15:
        return 13
    else:
        return 15

SKILL_CATEGORIES = {
    "languages": {"c", "c++", "c#", "python", "javascript", "sql", "kotlin"},
    "frameworks": {"fastapi", "react", "flutter", "express"},
    "databases": {"mongodb", "firebase"},
    "tools": {"git", "github", "postman", "vs code", "aws", "docker", "faiss"}
}

def score_skill_diversity(skills: list[str]) -> float:
    present = set(skills)
    categories_covered = 0

    for group in SKILL_CATEGORIES.values():
        if present & group:
            categories_covered += 1

    if categories_covered >= 4:
        return 8
    elif categories_covered == 3:
        return 6
    elif categories_covered == 2:
        return 4
    else:
        return 2

def score_skill_reuse(skills: list[str], analysis: dict) -> float:
    text = (
        analysis["raw_sections"].get("experience", "") +
        analysis["raw_sections"].get("projects", "")
    ).lower()

    reused = sum(1 for s in skills if s in text)

    ratio = reused / max(len(skills), 1)

    if ratio > 0.6:
        return 7
    elif ratio > 0.4:
        return 5
    elif ratio > 0.2:
        return 3
    else:
        return 1

def score_skills(analysis: dict) -> float:
    skills = analysis["skills"]

    return (
        score_skill_count(skills)
        + score_skill_diversity(skills)
        + score_skill_reuse(skills, analysis)
    )


# --- KEYWORD ---
def extract_top_keywords(text: str, top_k: int = 30) -> list[str]:
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=top_k
    )

    tfidf = vectorizer.fit_transform([text])
    return vectorizer.get_feature_names_out().tolist()


def normalize_token(s: str) -> str:
    return s.lower().replace(".", "").replace(" ", "")


def score_keyword_presence(keywords: list[str], skills: list[str]) -> float:
    skill_set = {normalize_token(s) for s in skills}
    hits = sum(1 for k in keywords if normalize_token(k) in skill_set)

    if hits >= 8:
        return 10
    elif hits >= 5:
        return 7
    elif hits >= 3:
        return 4
    else:
        return 2

def score_keyword_density(text: str, keywords: list[str]) -> float:
    words = re.findall(r"[a-z0-9]+", text.lower())
    counts = Counter(words)

    repeated = sum(1 for k in keywords if counts[k] >= 2)

    ratio = repeated / max(len(keywords), 1)

    if ratio > 0.5:
        return 6
    elif ratio > 0.3:
        return 4
    else:
        return 2

def score_filler_penalty(keywords: list[str], skills: list[str]) -> float:
    technical = set(skills)
    tech_hits = sum(1 for k in keywords if k in technical)

    ratio = tech_hits / max(len(keywords), 1)

    if ratio > 0.4:
        return 4
    elif ratio > 0.25:
        return 2
    else:
        return 1

def score_keyword_optimization(analysis: dict, content: str) -> float:
    if not content or not content.strip():
        return 0

    text = content.lower()
    keywords = extract_top_keywords(text)
    skills = analysis["skills"]

    return (
        score_keyword_presence(keywords, skills)
        + score_keyword_density(text, keywords)
        + score_filler_penalty(keywords, skills)
    )

# --- READABILITY ---
def score_flesch(text: str) -> float:
    score = textstat.flesch_reading_ease(text)

    if score >= 50:
        return 10
    elif score >= 40:
        return 8
    elif score >= 30:
        return 5
    else:
        return 2
    
def score_sentence_length(text: str) -> float:
    sentences = re.split(r"[.!?]", text)
    sentences = [s.strip() for s in sentences if s.strip()]

    if not sentences:
        return 0

    avg_len = sum(len(s.split()) for s in sentences) / len(sentences)

    if avg_len <= 20:
        return 5
    elif avg_len <= 25:
        return 3
    else:
        return 1

def score_paragraph_density(text: str) -> float:
    paragraphs = [p for p in text.split("\n\n") if p.strip()]

    if not paragraphs:
        return 0

    avg_len = sum(len(p.split()) for p in paragraphs) / len(paragraphs)

    if avg_len <= 80:
        return 5
    elif avg_len <= 120:
        return 3
    else:
        return 1
    
def score_readability(text: str) -> float:
    if not text or not text.strip():
        return 0

    return (
        score_flesch(text)
        + score_sentence_length(text)
        + score_paragraph_density(text)
    )

# --- FEEDBACK ---
def feedback_sections(analysis: dict) -> list[str]:
    feedback = []
    required = ["skills", "education", "experience", "projects"]

    for sec in required:
        if not analysis["sections"].get(sec):
            feedback.append(
                f"Add a {sec} section to improve resume completeness and ATS visibility."
            )
        elif not analysis.get(sec):
            feedback.append(
                f"Expand the {sec} section with more detailed and structured content."
            )

    return feedback

def feedback_skills(skill_score: float, skills: list[str]) -> list[str]:
    feedback = []

    if len(skills) < 8:
        feedback.append(
            "Include more relevant technical skills to improve keyword coverage."
        )

    if skill_score < 20:
        feedback.append(
            "Balance skills across languages, frameworks, databases, and tools."
        )

    return feedback

def feedback_keywords(keyword_score: float) -> list[str]:
    if keyword_score < 12:
        return [
            "Improve keyword alignment by repeating core technical terms in experience and project descriptions."
        ]
    return []

def feedback_readability(readability_score: float) -> list[str]:
    if readability_score < 12:
        return [
            "Improve readability by shortening sentences and breaking dense paragraphs into bullet points."
        ]
    return []

def generate_feedback(
    analysis: dict,
    section_score: float,
    skill_score: float,
    keyword_score: float,
    readability_score: float
) -> list[str]:

    feedback = []

    feedback += feedback_sections(analysis)
    feedback += feedback_skills(skill_score, analysis["skills"])
    feedback += feedback_keywords(keyword_score)
    feedback += feedback_readability(readability_score)

    # ensure minimum 3 feedback points
    if len(feedback) < 3:
        feedback.append(
            "Quantify impact in experience and project descriptions using metrics or outcomes."
        )

    # remove duplicates, preserve order
    seen = set()
    final = []
    for f in feedback:
        if f not in seen:
            final.append(f)
            seen.add(f)

    return final[:5]


def compute_ats_score(analysis: dict, content: str) -> dict:
    section_score = score_section_completeness(analysis)
    skill_score = score_skills(analysis)
    keyword_score = score_keyword_optimization(analysis, content)
    readability_score = score_readability(content)

    total = section_score + skill_score + keyword_score + readability_score

    feedback = generate_feedback(
        analysis,
        section_score,
        skill_score,
        keyword_score,
        readability_score
    )

    return {
        "ats_score": min(100, round(total)),
        "breakdown": {
            "sections": section_score,
            "skills": skill_score,
            "keywords": keyword_score,
            "readability": readability_score
        },
        "feedback": feedback
    }