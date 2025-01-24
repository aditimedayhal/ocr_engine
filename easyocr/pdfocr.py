import easyocr
from pdf2image import convert_from_path
import matplotlib.pyplot as plt
import cv2
import numpy as np

# Path to your PDF
pdf_path = r'C:\PES MATERIALS\SimTech internship\CHEMSKETCH.pdf'  # Use raw string to avoid escape characters

# Convert PDF pages to images
pages = convert_from_path(pdf_path)

# Initialize the EasyOCR Reader
reader = easyocr.Reader(['en'])

# Process each page image
for page_num, page in enumerate(pages, start=1):
    # Convert the PIL image to OpenCV format (numpy array)
    page_array = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)
    
    # Perform OCR
    results = reader.readtext(page_array)
    
    # Print results for each page
    print(f"--- Page {page_num} ---")
    for (bbox, text, prob) in results:
        print(f"Text: {text}, Probability: {prob:.2f}")
        
        # Extract coordinates from bounding box
        (top_left, top_right, bottom_right, bottom_left) = bbox
        top_left = tuple(map(int, top_left))
        bottom_right = tuple(map(int, bottom_right))

        # Draw bounding box on the image
        cv2.rectangle(page_array, top_left, bottom_right, (0, 255, 0), 2)
        
        # Annotate text above the bounding box
        cv2.putText(page_array, f'{text} ({prob:.2f})', (top_left[0], top_left[1] - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Convert BGR image to RGB for visualization
    page_array = cv2.cvtColor(page_array, cv2.COLOR_BGR2RGB)
    
    # Optionally visualize the text on the page with bounding boxes
    plt.figure(figsize=(10, 10))
    plt.imshow(page_array)
    plt.title(f"Page {page_num}")
    plt.axis("off")
    plt.show()
