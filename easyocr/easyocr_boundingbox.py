import easyocr
import matplotlib.pyplot as plt
import cv2
from PIL import Image

# Initialize the reader
reader = easyocr.Reader(['en'])

# Perform OCR on the image
image_path = 'sample_image.png'
results = reader.readtext(image_path)

# Load the image with OpenCV
image = cv2.imread(image_path)

# Draw bounding boxes and annotate the image
for (bbox, text, prob) in results:
    # Extract coordinates from the bounding box
    (top_left, top_right, bottom_right, bottom_left) = bbox
    top_left = tuple(map(int, top_left))
    bottom_right = tuple(map(int, bottom_right))
   
    cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
    
    # Annotate the text above the bounding box
    cv2.putText(image, f'{text} ({prob:.2f})', (top_left[0], top_left[1] - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Display the image with bounding boxes
plt.figure(figsize=(10, 10))
plt.imshow(image)
plt.axis('off')
plt.show()
