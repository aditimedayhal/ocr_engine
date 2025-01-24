# from fastapi import FastAPI, File, UploadFile, HTTPException
# from fastapi.responses import JSONResponse
# import os
# from utils.pdf_to_images import convert_pdf_to_images
# from utils.ocr_utils import detect_language, extract_text_from_image
# app = FastAPI(debug=True)

# UPLOAD_FOLDER = './uploads'
# EXTRACTED_TEXT_FOLDER = './extracted_text'
# ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(EXTRACTED_TEXT_FOLDER, exist_ok=True)

# # Helper function to check allowed file types
# def allowed_file(filename: str) -> bool:
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.post("/api/upload")
# async def upload_file(file: UploadFile = File(...)):
#     filename = file.filename
#     if not allowed_file(filename):
#         raise HTTPException(status_code=400, detail="Unsupported file type. Please upload a PDF or image.")

#     # Save uploaded file
#     file_path = os.path.join(UPLOAD_FOLDER, filename)
#     with open(file_path, "wb") as f:
#         f.write(await file.read())

#     file_extension = filename.rsplit('.', 1)[1].lower()

#     if file_extension == 'pdf':
#         # Process PDF: Convert to images and extract text
#         images = convert_pdf_to_images(file_path)
#         detected_language = None
#         all_text = ""

#         for image_path in images:
#             if not detected_language:
#                 detected_language = detect_language(image_path)
#             all_text += extract_text_from_image(image_path)

#         # Save extracted text to file
#         text_file_path = os.path.join(EXTRACTED_TEXT_FOLDER, f"{filename}_extracted.txt")
#         with open(text_file_path, "w", encoding="utf-8") as text_file:
#             text_file.write(all_text)

#         return JSONResponse({
#             "message": "PDF processed successfully.",
#             "detected_language": detected_language,
#             "extracted_text_file": text_file_path
#         })

#     else:  # Process image files
#         detected_language = detect_language(file_path)
#         extracted_text = extract_text_from_image(file_path)

#         # Save extracted text to file
#         text_file_path = os.path.join(EXTRACTED_TEXT_FOLDER, f"{filename}_extracted.txt")
#         with open(text_file_path, "w", encoding="utf-8") as text_file:
#             text_file.write(extracted_text)

#         return JSONResponse({
#             "message": "Image processed successfully.",
#             "detected_language": detected_language,
#             "extracted_text_file": text_file_path
#         })
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
import logging
from utils.pdf_to_images import convert_pdf_to_images
from utils.ocr_utils import detect_language, extract_text_from_image
import uvicorn

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(debug=True)

UPLOAD_FOLDER = './uploads'
EXTRACTED_TEXT_FOLDER = './extracted_text'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXTRACTED_TEXT_FOLDER, exist_ok=True)

# Helper function to check allowed file types
def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename
    logger.debug(f"Uploading file: {filename}")

    # Check if file extension is allowed
    if not allowed_file(filename):
        logger.error("Unsupported file type")
        raise HTTPException(status_code=400, detail="Unsupported file type. Please upload a PDF or image.")

    try:
        # Save uploaded file
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        logger.debug(f"File saved to: {file_path}")

        file_extension = filename.rsplit('.', 1)[1].lower()
        logger.debug(f"File extension: {file_extension}")

        if file_extension == 'pdf':
            images = convert_pdf_to_images(file_path)
            logger.debug(f"Converted PDF to {len(images)} images")

            detected_language = None
            all_text = ""

            for image_path in images:
                if not detected_language:
                    detected_language = detect_language(image_path)
                all_text += extract_text_from_image(image_path)

            # Save extracted text to file
            text_file_path = os.path.join(EXTRACTED_TEXT_FOLDER, f"{filename}_extracted.txt")
            with open(text_file_path, "w", encoding="utf-8") as text_file:
                text_file.write(all_text)
            logger.debug(f"Extracted text saved to: {text_file_path}")

            return JSONResponse({
                "message": "PDF processed successfully.",
                "detected_language": detected_language,
                "extracted_text_file": text_file_path
            })

        else:  # Process image files
            detected_language = detect_language(file_path)
            extracted_text = extract_text_from_image(file_path)

            # Save extracted text to file
            text_file_path = os.path.join(EXTRACTED_TEXT_FOLDER, f"{filename}_extracted.txt")
            
            with open(text_file_path, "w", encoding="utf-8") as text_file:
                text_file.write(extracted_text)
            logger.debug(f"Extracted text saved to: {text_file_path}")

            return JSONResponse({
                "message": "Image processed successfully.",
                "detected_language": detected_language,
                "extracted_text_file": text_file_path
            })

    except Exception as e:
        logger.exception(f"Error processing file {filename}: {str(e)}")
        raise HTTPException(e, status_code=500, detail="Internal Server Error")

# Run the app with uvicorn (you can define the port here)
if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)  # Set your desired port here (e.g., 8000)
