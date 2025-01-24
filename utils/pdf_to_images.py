from pdf2image import convert_from_path
import logging

logger = logging.getLogger(__name__)

def convert_pdf_to_images(pdf_path: str):
    try:
        images = convert_from_path(pdf_path)
        image_paths = []
        for idx, image in enumerate(images):
            image_path = f"image_{idx}.png"
            image.save(image_path, "PNG")
            image_paths.append(image_path)
        logger.debug(f"PDF converted to {len(images)} images.")
        return image_paths
    except Exception as e:
        logger.exception(f"Error converting PDF {pdf_path} to images: {str(e)}")
        raise Exception("Error converting PDF to images.")
