import easyocr
from pdf2image import convert_from_path
import os

# Function to convert PDF to images
def process_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    image_paths = []
    for i, image in enumerate(images):
        image_path = f"./uploads/page_{i}.png"
        image.save(image_path, 'PNG')
        image_paths.append(image_path)
    return image_paths

# Function to extract text from an image using EasyOCR
def extract_text_from_image(image_path):
    reader = easyocr.Reader(['en'])  # Create EasyOCR reader for English
    result = reader.readtext(image_path)
    
    # Combine the detected text into a single string
    text = "\n".join([res[1] for res in result])
    return text
