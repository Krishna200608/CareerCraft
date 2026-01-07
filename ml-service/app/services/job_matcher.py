"""
Job Matcher Service
Computes job-fit score and generates improvement feedback based on skill matching.
"""

from typing import List, Dict
from app.services.job_skill_extractor import extract_job_skills
from app.services.semantic_skill_matcher import (
    semantic_skill_matching,
    compute_skill_match_percentage
)


# Weight for skill match in overall job-fit score
SKILL_MATCH_WEIGHT = 0.85
ATS_SCORE_WEIGHT = 0.15


def compute_job_fit_score(
    skill_match_percentage: float,
    ats_score: float
) -> int:
    """
    Compute overall job-fit score combining skill match and ATS score.
    
    Args:
        skill_match_percentage: Skill match percentage (0-100)
        ats_score: ATS score from resume analysis (0-100)
        
    Returns:
        Job-fit score (0-100)
    """
    weighted_score = (
        skill_match_percentage * SKILL_MATCH_WEIGHT +
        ats_score * ATS_SCORE_WEIGHT
    )
    
    return round(weighted_score)


def generate_feedback(
    matched_skills: List[str],
    partial_matches: List[str],
    missing_skills: List[str],
    skill_match_percentage: float,
    jd_skill_count: int
) -> List[str]:
    """
    Generate deterministic, rule-based feedback for job matching.
    
    Args:
        matched_skills: List of matched skills
        partial_matches: List of partially matched skills
        missing_skills: List of missing skills
        skill_match_percentage: Overall skill match percentage
        jd_skill_count: Total number of skills in job description
        
    Returns:
        List of feedback strings
    """
    feedback = []
    
    # Rule 1: Address missing skills (high priority)
    if len(missing_skills) > 0:
        if len(missing_skills) >= 5:
            # Many missing skills - provide grouped feedback
            skill_groups = group_skills_by_category(missing_skills)
            
            if skill_groups:
                for category, skills in list(skill_groups.items())[:2]:  # Top 2 categories
                    skill_list = ', '.join(skills[:3])  # Top 3 skills in category
                    feedback.append(
                        f"Add {category}-related skills such as {skill_list} to improve job alignment."
                    )
            else:
                # No clear grouping - list top missing skills
                top_missing = ', '.join(missing_skills[:4])
                feedback.append(
                    f"Add key skills such as {top_missing} to better match job requirements."
                )
        else:
            # Few missing skills - list them specifically
            skill_list = ', '.join(missing_skills)
            feedback.append(
                f"Consider adding {skill_list} to your resume to meet all job requirements."
            )
    
    # Rule 2: Address partial matches (medium priority)
    if len(partial_matches) > 0 and len(partial_matches) <= 4:
        # List specific partial matches that need strengthening
        for skill in partial_matches[:2]:  # Top 2 partial matches
            feedback.append(
                f"Strengthen {skill} proficiency through hands-on projects or practical experience."
            )
    elif len(partial_matches) > 4:
        # Many partial matches - general guidance
        feedback.append(
            "Strengthen your proficiency in partially matched skills through practical projects and real-world applications."
        )
    
    # Rule 3: Low overall match percentage
    if skill_match_percentage < 40:
        feedback.append(
            "Your skill set shows significant gaps for this role. Focus on acquiring core technical skills listed in the job description."
        )
    elif skill_match_percentage < 60:
        feedback.append(
            "Consider targeted upskilling in missing areas to improve your candidacy for this position."
        )
    
    # Rule 4: No matched skills at all
    if len(matched_skills) == 0 and jd_skill_count > 0:
        feedback.append(
            "Your resume shows minimal alignment with this job's technical requirements. Review the job description carefully and highlight relevant experience."
        )
    
    # Rule 5: Good match but can improve
    if skill_match_percentage >= 70 and len(missing_skills) > 0:
        top_missing = ', '.join(missing_skills[:2])
        feedback.append(
            f"You have a strong skill match. Adding {top_missing} would make you an even stronger candidate."
        )
    
    # Ensure minimum 2 feedback points if possible
    if len(feedback) < 2 and (len(missing_skills) > 0 or len(partial_matches) > 0):
        if len(missing_skills) > 0:
            feedback.append(
                "Focus on acquiring missing technical skills through online courses, certifications, or projects."
            )
        elif len(partial_matches) > 0:
            feedback.append(
                "Build practical projects that demonstrate your proficiency in the required technologies."
            )
    
    # If still no feedback and everything is good
    if len(feedback) == 0:
        feedback.append(
            "Your skills align well with the job requirements. Ensure your resume clearly demonstrates your experience with these technologies."
        )
        feedback.append(
            "Consider highlighting specific projects or achievements that showcase your expertise in the matched skills."
        )
    
    return feedback


