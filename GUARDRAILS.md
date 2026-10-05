# GUARDRAILS.md — SatQuery AI

Hard rules for anyone (human or coding agent) building or describing this project. These exist to prevent the prototype from being oversold or misrepresented — to teammates, judges, or in the code itself.

---

## 1. Never claim fine-tuning that didn't happen

- Do not write comments, docstrings, README text, or demo narration implying any model was fine-tuned or trained in this prototype.
- The accurate description is always: "task-specific prompting on a general-purpose vision-language model (Gemini), simulating domain adaptation."
- If asked directly ("did you fine-tune a model?"), the honest answer is no — and that should be easy to say because the code says so too.

## 2. Never fabricate a confidence score as calibrated

- Confidence values must come from either (a) the model's own self-reported estimate, or (b) the image-diff percentage for change detection. Nothing else.
- Never label this confidence as "validated," "calibrated," or derived from a benchmark unless that work has actually been done.

## 3. Never claim ISRO specified something it didn't

- BigEarthNet, VRSBench, RSVQA, and CDVQA are ISRO-mandated — say so plainly.
- The optical-SAR dataset (SEN12MS/SEN1-2) was the team's own choice because ISRO left it open — never phrase this as if it were also mandated.
- Do not overstate problem-statement compliance in any generated pitch text, README, or slide content.

## 4. Never silently drop or fabricate data

- If an image fails to load, or the API call fails, surface the failure in the response (`answer`/`error` field) — never return a plausible-sounding fake answer to keep a demo looking smooth.
- Never invent ground-truth answers for demo images; use the actual Q&A pairs shipped with VRSBench/RSVQA/CDVQA where available.

## 5. Scope lock — do not silently expand scope

The following are out of scope for this build stage. A coding agent must not add them unprompted, even if it seems like an improvement:
- Model fine-tuning or training pipelines
- GeoTIFF/geospatial metadata parsing
- A frontend/UI beyond an optional local debug harness
- A database, user auth, or persistent storage
- Any new third-party API beyond Gemini (and OpenCV, which is local)

If a task seems to require one of these, stop and flag it rather than building it silently.

## 6. Never hardcode secrets

- The Gemini API key must only ever come from the `GEMINI_API_KEY` environment variable.
- Never commit a key to any file, including README examples — use a placeholder like `YOUR_KEY_HERE` in documentation.

## 7. Keep the routing logic auditable

- The Controller (`agent.py`) must remain simple, rule-based, and free of hidden LLM calls for the routing decision itself. This is the one part of the system a judge/reviewer is most likely to probe — it must stay something a teammate can explain from memory, line by line.
- Any change to routing logic must be reflected in `AGENTS.md`'s decision table in the same change.

## 8. Failure mode: don't let a broken demo look "fixed" by faking success

- If a specialist function throws, propagate a clear error rather than returning a hardcoded fallback answer that implies success.
- Do not add "if API fails, return this canned demo answer" logic — this is a hard no, since it would misrepresent the system's actual behavior live.

## 9. Documentation must stay honest under time pressure

Even when working fast under a deadline, generated docstrings, commit messages, and README updates must accurately reflect what the code does at that moment — not what it's planned to do later. Aspirational claims belong in `PRD.md`'s roadmap section, never in code-adjacent documentation describing current behavior.
