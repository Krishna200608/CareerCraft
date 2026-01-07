from fastapi import APIRouter,UploadFile,File,HTTPException
from pydantic import BaseModel
from typing import List, Optional

from app.services.resume_parser import extract_textpdf, extract_textdocs
from app.services.resume_analyzer import get_analysis
from app.services.ats_scorer import compute_ats_score
from app.services.job_matcher import match_job_with_resume

router = APIRouter()

class ResumeAnalyzeRequest(BaseModel):
    content: str

class JobMatchRequest(BaseModel):
    resume_analysis: dict
    job_description: str

@router.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):

    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="Unable to access the filename")
        
        extension = file.filename.split(".")[-1].lower()

        #read
        content = await file.read()

        if extension=='pdf':
            text = extract_textpdf(content)
        elif extension == "docx":
            text = extract_textdocs(content)
        else:
            raise HTTPException(status_code=422, detail="Unsupported file format. Please upload PDF or DOCX.")
        
        if file.content_type not in (
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ):
            raise HTTPException(status_code=422, detail="Invalid file type")
        
        return{
            "filename": file.filename,
            "text": text.strip()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@router.post("/analyze")
async def analyze_text(request: ResumeAnalyzeRequest):
    try:
        content = request.content

        analysis = get_analysis(content)
        ats = compute_ats_score(analysis, content)

        analysis.pop("raw_sections")
        
        return {
            **analysis,
            **ats
        }

        
        


    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing content: {str(e)}")


@router.post("/job-match")
async def job_match(request: JobMatchRequest):
    """
    Match job description with resume analysis to compute job-fit score.
    
    Expects:
        - resume_analysis: Output from /analyze endpoint (with 'skills' and 'ats_score')
        - job_description: Raw job description text
    
    Returns:
        - job_fit_score: Overall job fit score (0-100)
        - skill_match_percentage: Skill alignment percentage
        - matched_skills: Skills that match the job
        - partial_matches: Skills that partially match
        - missing_skills: Skills missing from resume
        - job_feedback: Actionable improvement suggestions
    """
    try:
        # Validate input
        if not request.resume_analysis:
            raise HTTPException(
                status_code=400,
                detail="resume_analysis is required"
            )
        
        if not request.job_description or not request.job_description.strip():
            raise HTTPException(
                status_code=400,
                detail="job_description cannot be empty"
            )
        
        # Validate resume_analysis has required fields
        if "skills" not in request.resume_analysis:
            raise HTTPException(
                status_code=400,
                detail="resume_analysis must contain 'skills' field"
            )
        
        if "ats_score" not in request.resume_analysis:
            raise HTTPException(
                status_code=400,
                detail="resume_analysis must contain 'ats_score' field"
            )
        
        # Perform job matching
        result = match_job_with_resume(
            resume_analysis=request.resume_analysis,
            job_description=request.job_description
        )
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error performing job match: {str(e)}"
        )
