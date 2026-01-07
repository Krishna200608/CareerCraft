"""
Job Skill Extractor Service
Extracts required skills from job descriptions using spaCy and regex.
"""

import re
import spacy
from typing import List, Set

# Load spaCy model with automatic download
def load_spacy_model():
    """Load spaCy model, downloading if necessary."""
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        print("Downloading spaCy model 'en_core_web_sm'...")
        import subprocess
        import sys
        subprocess.check_call([
            sys.executable, "-m", "spacy", "download", "en_core_web_sm"
        ])
        return spacy.load("en_core_web_sm")

nlp = load_spacy_model()


# Skill-heavy section keywords
SKILL_SECTION_PATTERNS = [
    r"(?i)required\s+skills?",
    r"(?i)technical\s+skills?",
    r"(?i)qualifications?",
    r"(?i)requirements?",
    r"(?i)must\s+have",
    r"(?i)experience\s+with",
    r"(?i)proficiency\s+in",
    r"(?i)knowledge\s+of",
]

# Common soft skills to filter out
SOFT_SKILLS = {
    "communication", "teamwork", "leadership", "problem solving",
    "critical thinking", "time management", "adaptability", "creativity",
    "interpersonal", "organizational", "analytical", "detail oriented",
    "self motivated", "collaborative", "flexible", "motivated"
}


def extract_skill_sections(job_description: str) -> str:
    """
    Extract skill-heavy sections from job description using regex.
    
    Args:
        job_description: Raw job description text
        
    Returns:
        Combined text from skill-relevant sections
    """
    skill_text = []
    lines = job_description.split('\n')
    
    in_skill_section = False
    section_buffer = []
    
    for line in lines:
        line_stripped = line.strip()
        
        # Check if this line starts a skill section
        is_section_header = any(
            re.search(pattern, line_stripped) 
            for pattern in SKILL_SECTION_PATTERNS
        )
        
        if is_section_header:
            in_skill_section = True
            section_buffer = []
        
        # If in skill section, accumulate lines
        if in_skill_section:
            section_buffer.append(line_stripped)
            
            # End section if we hit a blank line after content
            if not line_stripped and len(section_buffer) > 1:
                skill_text.append(' '.join(section_buffer))
                in_skill_section = False
                section_buffer = []
    
    # Add any remaining buffer
    if section_buffer:
        skill_text.append(' '.join(section_buffer))
    
    # If no specific sections found, use entire description
    if not skill_text:
        skill_text.append(job_description)
    
    return ' '.join(skill_text)


def clean_and_normalize_skill(skill: str) -> str:
    """
    Normalize skill text: lowercase, remove special chars, deduplicate spaces.
    
    Args:
        skill: Raw skill text
        
    Returns:
        Normalized skill string
    """
    # Lowercase
    skill = skill.lower()
    
    # Remove special characters except dots, hyphens, pluses, sharps
    skill = re.sub(r'[^\w\s.+#-]', '', skill)
    
    # Normalize whitespace
    skill = ' '.join(skill.split())
    
    # Remove trailing/leading dots or dashes
    skill = skill.strip('.-')
    
    return skill


def extract_technical_skills(text: str) -> List[str]:
    """
    Extract technical skills using spaCy NLP and pattern matching.
    
    Args:
        text: Text to extract skills from
        
    Returns:
        List of normalized technical skills
    """
    # Process with spaCy
    doc = nlp(text)
    
    skills = set()
    
    # Extract noun phrases as potential skills
    for chunk in doc.noun_chunks:
        skill = clean_and_normalize_skill(chunk.text)
        
        # Filter out soft skills and very short/long phrases
        if (skill and 
            len(skill) >= 2 and 
            len(skill.split()) <= 4 and
            skill not in SOFT_SKILLS):
            skills.add(skill)
    
    # Extract named entities (PRODUCT, ORG) as potential tech skills
    for ent in doc.ents:
        if ent.label_ in ["PRODUCT", "ORG"]:
            skill = clean_and_normalize_skill(ent.text)
            if skill and len(skill) >= 2:
                skills.add(skill)
    
    # Pattern-based extraction for common tech terms
    # Technologies often appear in specific patterns
    tech_patterns = [
        r'\b[A-Z][a-z]+(?:\.[a-z]+)+\b',  # e.g., Node.js, React.js
        r'\b[A-Z]{2,}\b',  # e.g., AWS, SQL, API
        r'\b\w+\+\+\b',  # e.g., C++
        r'\b[Cc]#\b',  # C#
    ]
    
    for pattern in tech_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            skill = clean_and_normalize_skill(match)
            if skill:
                skills.add(skill)
    
    return list(skills)


def deduplicate_skills(skills: List[str]) -> List[str]:
    """
    Remove duplicate skills (including substring matches).
    
    Args:
        skills: List of skills
        
    Returns:
        Deduplicated list of skills
    """
    # Sort by length (longest first) to keep more specific terms
    sorted_skills = sorted(set(skills), key=len, reverse=True)
    
    unique_skills = []
    seen_tokens = set()
    
    for skill in sorted_skills:
        tokens = set(skill.split())
        
        # Check if this is a subset of already seen skills
        if not tokens.issubset(seen_tokens):
            unique_skills.append(skill)
            seen_tokens.update(tokens)
    
    return unique_skills


def extract_job_skills(job_description: str) -> List[str]:
    """
    Main function to extract technical skills from job description.
    
    Args:
        job_description: Raw job description text
        
    Returns:
        List of normalized, deduplicated technical skills
    """
    # Extract skill-relevant sections
    skill_text = extract_skill_sections(job_description)
    
    # Extract technical skills
    skills = extract_technical_skills(skill_text)
    
    # Deduplicate
    skills = deduplicate_skills(skills)
    
    # Sort alphabetically for consistency
    skills.sort()
    
    return skills
