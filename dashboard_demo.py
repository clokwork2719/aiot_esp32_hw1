import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
from datetime import timedelta

# Page configuration
st.set_page_config(
    page_title="AIoT Environmental Monitor (Demo)",
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

# Database connection cached for deployment demo
@st.cache_data
def get_cached_data():
    conn = sqlite3.connect("aiotdb.db")
    # Load all data, ordered oldest to newest, to simulate time moving forward
    df = pd.read_sql_query("SELECT * FROM sensors ORDER BY id ASC", conn)
    conn.close()
    return df

# Initialize session state for sliding window offset
if 'offset' not in st.session_state:
    st.session_state.offset = 0
else:
    st.session_state.offset += 1

# Auto-refresh control
refresh_rate_sec = st.sidebar.selectbox(
    "🔄 Refresh Rate",
    options=[1, 2, 5, 10, 30],
    index=2,  # Default to 5s
    format_func=lambda x: f"{x} seconds"
)
_ = st_autorefresh(interval=refresh_rate_sec * 1000, key="datarefresh")

_ = st.title("🚀 AIoT Environmental Monitor (Deployment Demo)")
_ = st.markdown("---")

df_all = get_cached_data()

if df_all.empty:
    _ = st.info("No data available in the deployed database.")
else:
    def render_data_tab(df_subset, mode_title):
        if df_subset.empty:
            st.warning(f"No {mode_title.lower()} data available.")
            return

        window_size = 20
        total_rows = len(df_subset)
        
        start_idx = st.session_state.offset % total_rows
        end_idx = start_idx + window_size
        
        # Slicing the dataframe
        if end_idx <= total_rows:
            df_window = df_subset.iloc[start_idx:end_idx].copy()
        else:
            # Wrap around scenario
            df_window = pd.concat([df_subset.iloc[start_idx:], df_subset.iloc[:end_idx - total_rows]]).copy()
        
        # Fake timestamps replacing historical data logically
        now = pd.Timestamp.now()
        # Generate fake timestamps backwards from now, frequency based on refresh rate
        fake_times = pd.date_range(end=now, periods=window_size, freq=f'{refresh_rate_sec}s')
        df_window['timestamp'] = fake_times

        # Reverse for display so newest is at the top of the table/KPIs
        df_display = df_window.iloc[::-1].copy()
        
        # Latest data for KPIs
        latest = df_display.iloc[0]
        
        # ─── KPI Section ─────────────────────────────────────────────
        col1, col2, col3 = st.columns(3)
        with col1:
            _ = st.metric(f"{mode_title} Temp", f"{latest['temp']:.1f}°C")
        with col2:
            _ = st.metric(f"{mode_title} Humidity", f"{latest['humidity']:.1f}%")
        with col3:
            # Format string nicely
            _ = st.metric("Last Updated", latest['timestamp'].strftime('%H:%M:%S'))

        _ = st.markdown("---")

        # ─── Chart Section ───────────────────────────────────────────
        _ = st.subheader("Environmental Trends")
        
        # Combined Chart (chronological df_window)
        fig = px.line(
            df_window, 
            x="timestamp", 
            y=["temp", "humidity"],
            labels={"value": "Level", "timestamp": "Time", "variable": "Sensor"},
            color_discrete_map={"temp": "#fb7185", "humidity": "#38bdf8"},
            title="Temperature & Humidity History",
            template="plotly_dark",
            line_shape='linear'
        )
        
        _ = fig.update_layout(
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)")
        )
        
        _ = st.plotly_chart(fig, width='stretch')

        _ = st.markdown("---")

        # ─── Table Section ───────────────────────────────────────────
        _ = st.subheader("Recent Sensor Log (Latest 20)")
        
        # Convert timestamps back to string for neat dataframe display
        df_display['timestamp'] = df_display['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
        _ = st.dataframe(df_display.head(20), width='stretch')

    df_sim = df_all[df_all['type'] == 'SIMULATED']
    df_real = df_all[df_all['type'] == 'REAL']

    tab1, tab2 = st.tabs(["🎲 Random Data", "📡 Real Sensors"])

    with tab1:
        render_data_tab(df_sim, "Simulated")
        
    with tab2:
        render_data_tab(df_real, "Real")
