import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.express as px

# Nastavenie stránky
st.set_page_config(page_title="Rešerš DTA Zmlúv", layout="wide")

@st.cache_data
def nacitaj_data_mf_sr():
    url = "https://www.mfsr.sk/sk/dane-cla-uctovnictvo/priame-dane/dane-z-prijmu/zmluvy-zamedzeni-dvojiteho-zdanenia/zmluvy-zamedzeni-dvojiteho-zdanenia/"
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table')
        rows = table.find_all('tr')
        
        data = []
        for row in rows[1:]:
            cols = row.find_all('td')
            if len(cols) >= 2:
                stat = cols[0].get_text(strip=True)
                link = cols[1].find('a')['href'] if cols[1].find('a') else ""
                # Simulácia sadzieb pre demo (v praxi by tu bol AI extraktor)
                data.append({
                    "Štát": stat,
                    "Dividendy (%)": 5 if "A" in stat else 15,
                    "Licencie (%)": 10 if len(stat) > 7 else 0,
                    "Zdroj": "https://www.mfsr.sk" + link if not link.startswith('http') else link
                })
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Chyba pri načítaní dát: {e}")
        return pd.DataFrame()

# --- UI APLIKÁCIE ---
st.title("🔎 Inteligentná rešerš medzinárodných zmlúv")
st.markdown("Analýza zmlúv o zamedzení dvojitého zdanenia (DTA) zo zdrojov MF SR a Slov-lex.")

df = nacitaj_data_mf_sr()

if not df.empty:
    # Filtre v hornom paneli
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Filtre")
        vybrane_staty = st.multiselect("Vyberte štáty na porovnanie:", df['Štát'].unique())
        typ_prijmu = st.selectbox("Typ príjmu pre graf:", ["Dividendy (%)", "Licencie (%)"])

    # Logika filtrovania
    display_df = df[df['Štát'].isin(vybrane_staty)] if vybrane_staty else df

    with col2:
        st.subheader("Grafické porovnanie")
        fig = px.bar(display_df, x='Štát', y=typ_prijmu, color='Štát', 
                     text_auto=True, title=f"Porovnanie sadzieb: {typ_prijmu}")
        st.plotly_chart(fig, use_container_width=True)

    # Tabuľka a detail
    st.divider()
    st.subheader("Detailný prehľad zmlúv")
    st.dataframe(display_df[['Štát', 'Dividendy (%)', 'Licencie (%)', 'Zdroj']], use_container_width=True)

    if vybrane_staty:
        st.info(f"💡 Tip: Kliknutím na odkaz v stĺpci 'Zdroj' otvoríte plné znenie zmluvy na Slov-lexe.")
else:
    st.warning("Dáta sa nepodarilo načítať. Skontrolujte pripojenie na mfsr.sk.")
