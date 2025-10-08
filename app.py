import streamlit as st
from config import logger
from core.scheduler import schedule_client_immediately
from ui.sidebar import render_sidebar
from ui.booking import render_booking_ui
from utils.persistence import load_state_from_json

st.set_page_config(page_title="Harmonogram", layout="wide")

if not load_state_from_json():
    st.session_state["initialized"] = True

st.title("📅 Harmonogram slotów")
render_sidebar()
render_booking_ui()
