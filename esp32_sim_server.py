import time
from flask import Flask, request, jsonify
import aiotdb

app = Flask(__name__)

# Initialize database on startup
aiotdb.setup_database()

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "timestamp": time.time()}), 200

@app.route("/sensor", methods=["POST"])
def sensor_data():
    """Endpoint to receive sensor data from ESP32 simulator"""
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"status": "error", "message": "No JSON data received"}), 400
        
        temp = data.get("temp")
        humidity = data.get("humidity")
        mac = data.get("mac")
        ip = data.get("ip")
        device_name = data.get("device_name")
        data_type = data.get("type", "SIMULATED")
        
        if temp is None or humidity is None:
            return jsonify({"status": "error", "message": "Missing temperature or humidity"}), 400
        
        record_id = aiotdb.insert_data(
            temp=float(temp),
            humidity=float(humidity),
            mac=mac,
            ip=ip,
            device_name=device_name,
            data_type=data_type
        )
        
        print(f"[Server] Data received from {device_name} ({mac}) [{data_type}]: Temp={temp}, Hum={humidity}")
        
        return jsonify({
            "status": "ok",
            "id": record_id,
            "message": "Data stored successfully"
        }), 201
        
    except Exception as e:
        print(f"[Error] Failed to process sensor data: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    print("AIoT Flask Server starting on http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
