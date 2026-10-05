# SatQuery AI - Orbital Vision-Language Mission Control

SatQuery AI is a state-of-the-art vision-language AI system designed to analyze satellite imagery. 
This repository is organized into a professional modular monorepo containing both the frontend user interfaces and the backend AI services.

## Repository Structure

- `/frontend`: Contains the web-based mission control interfaces and UI variations.
- `/backend`: Contains the Python backend logic including AI agents, specialists, FastAPI endpoints, and environment configurations.
- `docs` / `markdown files`: Guardrails, Skills, Knowledge base, PRDs, etc.

## Setup & Execution

### Backend
1. Navigate to the `backend` directory.
2. Ensure you have Python installed.
3. Install dependencies: `pip install -r requirements.txt`
4. Create a `.env` file and set the required API keys.
5. Run the application: `python main.py` or through your ASGI server.

### Frontend
1. Navigate to the `frontend` directory.
2. The frontends are generally static HTML/CSS/JS or use local dev servers depending on the sub-project.
3. For the `satquery_ai_vision_language_mission_control`, open `index.html` in your browser or run a local static server.

## Deployment
- **Frontend** can be automatically deployed to GitHub Pages via the `gh-pages` branch.
- **Backend** can be containerized and deployed on standard cloud platforms like AWS, GCP, Azure, or Render.
