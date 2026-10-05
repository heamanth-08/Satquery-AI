# SatQuery AI — Vision-Language Mission Control

Interactive Vision-Language Agent for Remote Sensing Image Analysis.

## System Architecture

```
User Input (image(s) + text query)
        │
        ▼
Input Validator (PNG/JPEG format, 1–2 images, non-empty query)
        │
        ▼
Agentic Controller (`agent.py`)
        │  deterministic rule-based routing
        ▼
Specialist Functions (`specialists.py`)
   ├── vqa()
   ├── caption()
   ├── grounding()
   ├── change_detection() (+ OpenCV diff overlay)
   └── optical_sar_fusion()
        │
        ▼
Response Composer (`main.py`)
        │
        ▼
Output JSON Contract (consumed by Google Stitch Frontend)
```

## Running Locally

### 1. Requirements

Install python dependencies:
```bash
pip install -r requirements.txt
```

Set your Gemini API Key:
```bash
# Windows PowerShell
$env:GEMINI_API_KEY="YOUR_KEY_HERE"

# Linux / macOS
export GEMINI_API_KEY="YOUR_KEY_HERE"
```

### 2. Start the Backend Service

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
The FastAPI backend runs at `http://127.0.0.1:8000`. API documentation is available at `http://127.0.0.1:8000/docs`.

### 3. Serve the Mission Control Frontend

```bash
python -m http.server 3000 --directory "Frontend/satquery_ai_vision_language_mission_control"
```
Open `http://localhost:3000/code.html` in your browser.

## Contract Specification

`POST /query` expects multipart/form-data:
- `query`: Text string (required)
- `image1`: PNG or JPEG image file (required)
- `image2`: PNG or JPEG image file (optional, required for Change Detection / Optical-SAR Fusion)

Response contract:
```json
{
  "answer": "string",
  "confidence": 0.0,
  "trace": {
    "task_detected": "vqa | caption | grounding | change_detection | optical_sar_fusion",
    "reason": "string",
    "model_used": "gemini-2.5-flash"
  },
  "overlay_image": "data:image/png;base64,... or null"
}
```

## Curl Testing Examples

Single image VQA:
```bash
curl -X POST "http://127.0.0.1:8000/query" \
  -F "query=What is visible in the harbor?" \
  -F "image1=@samples/t0.png"
```

Two images Change Detection:
```bash
curl -X POST "http://127.0.0.1:8000/query" \
  -F "query=What changed between Image 1 and Image 2?" \
  -F "image1=@samples/t0.png" \
  -F "image2=@samples/t1.png"
```
