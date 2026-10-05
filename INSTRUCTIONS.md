# INSTRUCTIONS.md — SatQuery AI Backend Build

Instructions for any coding agent (or human) building this repository.

---

## 1. Objective

Build a working, frontend-agnostic backend for SatQuery AI: a FastAPI service that accepts 1–2 remote-sensing images plus a text query, routes the request to the correct specialist function, and returns a structured JSON answer with a confidence score and execution trace.

This is a **prototype for a hackathon round**, not a production system. Optimize for: it runs correctly end-to-end, the logic is explainable, and nothing crashes mid-demo.

---

## 2. Scope Boundaries

**Build:**
- FastAPI app with a single `POST /query` endpoint
- Rule-based controller/router (see `AGENTS.md`)
- Five specialist functions wrapping Gemini `gemini-2.5-flash` calls
- OpenCV-based image diff for change detection
- A structured JSON response contract (see `AGENTS.md` §4)

**Do NOT build:**
- Any frontend, HTML, or Gradio UI as the delivery interface (a debug-only Gradio harness is optional, but never the shipped interface)
- GeoTIFF/geospatial file parsing
- A database, user accounts, or auth
- Model fine-tuning or training code of any kind
- Bulk dataset download scripts — sample images are provided locally, already downloaded by the team

---

## 3. File Structure to Produce

```
/main.py            FastAPI app + the /query route
/agent.py           route_query() — the controller from AGENTS.md
/specialists.py     vqa, caption, grounding, change_detection, optical_sar_fusion
/utils.py           image diff helper (OpenCV), base64 encode/decode helpers
/requirements.txt
/README.md          how to run locally + curl test examples
```

Keep it to these files. Do not introduce extra abstraction layers, config frameworks, or folders unless a file genuinely can't fit its purpose otherwise.

---

## 4. Build Order

1. `specialists.py` — get one function (`vqa`) calling Gemini and returning text. Confirm it works before writing the rest.
2. `utils.py` — image diff helper, tested standalone on two sample images.
3. `agent.py` — the rule-based router, pure logic, no I/O. Unit-testable without calling any API.
4. `main.py` — wire validator → router → specialist → response composer into the `/query` endpoint.
5. `requirements.txt` and `README.md` last, once the app actually runs.

---

## 5. Configuration

- Gemini API key must be read from the environment variable `GEMINI_API_KEY`. Never hardcode a key or commit one.
- Model name (`gemini-2.5-flash`) should be a single named constant, not repeated as a string in five places.

---

## 6. Validation Rules (enforce in `main.py` before routing)

- Reject 0 images or more than 2 images with a clear 4xx error and message.
- Accept only PNG/JPG.
- Reject an empty query string.

---

## 7. Testing Expectations

Before calling this "done," verify manually with the team's sample images:
- 1 image + a general question → `vqa`
- 1 image + "describe this" → `caption`
- 1 image + "where is X" → `grounding`
- 2 images + "what changed" → `change_detection`, overlay image returned
- 2 images + a fusion-style question → `optical_sar_fusion`

Every one of the above must return a non-empty `answer` and a populated `trace`.

---

## 8. Honesty Requirements

Any code comments, README text, or agent-generated explanation must be accurate about what this system does:
- State clearly that specialists are prompted general-purpose VLM calls, not fine-tuned models.
- State clearly that confidence is self-reported or diff-based, not a calibrated model output.
- Do not use language implying training, fine-tuning, or GeoTIFF support happened if it didn't.

See `GUARDRAILS.md` for the full list of things not to claim or fabricate.
