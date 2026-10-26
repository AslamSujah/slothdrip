import requests

OLLAMA = "http://localhost:11434/api/generate"
MODEL = "gemma3"  # or "gemma2"

def lazy_note(plant, p, days, temp, soil):
    water = p >= 0.5
    prompt = (
        "You are a sloth gardener who loves doing nothing. Reply with ONE short, "
        "funny sentence, max 20 words, no emojis spam.\n"
        f"Plant: {plant}. Soil: {soil}. Days since watered: {days}. Temp: {temp}C. "
        f"Probability it needs water: {p:.0%}. "
        f"Verdict: {'WATER IT' if water else 'DO NOTHING'}."
    )
    try:
        r = requests.post(OLLAMA, json={"model": MODEL, "prompt": prompt, "stream": False,
                                        "options": {"temperature": 0.7, "num_predict": 60}}, timeout=60)
        r.raise_for_status()
        return r.json()["response"].strip()
    except Exception:
        return ("Fine, a little water, then back to napping." if water
                else "Soil's fine. Go back to the hammock.")
