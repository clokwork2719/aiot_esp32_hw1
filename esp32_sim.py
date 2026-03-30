import time
import requests
import random

SERVER_URL = "http://localhost:5000/sensor"
SEND_INTERVAL = 5  # seconds

# Simulated ESP32 Metadata
DEVICE_METADATA = {
    "mac": "AA:BB:CC:DD:EE:FF",
    "ip": "192.168.1.100",
    "device_name": "ESP32-DHT11-Sim"
}

def generate_sensor_data():
    """Simulate DHT11 temperature and humidity readings"""
    # Typical indoor range
    temp = round(random.uniform(22.0, 28.0), 2)
    humidity = round(random.uniform(40.0, 60.0), 2)
    return temp, humidity

def send_data():
    """Send simulated sensor data to the server via POST"""
    temp, humidity = generate_sensor_data()
    payload = {
        "temp": temp,
        "humidity": humidity,
        **DEVICE_METADATA
    }
    
    try:
        response = requests.post(SERVER_URL, json=payload, timeout=5)
        if response.status_code == 201:
            print(f"[Sim] Data sent successfully: Temp={temp}, Hum={humidity}")
        else:
            print(f"[Sim] Server returned error: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        print("[Sim] Error: Could not connect to server. Is it running?")
    except Exception as e:
        print(f"[Sim] Unexpected error: {e}")

if __name__ == "__main__":
    print(f"ESP32 Simulator starting. Sending to {SERVER_URL} every {SEND_INTERVAL}s")
    try:
        while True:
            send_data()
            time.sleep(SEND_INTERVAL)
    except KeyboardInterrupt:
        print("\n[Sim] Stopping simulator.")
