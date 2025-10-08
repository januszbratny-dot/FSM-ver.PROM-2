import streamlit as st
from config import logger
from utils.persistence import load_state_from_json, save_state_to_json
from ui.sidebar import render_sidebar
from ui.booking import render_booking_ui
from ui.tables import render_schedule_table

st.set_page_config(page_title="📅 Harmonogram Slotów", layout="wide")

if "initialized" not in st.session_state:
    load_state_from_json()

st.title("📅 Harmonogram pracy zespołów")
render_sidebar()
render_booking_ui()
render_schedule_table()

if st.button("💾 Zapisz dane"):
    save_state_to_json()
    st.success("Stan zapisany pomyślnie!")
