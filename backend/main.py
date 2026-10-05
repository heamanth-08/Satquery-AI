import io
import os
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image

import agent
import specialists
import utils

app = FastAPI(
    title="SatQuery AI Backend",
    description="Interactive Vision-Language Agent for Remote Sensing Image Analysis",
    version="1.0.0"
)

# Step 3: Enable CORS Middleware for local frontend origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all local origins including file://, localhost:3000, 5173, 8080
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_IMAGE_TYPES = {"image/png", "image/jpeg", "image/jpg"}

@app.get("/")
def health_check():
    return {
        "status": "online",
        "service": "SatQuery AI",
        "model": specialists.MODEL_NAME,
        "gemini_api_key_configured": bool(specialists.get_api_key())
    }

@app.post("/query")
async def query_endpoint(
    query: str = Form(None),
    image1: Optional[UploadFile] = File(None),
    image2: Optional[UploadFile] = File(None)
):
    # Enforce strict validation rules
    if not query or not query.strip():
        raise HTTPException(
            status_code=400,
            detail="Query string cannot be empty. Please provide a question or instruction."
        )

    if image1 is None:
        raise HTTPException(
            status_code=400,
            detail="At least one image (image1) is required."
        )

    # Validate image MIME types
    uploaded_files = [image1]
    if image2 is not None:
        uploaded_files.append(image2)

    for idx, img_file in enumerate(uploaded_files, start=1):
        content_type = (img_file.content_type or "").lower()
        filename = (img_file.filename or "").lower()
        is_valid_type = (
            content_type in ALLOWED_IMAGE_TYPES or
            filename.endswith(".png") or
            filename.endswith(".jpg") or
            filename.endswith(".jpeg")
        )
        if not is_valid_type:
            raise HTTPException(
                status_code=415,
                detail=f"Unsupported file type for image{idx}: {img_file.content_type or filename}. Only PNG and JPEG images are supported."
            )

    # Read image bytes
    try:
        image1_bytes = await image1.read()
        pil_images = [Image.open(io.BytesIO(image1_bytes)).convert("RGB")]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process image1: {str(e)}")

    image2_bytes = None
    if image2 is not None:
        try:
            image2_bytes = await image2.read()
            pil_images.append(Image.open(io.BytesIO(image2_bytes)).convert("RGB"))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to process image2: {str(e)}")

    # Route request deterministically via Agentic Controller
    route_decision = agent.route_query(query, pil_images)
    task = route_decision["task"]
    reason = route_decision["reason"]

    overlay_image = None
    diff_pct = 0.0

    # Execute change diff if change_detection
    if task == "change_detection" and image2_bytes is not None:
        try:
            overlay_image, diff_pct = utils.compute_diff(image1_bytes, image2_bytes)
        except Exception as e:
            overlay_image = None
            diff_pct = 0.0

    # Call specialist function
    try:
        if task == "change_detection":
            res = specialists.change_detection(pil_images, query, diff_pct)
        elif task == "optical_sar_fusion":
            res = specialists.optical_sar_fusion(pil_images, query)
        elif task == "grounding":
            res = specialists.grounding(pil_images, query)
        elif task == "caption":
            res = specialists.caption(pil_images, query)
        else: # vqa
            res = specialists.vqa(pil_images, query)

        answer = res.get("answer", "")
        confidence = float(res.get("confidence", 0.88))
    except Exception as e:
        # Guardrail compliance: do not hide error with fake answers
        error_msg = str(e)
        if "GEMINI_API_KEY" in error_msg:
            raise HTTPException(status_code=500, detail=error_msg)
        raise HTTPException(status_code=502, detail=f"VLM specialist call failed: {error_msg}")

    # Assemble final output contract
    response_payload = {
        "answer": answer,
        "confidence": confidence,
        "trace": {
            "task_detected": task,
            "reason": reason,
            "model_used": specialists.MODEL_NAME
        },
        "overlay_image": overlay_image
    }

    return JSONResponse(status_code=200, content=response_payload)
