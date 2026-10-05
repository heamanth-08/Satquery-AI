# KNOWLEDGE.md — SatQuery AI Domain Reference

Background context a coding agent needs to make good decisions on this project, without re-deriving it from scratch each session.

---

## 1. Problem Statement Context

SatQuery AI answers: "Interactive Vision-Language Agent for Remote Sensing Image Analysis." The system must handle:
- Single-image visual question answering
- Single-image captioning
- Single-image grounding (locating a described feature)
- Multi-temporal (before/after) change-based VQA
- Optical + SAR paired image fusion

Final evaluation runs against VRSBench, RSVQA, and CDVQA test splits, plus a hidden ISRO evaluation set. Anything built should stay compatible with being tested against these, even though this prototype doesn't formally evaluate against them yet.

---

## 2. ISRO-Specified vs. Team-Chosen (know the difference)

| Item | Specified by ISRO? | What to use |
|---|---|---|
| Foundation dataset for image-text adaptation | Yes | BigEarthNet |
| Single-image captioning/grounding/VQA benchmark | Yes | VRSBench, RSVQA |
| Change-based VQA benchmark | Yes | CDVQA |
| Optical-SAR fusion dataset | **No — open** | SEN12MS / SEN1-2 (team's own defensible choice) |
| Specific model architecture | No — open | GeoChat / RemoteCLIP are the team's stated real-build target; Gemini-via-prompting is the honest prototype shortcut |

If asked to justify a dataset or model choice, always distinguish "ISRO required this" from "we chose this ourselves because ISRO left it open."

---

## 3. Datasets (reference only — do not bulk download)

| Dataset | Used for | Where to pull small samples |
|---|---|---|
| BigEarthNet | Foundation/adaptation reference | HF mirror `torchgeo/bigearthnet` (viewer only, ~65GB full set — never bulk download) |
| VRSBench | Captioning, grounding, VQA | HF `xiang709/VRSBench`, GitHub `lx709/VRSBench` |
| RSVQA | VQA | `rsvqa.sylvainlobry.com`, Kaggle `rsvqa-dataset` (use RSVQA-LR, not HR) |
| CDVQA | Change-based VQA | GitHub `YZHJessica/CDVQA` |
| SEN12MS / SEN1-2 | Optical-SAR pairs | Sample patches only, team's own choice |

---

## 4. Model Choice Reasoning

- **Prototype stage (now):** Gemini `gemini-2.5-flash` via `google.generativeai`, used with task-specific prompts per specialist. This is prompting-based domain simulation, not fine-tuning — this must always be described accurately, never implied to be a trained specialist model.
- **Real-build target (future, not this prototype):** GeoChat and/or RemoteCLIP, fine-tuned or adapted on BigEarthNet per the problem statement's requirement that "at least one visual or vision-language component must be fine-tuned or otherwise adapted using BigEarthNet or other open-source training data."

---

## 5. Why Gemini Flash specifically

- Free tier has generous rate limits (dozens of requests/minute — enough for a live demo)
- Native multi-image input support
- If rate-limited mid-demo, fallback options (not yet integrated, only noted): OpenRouter (free-tier vision models, OpenAI-style API), Groq (fast inference, some vision models on free tier)

---

## 6. Architecture Rationale (why it's built this way)

- **Rule-based router, not an LLM-based router:** must be deterministic and explainable in one sentence to a judge/reviewer — an LLM router would be harder to defend live and adds a point of failure with no real benefit at this stage.
- **Frontend-agnostic JSON contract:** the UI is being generated separately via Google Stitch. The backend must not assume any particular frontend, so it exposes a plain REST endpoint with a fixed response shape.
- **No GeoTIFF/geospatial handling:** genuinely out of scope for a prototype demo; PNG/JPG demonstrates the same pipeline without the setup cost.

---

## 7. Terminology Consistency

Use these terms consistently across code comments, docs, and any generated explanation:
- "Agentic Controller" — the rule-based router (not an LLM)
- "Specialist function" — one of the five task-specific wrappers (not "model," since none are actually trained/fine-tuned yet)
- "Execution trace" — the returned `{task_detected, reason, model_used}` object
- "Confidence" — self-reported or diff-percentage-derived; never call it "calibrated" or "validated"
