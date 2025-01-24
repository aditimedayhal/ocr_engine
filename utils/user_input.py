import easyocr
import logging

# Initialize logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Hardcoded list of supported languages in EasyOCR
SUPPORTED_LANGUAGES = [
    "abq", "ady", "af", "ang", "ar", "as", "ava", "az", "be", "bg", "bh", "bho",
    "bn", "bs", "ch_sim", "ch_tra", "che", "cs", "cy", "da", "dar", "de", "en",
    "es", "et", "fa", "fi", "fr", "ga", "gom", "grc", "gu", "ha", "he", "hi",
    "hr", "hu", "id", "inh", "is", "it", "ja", "jv", "ka", "kannada", "kas",
    "khm", "kn", "ko", "ku", "la", "lbe", "lez", "lij", "lt", "lv", "mah",
    "mai", "mg", "mhr", "mi", "mn", "mr", "ms", "mt", "ne", "new", "nl", "no",
    "oc", "pa", "pl", "pt", "ro", "ru", "rs_cyrillic", "rs_latin", "sanskrit",
    "si", "sk", "sl", "sq", "sr", "sv", "sw", "ta", "te", "th", "ti", "tk",
    "tl", "tr", "ug", "uk", "ur", "uz", "vi", "vo", "wo", "xh", "yi", "yo",
    "zh_cn", "zh_tw", "zu"
]

def get_user_language_selection() -> list:
    """
    Ask the user to select languages from the list of supported EasyOCR languages.
    """
    print("\nAvailable languages:")
    for idx, lang in enumerate(SUPPORTED_LANGUAGES):
        print(f"{idx + 1}. {lang}")
    
    try:
        num_languages = int(input("\nHow many languages would you like to choose? "))
        
        if num_languages < 1:
            raise ValueError("You must select at least one language.")
        
        selected_languages = []
        for _ in range(num_languages):
            lang_choice = int(input(f"Enter the number of your language choice (1-{len(SUPPORTED_LANGUAGES)}): "))
            
            if 1 <= lang_choice <= len(SUPPORTED_LANGUAGES):
                selected_languages.append(SUPPORTED_LANGUAGES[lang_choice - 1])
            else:
                raise ValueError("Invalid language choice.")
        
        logger.info(f"Selected languages: {selected_languages}")
        return selected_languages
    except ValueError as e:
        logger.error(f"Invalid input: {str(e)}")
        raise Exception("Error in selecting languages.")

def extract_text_with_easyocr(image_path: str, languages: list) -> str:
    """
    Extract text from an image using EasyOCR with the specified languages.
    """
    try:
        logger.debug(f"Initializing EasyOCR with languages: {languages}")
        reader = easyocr.Reader(languages)
        result = reader.readtext(image_path)
        
        # Extract text from the OCR result
        extracted_text = " ".join([text[1] for text in result])
        logger.debug(f"Extracted text: {extracted_text}")
        return extracted_text
    except Exception as e:
        logger.exception(f"Error extracting text from image {image_path}: {str(e)}")
        raise Exception("Error extracting text.")

def main(image_path: str):
    """
    Main function to get user language input and extract text from the image.
    """
    try:
        print("\n=== Text Extraction using EasyOCR ===")
        selected_languages = get_user_language_selection()
        
        print("\nStarting text extraction...")
        extracted_text = extract_text_with_easyocr(image_path, selected_languages)
        
        print(f"\nExtracted Text:\n{extracted_text}")
        logger.info(f"Final Extracted Text:\n{extracted_text}")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

# Image path
image_path = 'C:/PES MATERIALS/SimTech internship/project/utils/1.png'

# Run the script
if __name__ == "__main__":
    main(image_path)
1