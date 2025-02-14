import easyocr
import uvicorn
from PIL import Image
from pdf2image import convert_from_path
import os
from typing import List, Dict
import numpy as np
import cv2

class OCREngine:
    def __init__(self):
        """Initialize the OCR engine with a cache for readers."""
        self.readers: Dict[str, easyocr.Reader] = {}
    
    def get_reader(self, language: str) -> easyocr.Reader:
        """Get or create a reader for the specified language."""
        if language not in self.readers:
            # For some languages, English is added as secondary language for better recognition
            languages = [language]
            if language != 'en':
                languages.append('en')
            self.readers[language] = easyocr.Reader(languages)
        return self.readers[language]

    def preprocess_image(self, image_path: str) -> str:
        """Preprocess image for better OCR accuracy."""
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise Exception("Failed to load image")
        
        # Apply adaptive thresholding
        binary_image = cv2.adaptiveThreshold(
            image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(binary_image)
        
        temp_path = "preprocessed.png"
        cv2.imwrite(temp_path, denoised)
        return temp_path

    def process_image_file(self, image_path: str, language: str) -> dict:
        """Process a single image file."""
        try:
            # Preprocess the image
            preprocessed_path = self.preprocess_image(image_path)
            
            # Get reader for specified language
            reader = self.get_reader(language)
            
            # Read the original image for drawing boxes
            image = cv2.imread(preprocessed_path)
            
            # Perform OCR
            result = reader.readtext(preprocessed_path)
            
            # Draw bounding boxes
            for bbox, text, conf in result:
                # Convert bbox points to integers
                bbox = [[int(x) for x in point] for point in bbox]
                
                # Draw rectangle
                cv2.rectangle(
                    image,
                    (bbox[0][0], bbox[0][1]),
                    (bbox[2][0], bbox[2][1]),
                    (0, 255, 0),  # Green color
                    2  # Thickness
                )
            
            # Save the image with bounding boxes
            output_path = "temp_output.png"
            cv2.imwrite(output_path, image)
            
            # Read the image as bytes
            with open(output_path, "rb") as f:
                image_bytes = f.read()
            
            # Clean up
            if os.path.exists(preprocessed_path):
                os.remove(preprocessed_path)
            if os.path.exists(output_path):
                os.remove(output_path)
            
            # Return both text and image bytes
            return {
                'text': ' '.join([text[1] for text in result]),
                'image_with_boxes': image_bytes
            }
        except Exception as e:
            raise Exception(f"Error processing image: {str(e)}")

    def process_pdf_file(self, pdf_path: str, language: str) -> dict:
        """Process a PDF file by converting to images first."""
        try:
            images = convert_from_path(pdf_path, dpi=300, thread_count=4)
            full_text = []
            first_page_boxes = None
            
            for i, image in enumerate(images):
                temp_path = f'temp_page_{i}.png'
                image.save(temp_path)
                
                result = self.process_image_file(temp_path, language)
                full_text.append(result['text'])
                
                # Keep the first page's image with boxes
                if i == 0:
                    first_page_boxes = result['image_with_boxes']
                
                # Clean up temporary file
                os.remove(temp_path)
            
            return {
                'text': '\n\n'.join(full_text),
                'image_with_boxes': first_page_boxes
            }
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")
        
# Create a global OCR engine instance
ocr_engine = OCREngine()

def process_image(filepath: str, language: str = 'en') -> str:
    """Process an image or PDF file and extract text."""
    try:
        if filepath.lower().endswith('.pdf'):
            return ocr_engine.process_pdf_file(filepath, language)
        else:
            return ocr_engine.process_image_file(filepath, language)
    except Exception as e:
        raise Exception(f"OCR processing error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)