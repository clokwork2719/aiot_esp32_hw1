# 🚀 AIoT Project - Quick Start Guide

This project provides a complete end-to-end AIoT solution including data ingestion (Flask), database (SQLite), and visualization (Streamlit). You can run it in **Simulation Mode** (no hardware needed) or with **Real Hardware** (ESP32 + DHT11).

---

## 🛠️ Step 1: Environment Setup

Before running anything, ensure you have the required dependencies installed.

1. **Create/Activate Virtual Environment**:
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. **Install Dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

---

## 🏁 Step 2: Running the Project

Choose one of the two modes below:

### Option A: Simulation Mode (Virtual ESP32)
*Great for testing without physical hardware.*

1. **Launch everything**:
   Run the following in your terminal:
   ```powershell
   .\run_demo.bat
   ```
   *(This starts the Flask server, the Simulator, and the Dashboard in separate windows.)*

### Option B: Real Hardware Mode (ESP32 + DHT11)
*Uses actual data from your ESP32 board over Serial.*

1. **Flash your ESP32**: 
   Upload the code found in `dht11_esp32/dht11_esp32.ino` to your board using the Arduino IDE.
2. **Launch everything**:
   Run the following in your terminal:
   ```powershell
   .\run_real_demo.bat
   ```
   > [!TIP]
   > If your ESP32 is NOT on `COM3`, pass the correct port as an argument:  
   > `.\run_real_demo.bat COM5`

---

## 📊 Step 3: View the Data

1. **Local Dashboard (`dashboard.py`)**: Once running, the Streamlit UI will be available at [http://localhost:8501](http://localhost:8501).
2. **Real vs Sim**: Use the navigation tabs within the local dashboard to switch between simulated and real-time sensor history!

---

## 🌐 Web Deployment (`dashboard_demo.py`)
This repository contains a separate file, `dashboard_demo.py`, designed specifically for **Streamlit Community Cloud** (or similar hosting platforms). 
- **Why two dashboards?**: `dashboard.py` relies on a live SQLite database continually updated by the background Flask server/simulator. When deployed to the web, those background services aren't running. 
- **How it works**: `dashboard_demo.py` automatically loops through the static data embedded in `aiotdb.db` and dynamically recalculates timestamps inside a sliding window of 20 observations, creating the *illusion* of a live data feed without actually needing physical sensors attached to the cloud instance!

---

## 📁 File Structure Overview
- `esp32_sim_server.py`: Flask backend that receives data.
- `dashboard.py`: Streamlit frontend for local data visualization.
- `dashboard_demo.py`: Deployment frontend simulating live updates.
- `aiotdb.py`: Database helper for reading/writing to `aiotdb.db` (SQLite).
- `esp32_sim.py`: Simulator that generates fake sensor readings.
- `serial_bridge.py`: Bridge that reads Serial data from ESP32 and sends it to the server.
