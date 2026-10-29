import random
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Ransomware Behavior Detection Simulator", page_icon="🛡️", layout="wide")
st.title("🛡️ Ransomware Behavior Detection Simulator")
st.caption("Educational simulator using synthetic file-activity events. It does not access or modify your files.")

with st.sidebar:
    st.header("Simulation settings")
    mode = st.selectbox("Activity profile", ["Mixed activity", "Normal office activity", "Suspicious burst"])
    files_per_minute = st.slider("File changes per minute", 1, 500, 180)
    entropy = st.slider("Average content entropy (0–100)", 0, 100, 78)
    extension_changes = st.slider("Files with changed extensions (%)", 0, 100, 65)
    canary_hits = st.slider("Canary-file alerts", 0, 10, 2)
    run = st.button("Run simulation", type="primary")

if "events" not in st.session_state:
    st.session_state.events = None
if run or st.session_state.events is None:
    rng = random.Random(17 if mode == "Suspicious burst" else 42)
    count = 90
    if mode == "Normal office activity":
        files_per_minute, entropy, extension_changes, canary_hits = 24, 36, 2, 0
    elif mode == "Suspicious burst":
        files_per_minute, entropy, extension_changes, canary_hits = 310, 93, 82, 5
    start = datetime.now().replace(microsecond=0) - timedelta(minutes=count)
    rows = []
    for i in range(count):
        suspicious = mode == "Suspicious burst" or (mode == "Mixed activity" and rng.random() < 0.35)
        rate = max(1, int(rng.gauss(files_per_minute if suspicious else 20, max(2, files_per_minute * 0.13))))
        ent = min(100, max(0, int(rng.gauss(entropy if suspicious else 35, 8))))
        ext = min(100, max(0, int(rng.gauss(extension_changes if suspicious else 2, 8))))
        rows.append({"Time": start + timedelta(minutes=i), "Files changed/min": rate,
                     "Entropy change": ent, "Extension changes (%)": ext,
                     "Canary hit": i < canary_hits})
    st.session_state.events = pd.DataFrame(rows)

df = st.session_state.events
avg_rate = float(df["Files changed/min"].mean())
avg_entropy = float(df["Entropy change"].mean())
avg_ext = float(df["Extension changes (%)"].mean())
canary_count = int(df["Canary hit"].sum())
score = min(100, round(0.30 * min(avg_rate / 3, 100) + 0.25 * avg_entropy + 0.25 * avg_ext + 20 * min(canary_count, 3)))
level = "High" if score >= 70 else "Elevated" if score >= 40 else "Low"

c1, c2, c3, c4 = st.columns(4)
c1.metric("Risk score", f"{score}/100", level)
c2.metric("Avg. file changes/min", f"{avg_rate:.0f}")
c3.metric("Avg. entropy indicator", f"{avg_entropy:.0f}/100")
c4.metric("Canary alerts", canary_count)

st.subheader("Synthetic activity timeline")
st.line_chart(df.set_index("Time")[["Files changed/min", "Entropy change", "Extension changes (%)"]])
st.subheader("Detection explanation")
reasons = []
if avg_rate > 100: reasons.append("High rate of file changes")
if avg_entropy > 70: reasons.append("Large change in the entropy indicator")
if avg_ext > 30: reasons.append("Many files show a simulated extension change")
if canary_count: reasons.append(f"{canary_count} simulated canary-file alert(s)")
if reasons:
    for reason in reasons: st.write(f"- {reason}")
else:
    st.success("No strong simulated indicators were observed.")
st.dataframe(df, width="stretch", hide_index=True)
st.download_button("Download simulated events as CSV", df.to_csv(index=False).encode("utf-8"),
                   "simulated_events.csv", "text/csv")
st.info("This is a classroom demonstration, not endpoint protection or a real malware detector. All events are generated in memory.")

