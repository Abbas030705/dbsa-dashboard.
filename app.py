import streamlit as st
import pandas as pd
import time

# Dashboard ki settings
st.set_page_config(page_title="DBSA Live Dashboard", layout="wide")

# Google Sheet CSV Links (Jo aapne pehle nikaale thay)
SHEET_ID = '1KmnVlRsXWOSaCGUnU9TZqtVYMcD9o2dpuaiCFDueAEU'
URLS = {
    'Split System': f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=SPLIT%20SYSTEM',
    'Hot Water': f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Hot%20Water'
}

# --- Styling ---
st.markdown("""
    <style>
    .main { background-color: #020617; }
    div[data-testid="stMetricValue"] { color: #a855f7; font-weight: bold; }
    </style>
    """, unsafe_allow_index=True)

st.title("🚀 DBSA Marketing Performance")
st.write("Live Data - Har 5 minute mein khud update hota hai.")

# --- Auto Refresh Logic ---
# Ye line page ko har 300 seconds (5 min) baad reload karegi
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=300 * 1000, key="datarefresh")

def load_data(url):
    df = pd.read_csv(url)
    df.columns = [c.lower().strip().replace(' ', '_') for c in df.columns]
    return df

# --- Dashboard Layout ---
tab1, tab2 = st.tabs(["Split System", "Hot Water"])

for tab, (name, url) in zip([tab1, tab2], URLS.items()):
    with tab:
        try:
            df = load_data(url)
            
            # Stats Cards
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Leads", len(df))
            fb_count = len(df[df['platform'].str.contains('fb|facebook', case=False, na=False)])
            col2.metric("Meta Ads", fb_count)
            col3.metric("Other Platforms", len(df) - fb_count)

            # Table
            st.subheader(f"Recent {name} Leads")
            st.dataframe(df[['full_name', 'campaign_name', 'platform', 'lead_status']].head(10), use_container_width=True)
            
        except Exception as e:
            st.error(f"Data load nahi ho saka: {e}")

st.info(f"Last Updated: {time.strftime('%H:%M:%S')}")
