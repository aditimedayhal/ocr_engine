import easyocr
import cv2
import numpy as np
import re

# Initialize the OCR reader globally (lazy loading)
reader_cache = {}

def get_reader(language):
    """Get or initialize an EasyOCR reader for the specified language"""
    if language not in reader_cache:
        reader_cache[language] = easyocr.Reader([language])
    return reader_cache[language]

def process_image(image_path, language="en", custom_fields=None):
    """
    Process an image using EasyOCR with custom field extraction

    Args:
        image_path (str): Path to the image file
        language (str): Language code for OCR
        custom_fields (dict): Dictionary mapping field names to regex patterns or keywords

    Returns:
        dict: Contains extracted text and image with bounding boxes
    """
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not load image from {image_path}")

    # Get OCR reader for the specified language
    reader = get_reader(language)

    # Perform OCR
    results = reader.readtext(img)

    # Create a copy of the image for drawing bounding boxes
    img_with_boxes = img.copy()

    # Dictionary to store field matches
    field_matches = {}

    # Initialize variables for output
    all_text = []

    # Preprocess custom fields to convert regex strings to compiled regex objects
    processed_fields = {}
    if custom_fields:
        for field_name, pattern in custom_fields.items():
            if isinstance(pattern, str) and pattern.startswith('regex:'):
                try:
                    # Compile the regex pattern
                    regex_pattern = re.compile(pattern[6:], re.IGNORECASE)
                    processed_fields[field_name] = regex_pattern
                except re.error as e:
                    print(f"Invalid regex pattern for {field_name}: {e}")
                    processed_fields[field_name] = pattern  # Keep as string if compilation fails
            else:
                processed_fields[field_name] = pattern

    # Process OCR results
    for (bbox, text, prob) in results:
        # Add all text
        all_text.append(text)

        # Default color for bounding box
        color = (0, 255, 0)  # Green

        # Check for custom field matches
        if processed_fields:
            found_match = False
            for field_name, pattern in processed_fields.items():
                # If we haven't found this field yet
                if field_name not in field_matches:
                    # Try to match based on context or pattern
                    if isinstance(pattern, str):
                        # If pattern is a string, check if it appears in the text
                        if pattern.lower() in text.lower():
                            # Found the label, now get the value from the next result
                            field_matches[field_name] = {'label_bbox': bbox, 'label_text': text}
                            color = (255, 0, 0)  # Red for field labels
                            found_match = True
                            break
                    elif hasattr(pattern, 'search'):  # Check if it's a regex pattern
                        match = pattern.search(text)
                        if match:
                            # Found the value directly
                            field_matches[field_name] = {
                                'value_bbox': bbox, 
                                'value_text': match.group(0),
                                'full_text': text
                            }
                            color = (0, 0, 255)  # Blue for field values
                            found_match = True
                            break
                elif 'label_bbox' in field_matches[field_name] and 'value_bbox' not in field_matches[field_name]:
                    # We have found a label but not yet the value
                    # Assume the next text element might be the value
                    field_matches[field_name]['value_bbox'] = bbox
                    field_matches[field_name]['value_text'] = text
                    color = (0, 0, 255)  # Blue for field values
                    found_match = True
                    break

        # Draw bounding box without text
        pts = np.array(bbox, np.int32).reshape((-1, 1, 2))
        cv2.polylines(img_with_boxes, [pts], True, color, 2)

    # Convert image with boxes to bytes
    _, buffer = cv2.imencode('.png', img_with_boxes)
    img_bytes = buffer.tobytes()

    # Format combined results
    joined_text = "\n".join(all_text)

    # Prepare extracted fields in a structured format
    extracted_fields = {}
    if custom_fields:
        for field_name, match_data in field_matches.items():
            if 'value_text' in match_data:
                extracted_fields[field_name] = match_data['value_text']

    return {
        'text': joined_text,
        'image_with_boxes': img_bytes,
        'extracted_fields': extracted_fields
    }
