import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Rešerš DTA Zmlúv", layout="wide")

# --- STATICKÉ DÁTA (TOTO VŽDY FUNGUJE) ---
data = [
    {"Štát": "Rakúsko", "Dividendy (%)": 5, "Licencie (%)": 5, "Zdroj": "https://www.slov-lex.sk/pravne-predpisy/SK/ZZ/1971/24/"},
    {"Štát": "Nemecko", "Dividendy (%)": 5, "Licencie (%)": 10, "Zdroj": "https://www.slov-lex.sk/pravne-predpisy/SK/ZZ/1984/18/"},
    {"Štát": "Cyprus", "Dividendy (%)": 0, "Licencie (%)": 0, "Zdroj": "https://www.slov-lex.sk/pravne-predpisy/SK/ZZ/1981/139/"},
    {"Štát": "Česko", "Dividendy (%)": 5, "Licencie (%)": 10, "Zdroj": "https://www.slov-lex.sk/pravne-predpisy/SK/ZZ/2003/137/"},
    {"Štát": "Maďarsko", "Dividendy (%)": 5, "Licencie (%)": 0, "Zdroj": "https://www.slov-lex.sk/pravne-predpisy/SK/ZZ/1996/238/"},
]

df = pd.DataFrame(data)

# --- UI ---
st.title("🔎 Moja Rešeršná Appka (Verzia 1.0)")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Nastavenia")
    vyber = st.multiselect("Vyber štáty:", df['Štát'].unique(), default=["Rakúsko", "Nemecko"])
    parameter = st.radio("Sledovať sadzbu:", ["Dividendy (%)", "Licencie (%)"])

filtered_df = df[df['Štát'].isin(vyber)]

with col2:
    fig = px.bar(filtered_df, x='Štát', y=parameter, color='Štát', text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.dataframe(filtered_df, use_container_width=True)
