import streamlit as st
from modules.ui import run_ui
from modules.persistence import load_state_from_json, save_state_to_json
from modules.config import STORAGE_FILENAME

# ---------------------- INIT ----------------------
st.set_page_config(page_title="Harmonogram slotów", layout="wide")
if not load_state_from_json(STORAGE_FILENAME):
    # Pierwsze uruchomienie - inicjalizacja w module UI
    from modules.ui import init_default_state
    init_default_state()

# ---------------------- URUCHOMIENIE UI ----------------------
run_ui()
