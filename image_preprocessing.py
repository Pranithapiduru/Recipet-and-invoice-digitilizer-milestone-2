import cv2
import numpy as np
from PIL import Image

def preprocess_image(pil_image: Image.Image) -> Image.Image:
    """
    SAFE preprocessing for receipts.
    No aggressive thresholding.
    """
    img = np.array(pil_image.convert("L"))

    # Normalize contrast
    img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)

    # Light denoise
    img = cv2.GaussianBlur(img, (3, 3), 0)

    return Image.fromarray(img)
