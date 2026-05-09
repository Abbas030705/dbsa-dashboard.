import streamlit as st
import pandas as pd
import time

# Page config
st.set_page_config(page_title="DBSA Leads", layout="wide")

# Google Sheet Links
SHEET_ID = '1KmnVlRsXWOSaCGUnU9TZqtVYMcD9o2dpuaiCFDueAEU'
URLS = {
    'Split System': f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=SPLIT%20SYSTEM',
    'Hot Water': f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Hot%20Water'
}

# Auto Refresh (Is baar error handling ke sath)
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=300 * 1000, key="datarefresh")
except:
    st.warning("Auto-refresh is currently disabled. Please refresh manually.")

st.title("🚀 DBSA Live Marketing Dashboard")

# Data Loading Function
def load_data(url):
    df = pd.read_csv(url)
    df.columns = [c.lower().strip().replace(' ', '_') for c in df.columns]
    return df

# Main Tabs
tab1, tab2 = st.tabs(["Split System", "Hot Water"])

for tab, (name, url) in zip([tab1, tab2], URLS.items()):
    with tab:
        try:
            df = load_data(url)
            
            # Stats
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Leads", len(df))
            fb_count = len(df[df['platform'].str.contains('fb|facebook', case=False, na=False)])
            c2.metric("Meta Ads", fb_count)
            c3.metric("Other", len(df) - fb_count)

            # Table
            st.write(f"### Recent {name} Leads")
            # Hum sirf wo columns dikhayenge jo kaam ke hain
            cols_to_show = [col for col in ['full_name', 'campaign_name', 'platform', 'lead_status'] if col in df.columns]
            st.dataframe(df[cols_to_show].head(20), use_container_width=True)
            
        except Exception as e:
            st.error(f"Error loading {name}: Check if Sheet is public.")

st.sidebar.write(f"Last Sync: {time.strftime('%H:%M:%S')}")