def group_skills_by_category(skills: List[str]) -> Dict[str, List[str]]:
    """
    Group skills into broad categories for better feedback.
    
    Args:
        skills: List of skills
        
    Returns:
        Dictionary of category -> skills
    """
    categories = {
        "cloud": [],
        "devops": [],
        "database": [],
        "frontend": [],
        "backend": [],
        "mobile": [],
        "data science": [],
        "testing": [],
    }
    
    # Keyword-based categorization
    category_keywords = {
        "cloud": ["aws", "azure", "gcp", "cloud", "s3", "ec2", "lambda"],
        "devops": ["docker", "kubernetes", "jenkins", "ci/cd", "terraform", "ansible"],
        "database": ["sql", "mongodb", "postgresql", "mysql", "redis", "database"],
        "frontend": ["react", "angular", "vue", "html", "css", "javascript", "typescript"],
        "backend": ["node", "express", "django", "flask", "fastapi", "spring", "api"],
        "mobile": ["android", "ios", "flutter", "react native", "swift", "kotlin"],
        "data science": ["python", "machine learning", "tensorflow", "pytorch", "pandas", "numpy"],
        "testing": ["selenium", "jest", "pytest", "testing", "junit"],
    }
    
    for skill in skills:
        skill_lower = skill.lower()
        categorized = False
        
        for category, keywords in category_keywords.items():
            if any(keyword in skill_lower for keyword in keywords):
                categories[category].append(skill)
                categorized = True
                break
        
        # If not categorized, add to a general category
        if not categorized:
            if "general" not in categories:
                categories["general"] = []
            categories["general"].append(skill)
    
    # Remove empty categories
    return {k: v for k, v in categories.items() if v}


def match_job_with_resume(
    resume_analysis: Dict,
    job_description: str
) -> Dict:
    """
    Main function to match job description with resume analysis.
    
    Args:
        resume_analysis: Resume analysis output from /analyze endpoint
        job_description: Raw job description text
        
    Returns:
        Job matching results with score and feedback
    """
    # Extract resume skills and ATS score
    resume_skills = resume_analysis.get("skills", [])
    ats_score = resume_analysis.get("ats_score", 0)
    
    # Extract skills from job description
    jd_skills = extract_job_skills(job_description)
    
    # Perform semantic matching
    match_results = semantic_skill_matching(resume_skills, jd_skills)
    
    matched_skills = match_results["matched_skills"]
    partial_matches = match_results["partial_matches"]
    missing_skills = match_results["missing_skills"]
    
    # Compute skill match percentage
    skill_match_percentage = compute_skill_match_percentage(
        matched_count=len(matched_skills),
        partial_count=len(partial_matches),
        total_jd_skills=len(jd_skills)
    )
    
    # Compute overall job-fit score
    job_fit_score = compute_job_fit_score(skill_match_percentage, ats_score)
    
    # Generate feedback
    job_feedback = generate_feedback(
        matched_skills=matched_skills,
        partial_matches=partial_matches,
        missing_skills=missing_skills,
        skill_match_percentage=skill_match_percentage,
        jd_skill_count=len(jd_skills)
    )
    
    return {
        "job_fit_score": job_fit_score,
        "skill_match_percentage": skill_match_percentage,
        "matched_skills": matched_skills,
        "partial_matches": partial_matches,
        "missing_skills": missing_skills,
        "job_feedback": job_feedback
    }
