import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# Page configuration
st.set_page_config(
    page_title="AIoT Environmental Monitor",
    page_icon="🚀",
    layout="wide",
)

# Custom CSS for premium look and high contrast
_ = st.markdown("""
    <style>
    .main {
        background-color: #0f172a;
    }
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 1.1rem !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
    }
    .stMetric {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 25px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    /* Specific accent colors for metrics */
    div[data-testid="stMetric"]:nth-child(1) { border-left: 5px solid #fb7185; }
    div[data-testid="stMetric"]:nth-child(2) { border-left: 5px solid #38bdf8; }
    div[data-testid="stMetric"]:nth-child(3) { border-left: 5px solid #a855f7; }
    </style>
    """, unsafe_allow_html=True)

# Database connection
def get_data():
    conn = sqlite3.connect("aiotdb.db")
    df = pd.read_sql_query("SELECT * FROM sensors ORDER BY timestamp DESC LIMIT 100", conn)
    conn.close()
    return df

# Auto-refresh control
refresh_rate_sec = st.sidebar.selectbox(
    "🔄 Refresh Rate",
    options=[1, 2, 5, 10, 30],
    index=2,  # Default to 5s
    format_func=lambda x: f"{x} seconds"
)
_ = st_autorefresh(interval=refresh_rate_sec * 1000, key="datarefresh")

_ = st.title("🚀 AIoT Environmental Monitor")
_ = st.markdown("---")

# Fetch data
df_all = get_data()

if df_all.empty:
    _ = st.info("No data available yet. Please ensure the ESP32 Simulator and Server are running.")
else:
    # Split into SIMULATED and REAL
    df_sim = df_all[df_all['type'] == 'SIMULATED']
    df_real = df_all[df_all['type'] == 'REAL']

    tab1, tab2 = st.tabs(["🎲 Random Data", "📡 Real Sensors"])

    with tab1:
        if df_sim.empty:
            st.warning("No simulated data yet.")
        else:
            # Latest data for KPIs
            latest = df_sim.iloc[0]
            
            # --- KPI Section ---
            col1, col2, col3 = st.columns(3)
            with col1:
                _ = st.metric("Temperature", f"{latest['temp']:.1f}°C")
            with col2:
                _ = st.metric("Humidity", f"{latest['humidity']:.1f}%")
            with col3:
                _ = st.metric("Last Updated", latest['timestamp'].split(" ")[1])

            st.markdown("---")
            
            # --- Chart ---
            fig = px.line(
                df_sim, 
                x="timestamp", 
                y=["temp", "humidity"],
                labels={"value": "Level", "timestamp": "Time", "variable": "Sensor"},
                color_discrete_map={"temp": "#fb7185", "humidity": "#38bdf8"},
                title="Simulated Trend",
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            st.subheader("Recent Simulated Logs")
            st.dataframe(df_sim.head(20), use_container_width=True)

    with tab2:
        if df_real.empty:
            st.warning("No real sensor data yet. Connect your ESP32 via WiFi or USB Serial Bridge.")
        else:
            # Latest data for KPIs
            latest_r = df_real.iloc[0]
            
            # --- KPI Section ---
            col1, col2, col3 = st.columns(3)
            with col1:
                _ = st.metric("Real Temp", f"{latest_r['temp']:.1f}°C")
            with col2:
                _ = st.metric("Real Humidity", f"{latest_r['humidity']:.1f}%")
            with col3:
                _ = st.metric("Last Updated", latest_r['timestamp'].split(" ")[1])

            st.markdown("---")
            
            # --- Chart ---
            fig_r = px.line(
                df_real, 
                x="timestamp", 
                y=["temp", "humidity"],
                labels={"value": "Level", "timestamp": "Time", "variable": "Sensor"},
                color_discrete_map={"temp": "#fb7185", "humidity": "#38bdf8"},
                title="Real Sensor Trend",
                template="plotly_dark"
            )
            st.plotly_chart(fig_r, use_container_width=True)
            
            st.markdown("---")
            st.subheader("Real Sensor Logs")
            st.dataframe(df_real.head(20), use_container_width=True)

