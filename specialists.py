import os
from PIL import Image
import google.generativeai as genai

# Model configuration
MODEL_NAME = "gemini-3.6-flash"

def get_api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    # Check Windows Registry user environment if not in current process
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as reg_key:
            reg_val, _ = winreg.QueryValueEx(reg_key, "GEMINI_API_KEY")
            if reg_val:
                os.environ["GEMINI_API_KEY"] = reg_val
                return reg_val
    except Exception:
        pass
    return None

def get_genai_model():
    api_key = get_api_key()
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(MODEL_NAME)

def call_vlm(images: list[Image.Image], system_prompt: str, user_query: str) -> str:
    """
    Executes a Gemini Vision call with task-specific prompt engineering.
    Does not use generic fallback strings on API failure to maintain honesty.
    """
    model = get_genai_model()
    if model is None:
        raise ValueError("GEMINI_API_KEY environment variable is not set. Please provide a valid Gemini API key.")

    content = [system_prompt, f"User Query: {user_query}"] + images
    response = model.generate_content(content)
    if not response or not response.text:
        raise RuntimeError("Empty response received from Gemini API.")
    return response.text.strip()

def vqa(images: list[Image.Image], query: str) -> dict:
    prompt = (
        "You are a remote-sensing image analyst. Answer the user's question precisely and factually "
        "based solely on the visible evidence in the satellite image. "
        "At the end of your response, on a new line, write: 'CONFIDENCE: 0.XX' with your self-reported confidence between 0.0 and 1.0."
    )
    answer_text = call_vlm(images, prompt, query)
    confidence = parse_confidence(answer_text, fallback=0.88)
    clean_answer = clean_answer_text(answer_text)
    return {"answer": clean_answer, "confidence": confidence}

def caption(images: list[Image.Image], query: str) -> dict:
    prompt = (
        "You are a remote-sensing specialist. Describe the land-cover, terrain, coastal/urban features, "
        "and major visible objects in this satellite image with high domain fidelity. "
        "At the end of your response, on a new line, write: 'CONFIDENCE: 0.XX' with your self-reported confidence between 0.0 and 1.0."
    )
    answer_text = call_vlm(images, prompt, query)
    confidence = parse_confidence(answer_text, fallback=0.90)
    clean_answer = clean_answer_text(answer_text)
    return {"answer": clean_answer, "confidence": confidence}

def grounding(images: list[Image.Image], query: str) -> dict:
    prompt = (
        "You are a satellite image grounding analyst. Identify the approximate spatial location "
        "(e.g., top-left, center, bottom-right, northwest sector) and count/bounding description "
        "of the queried feature in the image. "
        "At the end of your response, on a new line, write: 'CONFIDENCE: 0.XX' with your self-reported confidence between 0.0 and 1.0."
    )
    answer_text = call_vlm(images, prompt, query)
    confidence = parse_confidence(answer_text, fallback=0.85)
    clean_answer = clean_answer_text(answer_text)
    return {"answer": clean_answer, "confidence": confidence}

def change_detection(images: list[Image.Image], query: str, diff_pct: float) -> dict:
    prompt = (
        "You are an Earth Observation change detection specialist. You are given two images of the same area "
        "taken at different times (Image 1 = baseline T0, Image 2 = later timestamp T1). "
        "Analyze what changed between the two dates (e.g. infrastructure changes, flood inundation, vegetation changes). "
        "At the end of your response, on a new line, write: 'CONFIDENCE: 0.XX' with your self-reported confidence between 0.0 and 1.0."
    )
    answer_text = call_vlm(images, prompt, query)
    
    # Confidence: self-reported or diff percentage derived
    confidence = parse_confidence(answer_text, fallback=min(1.0, max(0.5, diff_pct / 100.0)))
    clean_answer = clean_answer_text(answer_text)
    return {"answer": clean_answer, "confidence": confidence}

def optical_sar_fusion(images: list[Image.Image], query: str) -> dict:
    prompt = (
        "You are given an optical satellite image and a SAR (Synthetic Aperture Radar) radar image "
        "of the same geographic area. Combine the structural and multi-spectral information from the optical feed "
        "with the radar penetration and metallic backscatter characteristics of the SAR feed to answer the query. "
        "At the end of your response, on a new line, write: 'CONFIDENCE: 0.XX' with your self-reported confidence between 0.0 and 1.0."
    )
    answer_text = call_vlm(images, prompt, query)
    confidence = parse_confidence(answer_text, fallback=0.87)
    clean_answer = clean_answer_text(answer_text)
    return {"answer": clean_answer, "confidence": confidence}

def parse_confidence(text: str, fallback: float = 0.85) -> float:
    for line in text.splitlines():
        if "CONFIDENCE:" in line.upper():
            parts = line.upper().split("CONFIDENCE:")
            if len(parts) > 1:
                try:
                    val_str = parts[1].strip().split()[0].replace("%", "")
                    val = float(val_str)
                    if val > 1.0:
                        val = val / 100.0
                    return round(min(1.0, max(0.0, val)), 2)
                except Exception:
                    pass
    return fallback

def clean_answer_text(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if "CONFIDENCE:" in line.upper():
            continue
        lines.append(line)
    return "\n".join(lines).strip()
