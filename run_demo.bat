@echo off
echo Starting AIoT Demo Components (Simulation Mode)...

echo Starting Flask Server...
start "AIoT Server" python esp32_sim_server.py

echo Starting ESP32 Simulator...
start "ESP32 Sim" python esp32_sim.py

echo Starting Streamlit Dashboard...
start "AIoT Dashboard" python -m streamlit run dashboard.py --server.headless true

echo All components started!
pause
