# SlothDrip

Offline-first automated garden moisture predictor for Hacktoberfest “Slow and Steady”.

## Stack
- Streamlit (UI)
- SQLite (offline log persistence)
- TabPFN (tabular prediction)
- Gemma via Ollama (short action note generation)

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
ollama pull gemma3
streamlit run app.py
```

Open the local URL shown by Streamlit (usually `http://localhost:8501`).

## Notes
- First TabPFN run may download model assets.
- If Ollama/Gemma is unavailable, the app falls back to a canned note.
