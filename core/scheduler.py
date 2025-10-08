import random
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
import streamlit as st
from .slots import add_slot_to_brygada

def schedule_client_immediately(client_name: str, slot_type_name: str, day: date,
                                pref_start: time, pref_end: time, save: bool = True) -> Tuple[bool, Optional[Dict]]:
    """
    Znajduje najlepszy możliwy termin dla klienta w danym dniu, preferując:
    1. Sloty mieszczące się w preferencjach klienta,
    2. Sloty najbliżej początku lub końca dnia pracy brygady,
    3. Brygady o najmniejszym wykorzystaniu.
    """
    slot_type = next((s for s in st.session_state.slot_types if s["name"] == slot_type_name), None)
    if not slot_type:
        return False, None

    dur = timedelta(minutes=slot_type["minutes"])
    candidates: List[Tuple[str, datetime, datetime, bool, float, int]] = []
    # (brygada, start_dt, end_dt, in_pref, edge_priority, utilization)

    for b in st.session_state.brygady:
        existing = get_day_slots_for_brygada(b, day)
        wh_start, wh_end = st.session_state.working_hours.get(b, (DEFAULT_WORK_START, DEFAULT_WORK_END))

        # ustalenie początku/końca dnia pracy
        day_start_dt = datetime.combine(day, wh_start)
        day_end_dt = datetime.combine(day, wh_end)
        if day_end_dt <= day_start_dt:
            day_end_dt += timedelta(days=1)

        pref_start_dt = datetime.combine(day, pref_start)
        pref_end_dt = datetime.combine(day, pref_end)
        if pref_end_dt <= pref_start_dt:
            pref_end_dt += timedelta(days=1)

        t = day_start_dt
        while t + dur <= day_end_dt:
            t_end = t + dur

            # sprawdź kolizję
            overlap = any(not (t_end <= s["start"] or t >= s["end"]) for s in existing)
            if not overlap:
                # czy slot mieści się w preferencjach
                in_pref = (t >= pref_start_dt) and (t_end <= pref_end_dt)

                # dystans do krawędzi dnia pracy (im mniejszy, tym lepiej)
                dist_to_start = (t - day_start_dt).total_seconds()
                dist_to_end = (day_end_dt - t_end).total_seconds()
                edge_priority = min(dist_to_start, dist_to_end)

                # wykorzystanie brygady (ile minut już zaplanowane)
                utilization = sum(
                    s["duration_min"] for d in st.session_state.schedules.get(b, {}).values() for s in d
                )

                candidates.append((b, t, t_end, in_pref, edge_priority, utilization))
            t += timedelta(minutes=SEARCH_STEP_MINUTES)

    if not candidates:
        st.session_state.not_found_counter = st.session_state.get("not_found_counter", 0) + 1
        return False, None

    # Sortowanie:
    # 1. sloty w preferencji (True przed False),
    # 2. edge_priority (bliżej krawędzi),
    # 3. wykorzystanie (mniej obciążona brygada),
    # 4. czas rozpoczęcia (wcześniej)
    candidates.sort(key=lambda x: (
        not x[3],            # False (czyli w preferencji) ma być pierwsze
        x[4],                # odległość od krawędzi
        x[5],                # wykorzystanie brygady
        x[1]                 # czas startu
    ))

    brygada, start, end, _, _, _ = candidates[0]

    slot = {
        "id": str(uuid.uuid4()),
        "start": start,
        "end": end,
        "slot_type": slot_type_name,
        "duration_min": slot_type["minutes"],
        "client": client_name,
    }

    add_slot_to_brygada(brygada, day, slot, save=save)
    # zwracamy informację o tym, do której brygady przydzielono slot
    slot_with_meta = dict(slot)
    slot_with_meta["brygada"] = brygada
    return True, slot_with_meta
