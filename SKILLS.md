# SKILLS.md — SatQuery AI Build Skills

Concrete technical capabilities required to build this project, and how each should be used. This is a reference for a coding agent deciding *how* to implement something, not *what* to implement (see `INSTRUCTIONS.md` for that).

---

## 1. Gemini Vision API calls

**Skill:** Calling `google.generativeai` with image + text input.

```python
import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

def call_vlm(images, prompt):
    if not isinstance(images, list):
        images = [images]
    response = model.generate_content([prompt] + images)
    return response.text
```

- Always pass a task-specific system-style prompt prefix per specialist — never a single generic prompt for all five functions.
- Wrap calls in a try/except; on failure, return a clear error string in `answer` and mark `trace.reason` accordingly rather than raising an unhandled exception through the API.

---

## 2. Image diffing (OpenCV)

**Skill:** Computing a visual change overlay between two images without any model.

```python
import cv2
import numpy as np

def compute_diff(image1, image2):
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(gray1, gray2)
    _, mask = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    diff_percentage = (np.count_nonzero(mask) / mask.size) * 100
    return mask, diff_percentage
```

- Use `diff_percentage` as the confidence fallback for `change_detection` when the model doesn't self-report one.
- Resize both images to matching dimensions before diffing if they differ.

---

## 3. Rule-based routing

**Skill:** Deterministic keyword + count-based decision logic (no model call).

```python
def route_query(query: str, images: list) -> dict:
    q = query.lower()
    if len(images) == 2:
        if any(w in q for w in ["changed", "difference", "compare", "before", "after"]):
            return {"task": "change_detection", "reason": "2 images + change-related keyword"}
        return {"task": "optical_sar_fusion", "reason": "2 images, no change-related keyword"}
    if any(w in q for w in ["locate", "where is", "find", "highlight"]):
        return {"task": "grounding", "reason": "1 image + locate-related keyword"}
    if any(w in q for w in ["describe", "caption", "what does this show"]):
        return {"task": "caption", "reason": "1 image + describe-related keyword"}
    return {"task": "vqa", "reason": "1 image, general question"}
```

- Keep this pure (no I/O, no API calls) so it can be unit-tested in isolation.
- The `reason` string is not cosmetic — it's returned to the caller and used to explain the decision live.

---

## 4. FastAPI endpoint with multipart image upload

**Skill:** Accepting 1–2 images + a text field in one request.

```python
from fastapi import FastAPI, UploadFile, File, Form
from typing import Optional

app = FastAPI()

@app.post("/query")
async def query(
    query: str = Form(...),
    image1: UploadFile = File(...),
    image2: Optional[UploadFile] = File(None),
):
    ...
```

- Validate image count/type here before calling the router.
- Return errors as proper HTTP 4xx responses with a JSON `{"error": "..."}` body, not as a 200 with an error string buried in `answer`.

---

## 5. Base64 image encoding (for the overlay response)

```python
import base64

def encode_image_b64(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("utf-8")
```

- Only populate `overlay_image` for `change_detection`; return `null` for all other tasks.

---

## 6. Environment/config handling

- Read `GEMINI_API_KEY` via `os.environ` — fail fast with a clear startup error if it's missing, rather than failing on the first request.
- Do not add a `.env` loader dependency unless one is already in use; a plain environment variable is sufficient for this stage.

---

## 7. Skills explicitly NOT needed for this stage

- Model fine-tuning / training loops
- GeoTIFF/Rasterio/GDAL handling
- Frontend frameworks (React, Gradio-as-delivery-UI)
- Database ORMs or migrations
- Authentication/authorization
