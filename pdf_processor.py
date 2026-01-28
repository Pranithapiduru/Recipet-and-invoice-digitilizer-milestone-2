from pdf2image import convert_from_bytes
from typing import List
from PIL import Image

# 🔴 UPDATE THIS PATH IF YOU MOVE POPPLER
POPPLER_PATH = r"C:\Users\p.pranitha\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin"


def pdf_to_images(pdf_bytes: bytes) -> List[Image.Image]:
    """
    Convert PDF bytes into list of PIL Images using Poppler
    """
    images = convert_from_bytes(
        pdf_bytes,
        poppler_path=POPPLER_PATH
    )
    return images
