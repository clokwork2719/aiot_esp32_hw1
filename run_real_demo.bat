@echo off
set PORT=
if not "%~1"=="" set PORT=--port %~1

echo Starting AIoT Real Hardware Demo Components...

echo Starting Flask Server...
start "AIoT Server" python esp32_sim_server.py

echo Starting Serial Bridge...
start "Serial Bridge" cmd /k python serial_bridge.py %PORT%

echo Starting Streamlit Dashboard...
start "AIoT Dashboard" python -m streamlit run dashboard.py --server.headless true

echo All components started!
echo The dashboard will automatically reflect REAL data.
pause
