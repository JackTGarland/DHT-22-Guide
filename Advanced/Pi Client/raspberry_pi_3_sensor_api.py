from flask import Flask, jsonify
import Adafruit_DHT
import time
from datetime import datetime
location = "Living Room"

app = Flask(__name__)

# DHT22 Sensor Configuration
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4  # GPIO4 - adjust if you're using a different pin

def get_sensor_reading():
    """Read temperature and humidity from DHT22 sensor"""
    try:
        # First reading (sometimes needed for sensor stabilization)
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        time.sleep(1)
        
        # Second reading (more reliable)
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        
        if humidity is not None and temperature is not None:
            return {
                "temperature": round(float(temperature), 2),
                "humidity": round(float(humidity), 2),
                "device": "raspberry_pi_3",
                "location": location,
                "timestamp": datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
            }, 200
        else:
            return {
                "error": "Failed to retrieve data from humidity sensor",
                "device": "raspberry_pi_3",
                "location": location
            }, 500
    except Exception as e:
        return {
            "error": f"Sensor reading error: {str(e)}",
            "device": "raspberry_pi_3",
            "location": location
        }, 500

@app.route('/reading', methods=['GET'])
def reading():
    """Get current temperature and humidity reading"""
    data, status_code = get_sensor_reading()
    return jsonify(data), status_code

@app.route('/', methods=['GET'])
def status():
    """Get API status"""
    return jsonify({
        "status": "Raspberry Pi 3 Sensor API Running",
        "device": "raspberry_pi_3",
        "location": location,
        "endpoints": {
            "/reading": "Get temperature and humidity data",
            "/": "Get API status"
        }
    }), 200

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    try:
        # Try to get a reading to verify sensor is working
        data, status_code = get_sensor_reading()
        if status_code == 200:
            return jsonify({
                "status": "healthy",
                "device": "raspberry_pi_3",
                "sensor": "operational"
            }), 200
        else:
            return jsonify({
                "status": "unhealthy",
                "device": "raspberry_pi_3",
                "sensor": "error",
                "error": data.get("error", "Unknown error")
            }), 503
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "device": "raspberry_pi_3",
            "sensor": "error",
            "error": str(e)
        }), 503

if __name__ == '__main__':
    print("Starting Raspberry Pi 3 Sensor API...")
    print("Device: Raspberry Pi 3")
    print("Location: "+ location)
    print("Sensor: DHT22 on GPIO4")
    print("API will be available at: http://0.0.0.0:5002")
    print("Endpoints:")
    print("  GET /reading - Get temperature and humidity")
    print("  GET / - Get API status")
    print("  GET /health - Health check")
    
    # Test sensor on startup
    print("\nTesting sensor...")
    data, status = get_sensor_reading()
    if status == 200:
        print(f"✅ Sensor test successful: {data['temperature']}°C, {data['humidity']}%")
    else:
        print(f"⚠️ Sensor test failed: {data.get('error', 'Unknown error')}")
    
    print("\nStarting Flask server...")
    app.run(host='0.0.0.0', port=5002, debug=False) 