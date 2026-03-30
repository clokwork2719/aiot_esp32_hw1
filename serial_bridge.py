import serial
import requests
import time
import re
import argparse

# --- Configuration ---
DEFAULT_SERIAL_PORT = "COM3"  # Change to your ESP32 serial port (e.g., /dev/ttyUSB0 on Linux)
BAUD_RATE = 115200
SERVER_URL = "http://localhost:5000/sensor"

def main():
    parser = argparse.ArgumentParser(description="AIoT Serial Bridge")
    _ = parser.add_argument("--port", type=str, default=DEFAULT_SERIAL_PORT, help="Serial port to connect to")
    args = parser.parse_args()
    
    SERIAL_PORT = str(args.port)
    print(f"[Bridge] Starting Serial Bridge on {SERIAL_PORT}...")
    
    ser = None
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Wait for connection
        
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                print(f"[Serial] {line}")
                
                # Regex to match format DATA_START|T:25.5|H:60.0|DATA_END
                match = re.search(r"DATA_START\|T:([\d\.]+)\|H:([\d\.]+)\|DATA_END", line)
                if match:
                    temp = float(match.group(1))
                    hum = float(match.group(2))
                    
                    payload = {
                        "temp": temp,
                        "humidity": hum,
                        "mac": "USB-SERIAL",
                        "ip": "127.0.0.1",
                        "device_name": "ESP32-USB-Bridge",
                        "type": "REAL"
                    }
                    
                    try:
                        resp = requests.post(SERVER_URL, json=payload)
                        if resp.status_code == 201:
                            print(f"[Bridge] Data sent to server: T={temp}, H={hum}")
                        else:
                            print(f"[Error] Server returned {resp.status_code}")
                    except Exception as e:
                        print(f"[Error] Failed to send to server: {e}")
            
            time.sleep(0.1)
                
    except Exception as e:
        print(f"[Error] Serial port error: {e}")
    finally:
        if ser is not None and ser.is_open:
            ser.close()

if __name__ == "__main__":
    main()
