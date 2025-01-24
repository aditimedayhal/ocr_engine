# import pytesseract
# from PIL import Image
# import logging
# import easyocr
# image_path = 'Screenshot.png'

# logger = logging.getLogger(__name__)

# def detect_language(image_path: str) -> str:
#     try:
#         img = Image.open(image_path)
#         osd_result = pytesseract.image_to_osd(img)
#         language = osd_result['language']
#         logger.debug(f"Detected language: {language}")
#         return language
#     except Exception as e:
#         logger.exception(f"Error detecting language in image {image_path}: {str(e)}")
#         raise Exception("Error detecting language.")

# def extract_text_from_image(image_path: str) -> str:
#     try:
#         img = Image.open(image_path)

#         # Use Tesseract to detect the language first
#         language = detect_language(image_path)
#         print(language)
#         logger.debug(f"Detected language: {language}. Initializing EasyOCR for text extraction.")

#         # Initialize EasyOCR dynamically based on the detected language
#         reader = easyocr.Reader([language])  # Use the detected language only for OCR

#         # Use EasyOCR to extract text
#         result = reader.readtext(image_path, lang=language)
        
#         # Extract the text from the result
#         extracted_text = " ".join([text[1] for text in result])  # Join the OCR results
#         print(extracted_text)

#         logger.debug(f"Extracted text from image {image_path}: {extracted_text[:50]}...")  # Display first 50 chars for logging
#         return extracted_text
#     except Exception as e:
#         logger.exception(f"Error extracting text from image {image_path}: {str(e)}")
#         raise Exception("Error extracting text from image.")
# import pytesseract
# from PIL import Image
# import logging
# import easyocr

# # Initialize logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

# # Image path
# image_path = 'C:/PES MATERIALS/SimTech internship/project/utils/sample_image.png'

# def detect_language_with_tesseract(image_path: str) -> str:
#     """
#     Detect the language of the text in an image using Tesseract OSD.
#     """
#     try:
#         img = Image.open(image_path)
#         osd_result = pytesseract.image_to_osd(img, output_type=pytesseract.Output.DICT)
        
#         logger.debug(f"OSD Result: {osd_result}")
        
#         # Extract the script (language) information
#         script = osd_result.get('script', 'eng')  # Default to 'eng' (English) if not detected
#         logger.debug(f"Detected script (language): {script}")
#         return script
#     except Exception as e:
#         logger.exception(f"Error detecting language in image {image_path}: {str(e)}")
#         raise Exception("Error detecting language.")

# def extract_text_with_easyocr(image_path: str, language: str) -> str:
#     """
#     Extract text from an image using EasyOCR, with the specified language.
#     """
#     try:
#         logger.debug(f"Initializing EasyOCR with language: {language}")
#         reader = easyocr.Reader([language])  # Initialize EasyOCR with detected language
        
#         result = reader.readtext(image_path)
        
#         # Extract text from the OCR result
#         extracted_text = " ".join([text[1] for text in result])  # Combine the extracted text
#         logger.debug(f"Extracted text: {extracted_text}")
#         return extracted_text
#     except Exception as e:
#         logger.exception(f"Error extracting text from image {image_path}: {str(e)}")
#         raise Exception("Error extracting text.")

# def main(image_path: str):
#     """
#     Main function to detect language using Tesseract and extract text using EasyOCR.
#     """
#     try:
#         logger.info("Starting language detection...")
#         language = detect_language_with_tesseract(image_path)
        
#         easyocr_language = language_map.get(language, 'en')  # Default to English if not mapped
        
#         logger.info(f"Language detected: {language}. Using EasyOCR language code: {easyocr_language}.")
        
#         logger.info("Starting text extraction...")
#         extracted_text = extract_text_with_easyocr(image_path, easyocr_language)
        
#         logger.info(f"Final Extracted Text:\n{extracted_text}")
#         print(f"\nFinal Extracted Text:\n{extracted_text}")
#     except Exception as e:
#         logger.error(f"An error occurred: {str(e)}")

# # Run the script
# if __name__ == "__main__":
#     main(image_path)

