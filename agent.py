"""
Agentic Controller (Rule-based Router)
Routes query and image count to specialist task capabilities.
Must remain deterministic, auditable, and free of hidden LLM routing calls.
"""

def route_query(query: str, images: list) -> dict:
    q = (query or "").lower().strip()
    num_images = len(images)

    if num_images == 2:
        if any(w in q for w in ["changed", "difference", "compare", "before", "after", "change", "delta"]):
            return {
                "task": "change_detection",
                "reason": "2 images + change-related keyword"
            }
        return {
            "task": "optical_sar_fusion",
            "reason": "2 images, no change-related keyword"
        }
    
    if num_images == 1:
        if any(w in q for w in ["locate", "where is", "find", "highlight", "count", "box", "detect"]):
            return {
                "task": "grounding",
                "reason": "1 image + locate-related keyword"
            }
        if any(w in q for w in ["describe", "caption", "what does this show", "summary", "overview"]):
            return {
                "task": "caption",
                "reason": "1 image + describe-related keyword"
            }
        return {
            "task": "vqa",
            "reason": "1 image, general question"
        }

    return {
        "task": "vqa",
        "reason": f"{num_images} images provided"
    }
