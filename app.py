import pandas as pd
import streamlit as st
import db
from model import SOILS, predict_water
from llm import lazy_note

st.set_page_config(page_title="SlothDrip", page_icon="🦥")
st.title("🦥 SlothDrip")
st.caption("Offline garden moisture predictor. Laziness, rewarded.")

c1, c2 = st.columns(2)
with c1:
    plant = st.text_input("Plant", "Tomatoes")
    days = st.slider("Days since watered", 0.0, 14.0, 3.0, 0.5)
    soil = st.selectbox("Soil type", list(SOILS))
with c2:
    temp = st.slider("Avg temp (°C)", 0, 45, 24)
    hum = st.slider("Humidity (%)", 0, 100, 50)

if st.button("Should I water?", type="primary"):
    with st.spinner("Sloth is thinking..."):
        p = predict_water(days, temp, hum, soil)
        note = lazy_note(plant, p, days, temp, soil)
    verdict = "💧 WATER" if p >= 0.5 else "😴 DO NOTHING"
    (st.error if p >= 0.5 else st.success)(f"{verdict}  (confidence water needed: {p:.0%})")
    st.write(note)
    st.session_state["last"] = (plant, days, temp, hum, soil, p, verdict, note)
    db.add_log(plant, days, temp, hum, soil, p, verdict, note)

if "last" in st.session_state and st.button("I watered it (reset)"):
    pl, _, t, h, s, p, v, n = st.session_state["last"]
    db.add_log(pl, 0, t, h, s, p, "WATERED", "Logged watering.", True)
    st.toast("Logged!")

st.subheader("Field log")
rows = db.get_logs()
if rows:
    st.dataframe(pd.DataFrame(rows, columns=["time", "plant", "days", "temp", "hum", "soil", "p_water", "verdict", "note", "watered"]),
                 use_container_width=True)