#language detection using tesseract and easyocr to detect text
'''
import pytesseract
from PIL import Image
import logging
import easyocr

# Initialize logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Image path
image_path = 'C:/PES MATERIALS/SimTech internship/project/utils/1.png'

def detect_language_with_tesseract(image_path: str) -> str:
    """
    Detect the language of the text in an image using Tesseract OSD.
    """
    try:
        img = Image.open(image_path)
        osd_result = pytesseract.image_to_osd(img, output_type=pytesseract.Output.DICT)
        
        logger.debug(f"OSD Result: {osd_result}")
        
        # Extract the script (language) information
        script = osd_result.get('script', 'eng')  # Default to 'eng' (English) if not detected
        logger.debug(f"Detected script (language): {script}")
        return script
    except Exception as e:
        logger.exception(f"Error detecting language in image {image_path}: {str(e)}")
        raise Exception("Error detecting language.")

def extract_text_with_easyocr(image_path: str, language: str) -> str:
    """
    Extract text from an image using EasyOCR, with the specified language.
    """
    try:
        logger.debug(f"Initializing EasyOCR with language: {language}")
        reader = easyocr.Reader([language])  # Initialize EasyOCR with detected language
        
        result = reader.readtext(image_path)
        
        # Extract text from the OCR result
        extracted_text = " ".join([text[1] for text in result])  # Combine the extracted text
        logger.debug(f"Extracted text: {extracted_text}")
        return extracted_text
    except Exception as e:
        logger.exception(f"Error extracting text from image {image_path}: {str(e)}")
        raise Exception("Error extracting text.")

def main(image_path: str):
    """
    Main function to detect language using Tesseract and extract text using EasyOCR.
    """
    try:
        logger.info("Starting language detection...")
        language = detect_language_with_tesseract(image_path)
    
        logger.info(f"Language detected: {language}. Using EasyOCR language code: {language}.")
        
        logger.info("Starting text extraction...")
        extracted_text = extract_text_with_easyocr(image_path, language)
        
        logger.info(f"Final Extracted Text:\n{extracted_text}")
        print(f"\nFinal Extracted Text:\n{extracted_text}")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

# Run the script
if __name__ == "__main__":
    main(image_path)
'''
import pytesseract
from PIL import Image
import logging
import easyocr
from langdetect import detect

# Initialize logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Image path
image_path = 'C:/PES MATERIALS/SimTech internship/project/utils/1.png'

def extract_text_with_tesseract(image_path: str) -> str:
    """
    Extract text from an image using Tesseract OCR.
    """
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        
        logger.debug(f"Extracted text with Tesseract: {text}")
        return text
    except Exception as e:
        logger.exception(f"Error extracting text from image {image_path}: {str(e)}")
        raise Exception("Error extracting text.")

def detect_language_with_langdetect(text: str) -> str:
    """
    Detect the language of the extracted text using langdetect.
    """
    try:
        language = detect(text)
        logger.debug(f"Detected language using langdetect: {language}")
        return language
    except Exception as e:
        logger.exception(f"Error detecting language: {str(e)}")
        raise Exception("Error detecting language.")

def extract_text_with_easyocr(image_path: str, language: str) -> str:
    """
    Extract text from an image using EasyOCR, with the specified language.
    """
    try:
        logger.debug(f"Initializing EasyOCR with language: {language}")
        reader = easyocr.Reader([language])  # Initialize EasyOCR with detected language
        
        result = reader.readtext(image_path)
        
        # Extract text from the OCR result
        extracted_text = " ".join([text[1] for text in result])  # Combine the extracted text
        logger.debug(f"Extracted text with EasyOCR: {extracted_text}")
        return extracted_text
    except Exception as e:
        logger.exception(f"Error extracting text from image {image_path}: {str(e)}")
        raise Exception("Error extracting text.")

def main(image_path: str):
    """
    Main function to detect language using langdetect and extract text using EasyOCR.
    """
    try:
        logger.info("Starting text extraction with Tesseract...")
        text = extract_text_with_tesseract(image_path)
        
        logger.info("Starting language detection with langdetect...")
        language = detect_language_with_langdetect(text)
        
        logger.info(f"Language detected: {language}.")
        
        logger.info("Starting text extraction with EasyOCR...")
        extracted_text = extract_text_with_easyocr(image_path, language)
        
        logger.info(f"Final Extracted Text:\n{extracted_text}")
        print(f"\nFinal Extracted Text:\n{extracted_text}")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

# Run the script
if __name__ == "__main__":
    main(image_path)
