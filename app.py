import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="Kita-Verteiler", page_icon="🧒")
st.title("🧒 Kindergarten Platz-Verteiler")

with st.sidebar:
    st.header("⚙️ Einstellungen")
    namen_raw = st.text_area("Namen der Kinder (pro Zeile):", 
                             value="\n".join([f"Kind_{i:02d}" for i in range(1, 21)]), height=250)
    tage_liste = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
    auswahl_tage = st.multiselect("Offene Tage wählen:", tage_liste, default=["Dienstag", "Mittwoch", "Donnerstag", "Freitag"])
    max_plaetze = st.number_input("Max. Kinder pro Tag:", min_value=1, value=10)
    start = st.button("🚀 Verteilung berechnen", use_container_width=True)

if start:
    kinder = [n.strip() for n in namen_raw.split('\n') if n.strip()]
    if not kinder or not auswahl_tage:
        st.error("Bitte Namen eingeben und Tage wählen!")
    else:
        pool = []
        for tag in auswahl_tage:
            pool.extend([tag] * max_plaetze)
        random.shuffle(pool)
        ergebnis = {tag: [] for tag in auswahl_tage}
        stats = {kind: 0 for kind in kinder}
        for kind in kinder:
            garantie = len(pool) // len(kinder)
            while stats[kind] < garantie:
                idx = next((i for i, t in enumerate(pool) if t is not None and kind not in ergebnis[t]), -1)
                if idx != -1:
                    t_name = pool[idx]; ergebnis[t_name].append(kind); stats[kind] += 1; pool[idx] = None
                else: break
        rest = [p for p in pool if p is not None]
        random.shuffle(rest)
        for tag in rest:
            moegliche = [k for k in kinder if k not in ergebnis[tag]]
            if moegliche:
                wahl = min(moegliche, key=lambda x: stats[x])
                ergebnis[tag].append(wahl); stats[wahl] += 1
        cols = st.columns(len(auswahl_tage))
        for i, tag in enumerate(auswahl_tage):
            with cols[i]:
                st.info(f"**{tag}**")
                for k in sorted(ergebnis[tag]): st.write(f"▫️ {k}")
        st.divider()
        st.subheader("📊 Statistik")
        st.dataframe(pd.DataFrame(list(stats.items()), columns=["Kind", "Tage"]), use_container_width=True)
