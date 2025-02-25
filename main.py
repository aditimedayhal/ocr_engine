from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from ocr_engine import process_image
import os
import json
from typing import Optional, Dict, Any
from pydantic import BaseModel
import shutil
import base64
import re

app = FastAPI(
    title="OCR API",
    description="API for extracting text from images and PDFs using EasyOCR with custom field extraction",
    version="1.1.0"
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
    extracted_fields: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

@app.post("/ocr", response_model=OCRResponse)
async def ocr(
    request: Request,
    file: UploadFile = File(...),
    language: str = Form("en"),
    custom_fields: Optional[str] = Form(None)
):
    # Print the form fields for debugging
    form_data = await request.form()
    print(f"All form fields: {form_data}")
    print(f"Custom fields (raw): {custom_fields}")
    
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
        # Parse custom fields if provided
        parsed_custom_fields = None
        if custom_fields:
            try:
                parsed_custom_fields = json.loads(custom_fields)
                print(f"Parsed custom fields: {parsed_custom_fields}")
            except json.JSONDecodeError as e:
                print(f"Error parsing custom fields: {e}")
                # Continue without custom fields rather than failing
        
        # Save uploaded file temporarily
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process the image with specified language and custom fields
        result = process_image(filepath, language, parsed_custom_fields)
        
        # Clean up
        os.remove(filepath)

        # Convert image bytes to base64
        image_base64 = base64.b64encode(result['image_with_boxes']).decode('utf-8')
        
        return OCRResponse(
            text=result['text'],
            image=f"data:image/png;base64,{image_base64}",
            extracted_fields=result.get('extracted_fields')
        )
    
    except Exception as e:
        # Clean up in case of error
        if os.path.exists(filepath):
            os.remove(filepath)
        print(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)