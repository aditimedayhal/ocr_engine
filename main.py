from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from ocr_engine import process_image
import os
from typing import Optional
from pydantic import BaseModel
import shutil
import base64

app = FastAPI(
    title="OCR API",
    description="API for extracting text from images and PDFs using EasyOCR",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

class OCRResponse(BaseModel):
    text: str
    image: Optional[str] = None
    error: Optional[str] = None

@app.post("/ocr", response_model=OCRResponse)
async def ocr(
    file: UploadFile = File(...),
    language: str = Form("en")  # Default language is English
):
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Validate file type
    allowed_extensions = {'.png', '.jpg', '.jpeg', '.pdf', '.tiff'}
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Allowed types: PNG, JPG, PDF, TIFF"
        )
    
    try:
        # Save uploaded file temporarily
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process the image with specified language
        result = process_image(filepath, language)
        
        # Clean up
        os.remove(filepath)

        # Convert image bytes to base64
        image_base64 = base64.b64encode(result['image_with_boxes']).decode('utf-8')
        
        return OCRResponse(
            text=result['text'],
            image=f"data:image/png;base64,{image_base64}"
        )
    
    except Exception as e:
        # Clean up in case of error
        if os.path.exists(filepath):
            os.remove(filepath)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)