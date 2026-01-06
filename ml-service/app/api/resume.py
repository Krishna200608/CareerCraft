from fastapi import APIRouter,UploadFile,File,HTTPException
from pydantic import BaseModel

from app.services.resume_parser import extract_textpdf, extract_textdocs
from app.services.resume_analyzer import get_analysis
from app.services.ats_scorer import compute_ats_score

router = APIRouter()

class ResumeAnalyzeRequest(BaseModel):
    content: str

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
        
        return {
            "content": request.content,
            **analysis,
            **ats
        }

        
        


    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing content: {str(e)}")
