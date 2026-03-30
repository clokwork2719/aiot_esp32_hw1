# Local Python AIoT Demo Walkthrough

The AIoT demo is fully functional, with an ESP32 simulator sending data to a Flask backend, which stores it in SQLite and serves it to a Streamlit dashboard.

## Accomplishments
- **Implemented Database Layer**: `aiotdb.py` uses `aiotdb.db` and includes metadata support (MAC, IP, device name).
- **Developed Flask Backend**: `esp32_sim_server.py` handles `/sensor` (POST) and `/health` (GET) requests.
- **Created ESP32 Simulator**: `esp32_sim.py` generates realistic DHT11 data every 5 seconds.
- **Built Streamlit Dashboard**: `dashboard.py` features interactive Plotly charts, KPIs, and auto-refreshing data tables.
- **Added Deployment Dashboard**: Created `dashboard_demo.py` specifically for web deployment, featuring simulated scrolling data and dynamic fake timestamps.
- **Enhanced Settings**: Both dashboards now have a User-controllable refresh rate dropdown.
- **Environment Management**: Project uses `uv` for seamless dependency management and script execution.

## Verification Results
- **Connectivity**: ESP32 simulator successfully posts to the Flask server (HTTP 201).
- **Data Persistence**: Data is confirmed stored in `aiotdb.db`.
- **Dashboard**: Streamlit UI is live and displaying real-time updates.

## How to Run
All components are currently running in the background. To restart them manually, use the following commands:

```powershell
# In three separate terminals:
uv run python esp32_sim_server.py
uv run python esp32_sim.py
```powershell
# For the Real Hardware / Local Simulator Dashboard:
python -m streamlit run dashboard.py --server.headless true

# For the Web Deployment Demo Dashboard:
python -m streamlit run dashboard_demo.py --server.headless true
```

## URLs
- **Health**: [http://localhost:5000/health](http://localhost:5000/health)
- **Streamlit Dashboard (Local)**: [http://localhost:8501](http://localhost:8501)
- **Streamlit Dashboard (Demo)**: Ensure it runs on a separate port or stop the local one first.

---

Enjoy your local AIoT simulation!
