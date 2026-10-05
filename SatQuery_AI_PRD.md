# Product Requirements Document — SatQuery AI (Prototype)

**Problem Statement:** SatQuery AI — Interactive Vision-Language Agent for Remote Sensing Image Analysis
**Stage:** Round 2 prototype (working demo, not production)
**Team:** Helix House / SatQuery AI team

---

## 1. Purpose

Build a working prototype that lets a user upload one or two satellite/remote-sensing images, ask a natural-language question, and receive an evidence-grounded answer — routed through an agentic controller to the correct specialist capability (VQA, captioning, grounding, change detection, or optical-SAR fusion).

The prototype's job is to **prove the architecture and routing logic work end-to-end**, using a general-purpose vision-language model (Gemini) via prompting as an honest stand-in for the fine-tuned specialist models that would exist in the full build.

---

## 2. Goals for This Stage

- Demonstrate the full pipeline: input → validation → routing → model execution → combined output → execution trace
- Use real, benchmark-authentic sample images (not random photos)
- Keep the reasoning/routing logic real and explainable — this is what judges will question
- Ship something that runs live and doesn't break mid-demo

## 3. Non-Goals (explicitly out of scope for this stage)

- No fine-tuning of any model tonight
- No GeoTIFF/geospatial file handling
- No frontend build in this repo — a separate UI will be generated via Google Stitch and wired in afterward
- No persistent database or user accounts
- No production-grade error handling, auth, or deployment hardening

---

## 4. Core Capabilities (Specialist Functions)

| Capability | Trigger condition | Backing dataset (for demo images / ground truth) |
|---|---|---|
| Visual Question Answering (VQA) | 1 image, general question | VRSBench, RSVQA |
| Captioning | 1 image, "describe/what does this show" | VRSBench |
| Grounding | 1 image, "locate/find/where is" | VRSBench |
| Change Detection (change-VQA) | 2 images, "changed/compare/before-after" | CDVQA |
| Optical-SAR Fusion | 2 images, not change-related | SEN12MS / SEN1-2 (ISRO left this open) |

Dataset note: BigEarthNet is ISRO's named foundation dataset for image-text adaptation; VRSBench, RSVQA, and CDVQA are the named evaluation benchmarks. Use these specifically — not generic alternatives — since final evaluation runs on these splits plus a hidden ISRO set.

---

## 5. System Architecture

```
User Input (image(s) + text query)
        │
        ▼
Input Validator  → checks image count, format, basic sanity
        │
        ▼
Agentic Controller (rule-based router)
        │  decides task type from image count + keyword match
        ▼
Specialist Function Layer (prompt-engineered Gemini calls)
   ├── vqa()
   ├── caption()
   ├── grounding()
   ├── change_detection()  (+ OpenCV diff mask)
   └── optical_sar_fusion()
        │
        ▼
Response Composer
   → answer text + confidence estimate + execution trace
        │
        ▼
Output (returned as structured JSON / dict — frontend-agnostic)
```

Each specialist "function" is a real Python function with a genuinely distinct system prompt — not a single generic call — so the routing decision has a real effect and can be explained honestly.

---

## 6. Functional Requirements

### 6.1 Input Validation
- Accept 1 or 2 images (PNG/JPG for now)
- Reject/flag: 0 images, >2 images, unsupported file types
- Accept a free-text query string

### 6.2 Agentic Controller / Router
- Rule-based (keyword + image-count based) — must be deterministic and explainable
- Logic:
  - 2 images + change keywords ("changed", "difference", "compare", "before", "after") → `change_detection()`
  - 2 images + no change keywords → `optical_sar_fusion()`
  - 1 image + locate keywords ("locate", "where is", "find", "highlight") → `grounding()`
  - 1 image + describe keywords ("describe", "caption", "what does this show") → `caption()`
  - 1 image + anything else → `vqa()`

### 6.3 Specialist Functions
- Each wraps a single Gemini call (`gemini-2.5-flash`) with a task-specific system prompt
- `change_detection()` additionally computes an OpenCV `absdiff` + threshold mask, used both as a visual overlay and as a proxy signal
- All functions must return plain text answers usable by any frontend

### 6.4 Confidence & Execution Trace
- Confidence: either self-reported by the VLM in-response, or derived from the image-diff percentage (change detection only)
- Trace must log: which function was called, why (routing reason), and any key parameters — returned alongside the answer, not just printed to console

### 6.5 Output Contract (for the future Stitch frontend)
Return a single structured object so any frontend can consume it without backend changes:
```json
{
  "answer": "string",
  "confidence": 0.0,
  "trace": {
    "task_detected": "vqa | caption | grounding | change_detection | optical_sar_fusion",
    "reason": "string",
    "model_used": "gemini-2.5-flash"
  },
  "overlay_image": "base64 or null   // only for change_detection"
}
```

---

## 7. Tech Stack

| Layer | Choice | Why |
|---|---|---|
| VLM | Gemini `gemini-2.5-flash` via `google.generativeai` | Free tier, generous limits, native image input |
| Image diff | OpenCV (`cv2.absdiff` + threshold) | No model needed, fast, explainable |
| Backend | Single Python module, function-based (no framework needed yet) | Frontend-agnostic; Stitch will call this via a thin API layer later |
| Data | Local sample images only, no bulk dataset downloads | Speed; production data handling is out of scope |

**Note on frontend:** Since the UI will be generated separately via Google Stitch, structure the backend as plain callable functions / a thin FastAPI wrapper (a few REST endpoints: `POST /query`) rather than a Gradio-only interface — that way Stitch's frontend (or anything else) can call it over HTTP once it's ready. Keep Gradio only as an optional local debug harness, not the delivery interface.

---

## 8. Demo Data Plan

| Folder | Contents | Source |
|---|---|---|
| `/vqa_captioning/` | 5–10 images with existing Q&A/caption pairs | VRSBench, RSVQA (HF/Kaggle viewer, saved manually) |
| `/change_pairs/` | 3–5 before/after image pairs | CDVQA (GitHub repo) |
| `/sar_optical_pairs/` | A handful of paired optical+SAR patches | SEN12MS / SEN1-2 |
| `/bigearthnet_samples/` | 5–10 reference patches (not used for training tonight) | BigEarthNet (HF mirror `torchgeo/bigearthnet`) |

Use the **actual ground-truth questions** shipped with VRSBench/RSVQA/CDVQA wherever possible, instead of inventing demo questions — it makes answers verifiable live.

---

## 9. Risks & Honest Framing

| Risk | Mitigation / what to say if asked |
|---|---|
| Using a general VLM instead of a fine-tuned specialist model | "We're simulating domain adaptation through prompting for this prototype stage; the architecture is built so a fine-tuned model drops in without changing the routing or interface." |
| Confidence score isn't from a real calibrated model | "This is a simplified proxy for the prototype — self-reported/diff-based — real confidence calibration is planned for the next stage." |
| No GeoTIFF/geospatial handling yet | "Out of scope for this prototype; PNG/JPG demonstrates the same pipeline." |
| Optical-SAR dataset not specified by ISRO | "ISRO didn't mandate one for this capability, so we chose SEN12MS ourselves as a well-established benchmark." |

---

## 10. Definition of Done (for tomorrow)

- [ ] Router correctly dispatches all 5 capability types on sample inputs
- [ ] Each specialist function returns a coherent, on-topic answer
- [ ] Change detection produces a visible diff overlay
- [ ] Every response includes an execution trace (task, reason, model)
- [ ] Runs end-to-end without crashing on the prepared demo images
- [ ] Team can explain, in one sentence each, why every shortcut was taken
