# AGENTS.md — SatQuery AI

This file defines the agents that make up the SatQuery AI backend and how they hand off work to one another. It is meant to be read by both humans and coding agents (e.g. Antigravity) before touching the codebase.

---

## 1. Overview

SatQuery AI is a single-agent-with-specialists system, not a multi-agent chat system. There is one **Controller Agent** that makes a routing decision, and five **Specialist Functions** it can call. None of the specialists talk to each other directly — everything flows through the Controller.

```
User → Input Validator → Controller Agent → Specialist Function → Response Composer → User
```

---

## 2. Controller Agent

**Role:** Decide which specialist capability a given request needs, based on how many images were provided and what the query is asking.

**Inputs:** `query: str`, `images: list[Image]` (length 1 or 2, pre-validated)

**Output:** a decision object: `{ "task": <name>, "reason": <string> }`

**Decision logic (deterministic, rule-based — no LLM call for routing itself):**

| Images | Query contains | Route to |
|---|---|---|
| 2 | "changed", "difference", "compare", "before", "after" | `change_detection` |
| 2 | anything else | `optical_sar_fusion` |
| 1 | "locate", "where is", "find", "highlight" | `grounding` |
| 1 | "describe", "caption", "what does this show" | `caption` |
| 1 | anything else | `vqa` |

**Non-negotiable property:** the Controller's decision must always be explainable in one sentence — this is what gets defended live in front of judges/reviewers. Do not replace this with an opaque LLM-based router unless the reasoning is also captured and returned in the trace.

---

## 3. Specialist Agents (Functions)

Each specialist is a thin wrapper around a single Gemini (`gemini-2.5-flash`) call with a distinct, task-specific system prompt. They are "agents" in the sense that each owns one job end-to-end, but they do not maintain state or call each other.

### 3.1 `vqa`
- **Job:** Answer a free-form question about a single image.
- **System prompt persona:** "You are a remote-sensing image analyst. Answer precisely and factually."

### 3.2 `caption`
- **Job:** Produce a land-cover/terrain description of a single image.
- **System prompt persona:** "Describe the land-cover, terrain, and major visible features in this satellite image."

### 3.3 `grounding`
- **Job:** Approximate the location of a described feature within a single image.
- **System prompt persona:** "Identify the approximate location (e.g. top-left, center, bottom-right) of the described feature."

### 3.4 `change_detection`
- **Job:** Compare two images of the same area at different times.
- **Extra responsibility:** compute an OpenCV `absdiff` + threshold overlay; use diff percentage as a confidence fallback if the model doesn't self-report one.

### 3.5 `optical_sar_fusion`
- **Job:** Combine an optical and a SAR image of the same area to answer a question.
- **System prompt persona:** "You are given an optical image and a SAR radar image of the same area. Combine information from both."

---

## 4. Response Composer

**Role:** Not a reasoning agent — a formatting layer. Takes the specialist's raw output plus the Controller's trace and assembles the final API response contract:

```json
{
  "answer": "string",
  "confidence": 0.0,
  "trace": { "task_detected": "string", "reason": "string", "model_used": "gemini-2.5-flash" },
  "overlay_image": "base64 or null"
}
```

---

## 5. What Agents Must NOT Do (this stage)

- No agent fine-tunes or trains a model — all specialists use prompting on a general-purpose VLM.
- No agent handles GeoTIFF or geospatial metadata — PNG/JPG only.
- No agent owns UI rendering — the frontend is built separately (Google Stitch) and consumes the JSON contract above.
- No agent silently swallows an error — validation failures and API failures must surface in the response, not just logs.

---

## 6. Extension Point (for the real/next-stage build)

When fine-tuned specialist models (GeoChat, RemoteCLIP, etc.) replace the prompted Gemini calls, only Section 3 changes — the Controller's interface, decision table, and the Response Composer's contract stay the same. Any coding agent extending this system should preserve that boundary.
