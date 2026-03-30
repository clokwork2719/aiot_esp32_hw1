#include <WiFi.h>
#include <HTTPClient.h>
#include <SimpleDHT.h>

// --- Configuration ---
const char* ssid = "YourSSID";         // Replace with your WiFi SSID
const char* password = "YourPassword"; // Replace with your WiFi Password
const char* serverUrl = "http://192.168.1.100:5000/sensor"; // Replace with your Flask server IP

#define DHTPIN 25          // Digital pin connected to the DHT sensor
#define MODE_PIN 0        // Pin to toggle between WiFi (HIGH) and USB (LOW) - Optional

SimpleDHT11 dht;

void setup() {
  Serial.begin(115200);
  
  pinMode(MODE_PIN, INPUT_PULLUP);

  Serial.println("ESP32 DHT11 AIoT Node Starting...");
}

void sendViaWiFi(float t, float h) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    String jsonPayload = "{\"temp\": " + String(t) + 
                         ", \"humidity\": " + String(h) + 
                         ", \"mac\": \"" + WiFi.macAddress() + "\"" +
                         ", \"ip\": \"" + WiFi.localIP().toString() + "\"" +
                         ", \"device_name\": \"ESP32-Real-Sensor\"" +
                         ", \"type\": \"REAL\"}";

    int httpResponseCode = http.POST(jsonPayload);
    
    if (httpResponseCode > 0) {
      Serial.print("WiFi POST Success: ");
      Serial.println(httpResponseCode);
    } else {
      Serial.print("WiFi POST Error: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  } else {
    Serial.println("WiFi Disconnected. Reconnecting...");
    WiFi.begin(ssid, password);
  }
}

void sendViaUSB(float t, float h) {
  // Simple JSON-like output for Serial Bridge
  Serial.print("DATA_START|T:");
  Serial.print(t);
  Serial.print("|H:");
  Serial.print(h);
  Serial.println("|DATA_END");
}

void loop() {
  delay(1000); // Read every 5 seconds

  byte temperature = 0;
  byte humidity = 0;
  int err = SimpleDHTErrSuccess;
  
  if ((err = dht.read(DHTPIN, &temperature, &humidity, NULL)) != SimpleDHTErrSuccess) {
    Serial.print("Failed to read from DHT sensor! err=");
    Serial.println(err);
    return;
  }

  float h = (float)humidity;
  float t = (float)temperature;

  // Determine mode: If WiFi is connected, prefer WiFi. Otherwise, USB.
  // Or use a physical switch if available (MODE_PIN).
  
  if (WiFi.status() == WL_CONNECTED) {
    sendViaWiFi(t, h);
  } else {
    // Attempt WiFi connection if not connected (background)
    if (WiFi.status() != WL_CONNECTED && String(ssid) != "YourSSID") {
       WiFi.begin(ssid, password);
    }
  }
  
  // Always output to USB as well, so bridge can pick it up if needed
  sendViaUSB(t, h);
}
