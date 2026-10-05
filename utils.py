import base64
import cv2
import numpy as np
from PIL import Image
import io


def compute_diff(image1_bytes: bytes, image2_bytes: bytes) -> tuple[str, float]:
    """
    Computes an OpenCV absdiff and threshold difference mask between two images.
    Returns (overlay_image_base64, diff_percentage).
    """
    nparr1 = np.frombuffer(image1_bytes, np.uint8)
    nparr2 = np.frombuffer(image2_bytes, np.uint8)
    img1 = cv2.imdecode(nparr1, cv2.IMREAD_COLOR)
    img2 = cv2.imdecode(nparr2, cv2.IMREAD_COLOR)

    if img1 is None or img2 is None:
        raise ValueError("Could not decode one or both images for diff computation")

    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    diff = cv2.absdiff(gray1, gray2)
    _, mask = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

    diff_percentage = float((np.count_nonzero(mask) / mask.size) * 100)

    # Create red alpha diff mask overlay on top of img2
    overlay = img2.copy()
    red_mask = np.zeros_like(img2)
    red_mask[:, :] = (0, 0, 255)  # Red in BGR

    change_indices = mask > 0
    overlay[change_indices] = cv2.addWeighted(
        img2[change_indices], 0.4, red_mask[change_indices], 0.6, 0
    )

    success, encoded_img = cv2.imencode(".png", overlay)
    if not success:
        raise ValueError("Failed to encode overlay image to PNG")

    overlay_b64 = f"data:image/png;base64,{base64.b64encode(encoded_img.tobytes()).decode('utf-8')}"
    return overlay_b64, round(diff_percentage, 2)


def encode_image_b64(image_bytes: bytes, mime_type: str = "image/png") -> str:
    """Encodes raw image bytes to a data URL string."""
    b64 = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:{mime_type};base64,{b64}"
