import easyocr

# Initialize the reader
reader = easyocr.Reader(['en'])

# Perform OCR on the image
results = reader.readtext('sample_image.png')

# Print detected text, confidence, and bounding box coordinates
for (bbox, text, prob) in results:
    print(f"Coordinates: {bbox}")
    print(f"Detected Text: '{text}'")
    print(f"Confidence: {prob:.2f}")
    print("-" * 50)
