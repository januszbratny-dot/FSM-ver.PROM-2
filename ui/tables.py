import streamlit as st
from core.analytics import get_total_usage

def render_schedule_table():
    st.subheader("📊 Harmonogram")
    for team, slots in st.session_state["teams"].items():
        st.write(f"### 👷 {team}")
        if not slots:
            st.info("Brak rezerwacji.")
        else:
            data = [
                {"Klient": s.client, "Start": s.start.strftime("%H:%M"), "Koniec": s.end.strftime("%H:%M"), "Typ": s.slot_type}
                for s in sorted(slots, key=lambda x: x.start)
            ]
            st.table(data)
    st.markdown("---")
    st.write("**Wykorzystanie:**", get_total_usage())
