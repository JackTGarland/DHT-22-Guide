from flask import Flask, request, jsonify, render_template_string
import requests
import threading
import time
from datetime import datetime

app = Flask(__name__)

# Store the latest readings from both devices
latest_readings = {
    "pico_w": {
        "timestamp": None,
        "temperature": None,
        "humidity": None,
        "location": "Office",
        "status": "offline"
    },
    "raspberry_pi_3": {
        "timestamp": None,
        "temperature": None,
        "humidity": None,
        "location": "Living Room",
        "status": "offline"
    }
}

# Configuration for devices, follow the structure and add as many devices as you want.
PICO_W_IP = "staticIPhere"  # Change this to your Pico W's IP address
PICO_W_PORT = 5001

RASPBERRY_PI_3_IP = "staticIPhere"  # Change this to your Raspberry Pi 3's IP address
RASPBERRY_PI_3_PORT = 5002

def fetch_pico_w_reading():
    """Fetch reading from Pico W"""
    try:
        response = requests.get(
            f"http://{PICO_W_IP}:{PICO_W_PORT}/reading",
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            # Add timestamp from when we received the response
            ts = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
            latest_readings["pico_w"]["timestamp"] = ts
            latest_readings["pico_w"]["temperature"] = data["temperature"]
            latest_readings["pico_w"]["humidity"] = data["humidity"]
            latest_readings["pico_w"]["status"] = "online"
            print(f"Successfully fetched Pico W reading: {data}")
        else:
            latest_readings["pico_w"]["status"] = "error"
            print(f"Failed to fetch Pico W reading: {response.status_code}")
    except Exception as e:
        latest_readings["pico_w"]["status"] = "offline"
        print(f"Error fetching Pico W reading: {e}")

def fetch_raspberry_pi_3_reading():
    """Fetch reading from Raspberry Pi 3"""
    try:
        response = requests.get(
            f"http://{RASPBERRY_PI_3_IP}:{RASPBERRY_PI_3_PORT}/reading",
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            # Add timestamp from when we received the response
            ts = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
            latest_readings["raspberry_pi_3"]["timestamp"] = ts
            latest_readings["raspberry_pi_3"]["temperature"] = data["temperature"]
            latest_readings["raspberry_pi_3"]["humidity"] = data["humidity"]
            latest_readings["raspberry_pi_3"]["status"] = "online"
            print(f"Successfully fetched Raspberry Pi 3 reading: {data}")
        else:
            latest_readings["raspberry_pi_3"]["status"] = "error"
            print(f"Failed to fetch Raspberry Pi 3 reading: {response.status_code}")
    except Exception as e:
        latest_readings["raspberry_pi_3"]["status"] = "offline"
        print(f"Error fetching Raspberry Pi 3 reading: {e}")

def background_fetch():
    """Background thread to fetch readings from both devices every 5 minutes"""
    while True:
        print("Fetching readings from both devices...")
        fetch_pico_w_reading()
        fetch_raspberry_pi_3_reading()
        time.sleep(300)  # 5 minutes = 300 seconds

# Start background thread for fetching readings
fetch_thread = threading.Thread(target=background_fetch, daemon=True)
fetch_thread.start()

@app.route('/api/latest', methods=['GET'])
def get_latest_json():
    """API endpoint to get latest readings in JSON format"""
    return jsonify(latest_readings)

@app.route('/api/pico-w', methods=['GET'])
def get_pico_w_reading():
    """API endpoint to get latest Pico W reading"""
    return jsonify(latest_readings["pico_w"])

@app.route('/api/raspberry-pi-3', methods=['GET'])
def get_raspberry_pi_3_reading():
    """API endpoint to get latest Raspberry Pi 3 reading"""
    return jsonify(latest_readings["raspberry_pi_3"])

@app.route('/api/force-fetch', methods=['POST'])
def force_fetch():
    """Force immediate fetch from both devices"""
    fetch_pico_w_reading()
    fetch_raspberry_pi_3_reading()
    return jsonify({"status": "Fetch completed", "readings": latest_readings})

@app.route('/', methods=['GET'])
def show_dashboard():
    """Main dashboard showing all sensor readings"""
    html = '''
    <html>
    <head>
        <title>Temperature & Humidity Dashboard</title>
        <meta http-equiv="refresh" content="60">
        <style>
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                margin: 0; 
                padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            .header {
                text-align: center;
                color: white;
                margin-bottom: 30px;
            }
            .header h1 {
                margin: 0;
                font-size: 2.5em;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .header p {
                margin: 10px 0 0 0;
                opacity: 0.9;
            }
            .devices-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .device-card {
                background: white;
                border-radius: 15px;
                padding: 25px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                transition: transform 0.3s ease;
            }
            .device-card:hover {
                transform: translateY(-5px);
            }
            .device-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
                padding-bottom: 15px;
                border-bottom: 2px solid #f0f0f0;
            }
            .location {
                font-size: 1.5em;
                font-weight: bold;
                color: #333;
            }
            .device-title {
                font-size: 0.9em;
                color: #666;
                font-style: italic;
            }
            .status {
                padding: 5px 12px;
                border-radius: 20px;
                font-size: 0.8em;
                font-weight: bold;
                text-transform: uppercase;
            }
            .status.online { background: #d4edda; color: #155724; }
            .status.offline { background: #f8d7da; color: #721c24; }
            .status.error { background: #fff3cd; color: #856404; }
            .reading {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin: 15px 0;
                padding: 15px;
                background: #f8f9fa;
                border-radius: 10px;
            }
            .reading-label {
                font-weight: bold;
                color: #555;
            }
            .reading-value {
                font-size: 1.2em;
                font-weight: bold;
            }
            .temperature { color: #e74c3c; }
            .humidity { color: #3498db; }
            .timestamp {
                text-align: center;
                margin-top: 20px;
                padding: 10px;
                background: #e9ecef;
                border-radius: 8px;
                font-size: 0.9em;
                color: #666;
            }
            .controls {
                text-align: center;
                margin-top: 30px;
            }
            .btn {
                background: #007bff;
                color: white;
                border: none;
                padding: 12px 25px;
                border-radius: 25px;
                cursor: pointer;
                font-size: 1em;
                margin: 0 10px;
                transition: background 0.3s ease;
            }
            .btn:hover {
                background: #0056b3;
            }
            .footer {
                text-align: center;
                margin-top: 30px;
                color: white;
                opacity: 0.8;
            }
            .no-data {
                text-align: center;
                color: #999;
                font-style: italic;
                padding: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌡️ Temperature & Humidity Dashboard</h1>
                <p>Real-time sensor data from multiple locations</p>
            </div>
            
            <div class="devices-grid">
                <div class="device-card">
                    <div class="device-header">
                        <div>
			    <div class="location">{{ pico_w.location }}</div>
                            <div class="device-title">Raspberry Pi Pico W</div>
                        </div>
                        <div class="status {{ pico_w.status }}">{{ pico_w.status }}</div>
                    </div>
                    
                    {% if pico_w.timestamp %}
                        <div class="reading">
                            <span class="reading-label">Temperature:</span>
                            <span class="reading-value temperature">{{ pico_w.temperature }} °C</span>
                        </div>
                        <div class="reading">
                            <span class="reading-label">Humidity:</span>
                            <span class="reading-value humidity">{{ pico_w.humidity }} %</span>
                        </div>
                        <div class="timestamp">
                            Last updated: {{ pico_w.timestamp }}
                        </div>
                    {% else %}
                        <div class="no-data">No readings available</div>
                    {% endif %}
                </div>
                
                <div class="device-card">
                    <div class="device-header">
                        <div>
                            <div class="location">{{ raspberry_pi_3.location }}</div>
                            <div class="device-title">Raspberry Pi 3</div>
                        </div>
                        <div class="status {{ raspberry_pi_3.status }}">{{ raspberry_pi_3.status }}</div>
                    </div>
                    
                    {% if raspberry_pi_3.timestamp %}
                        <div class="reading">
                            <span class="reading-label">Temperature:</span>
                            <span class="reading-value temperature">{{ raspberry_pi_3.temperature }} °C</span>
                        </div>
                        <div class="reading">
                            <span class="reading-label">Humidity:</span>
                            <span class="reading-value humidity">{{ raspberry_pi_3.humidity }} %</span>
                        </div>
                        <div class="timestamp">
                            Last updated: {{ raspberry_pi_3.timestamp }}
                        </div>
                    {% else %}
                        <div class="no-data">No readings available</div>
                    {% endif %}
                </div>
            </div>
            
            <div class="controls">
                <button class="btn" onclick="forceFetch()">🔄 Force Refresh</button>
                <button class="btn" onclick="location.reload()">🔄 Reload Page</button>
            </div>
            
            <div class="footer">
                <p>Page auto-refreshes every 60 seconds • Readings fetched every 5 minutes</p>
                <p>Pico W IP: {{ pico_w_ip }} • Raspberry Pi 3 IP: {{ raspberry_pi_3_ip }}</p>
            </div>
        </div>
        
        <script>
            function forceFetch() {
                fetch('/api/force-fetch', {method: 'POST'})
                    .then(response => response.json())
                    .then(data => {
                        alert('Fetch completed! Page will reload in 2 seconds.');
                        setTimeout(() => location.reload(), 2000);
                    })
                    .catch(error => {
                        alert('Error forcing fetch: ' + error);
                    });
            }
        </script>
    </body>
    </html>
    '''
    return render_template_string(
        html,
        pico_w=latest_readings["pico_w"],
        raspberry_pi_3=latest_readings["raspberry_pi_3"],
        pico_w_ip=PICO_W_IP,
        raspberry_pi_3_ip=RASPBERRY_PI_3_IP
    )

if __name__ == '__main__':
    print("Starting Central Sensor Dashboard Server...")
    print(f"Pico W IP: {PICO_W_IP}:{PICO_W_PORT}")
    print(f"Raspberry Pi 3 IP: {RASPBERRY_PI_3_IP}:{RASPBERRY_PI_3_PORT}")
    print("Dashboard available at: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True) 