from pdf2image import convert_from_path
import subprocess
import os
import json

pdf_path = r'C:\PES MATERIALS\SimTech internship\CHEMSKETCH.pdf'

# Convert the PDF to images
images = convert_from_path(pdf_path)

image_dir = r'C:\PES MATERIALS\SimTech internship\imagess'
os.makedirs(image_dir, exist_ok=True)

# Process each image and perform OCR
for i, image in enumerate(images):
    # Save the image
    image_path = os.path.join(image_dir, f'page_{i+1}.png')
    image.save(image_path, 'PNG')
    
    # Run PaddleOCR on the image and capture the output
    result = subprocess.run(
        ['paddleocr', '--image_dir', image_dir, '--lang', 'en'],
        capture_output=True, text=True
    )
   
    print(f"Raw output for page {i+1}:")
    print(result.stdout)
    print(result.stderr)
    
