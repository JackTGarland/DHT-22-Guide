import network
import json
from time import sleep
from machine import Pin
import socket
import dht

location = ""

# WiFi Configuration
SSID = "SomeSSID"
PASSWORD = "SomePassword"

# Initialize LED for Pico W (uses "LED" pin)
led = Pin("LED", Pin.OUT)

def connect_wifi():
    """Connect to WiFi network"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if wlan.isconnected():
        print("Already connected to WiFi")
        return True
    
    print(f"Connecting to {SSID}...")
    wlan.connect(SSID, PASSWORD)
    
    # Wait for connection with timeout
    max_wait = 10
    while max_wait > 0:
        if wlan.isconnected():
            break
        max_wait -= 1
        print("Waiting for connection...")
        sleep(1)
    
    if wlan.isconnected():
        print(f"Connected to {SSID}")
        print(f"IP address: {wlan.ifconfig()[0]}")
        return True
    else:
        print("Failed to connect to WiFi")
        return False

# Connect to WiFi
if not connect_wifi():
    print("WiFi connection failed. Blinking LED to indicate error...")
    while True:
        led.toggle()  # Toggle LED state
        sleep(0.5)

# Initialize DHT22 sensor on GPIO4
dht_sensor = dht.DHT22(Pin(4))

def get_sensor_reading():
    try:
        print("Attempting to read DHT22 sensor...")
        
        # Add a small delay before reading
        sleep(0.5)
        
        # Read sensor data with retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"Reading attempt {attempt + 1}/{max_retries}")
                dht_sensor.measure()
                temperature = dht_sensor.temperature()
                humidity = dht_sensor.humidity()
                
                print(f"Raw values - Temp: {temperature}, Humidity: {humidity}")
                
                if humidity is not None and temperature is not None:
                    # Validate reasonable ranges
                    if -40 <= temperature <= 80 and 0 <= humidity <= 100:
                        return {
                            "temperature": round(float(temperature), 2),
                            "humidity": round(float(humidity), 2),
                            "device": "pi_pico_w"
                            "location": location
                        }, 200
                    else:
                        print(f"Values out of range - Temp: {temperature}, Humidity: {humidity}")
                        if attempt < max_retries - 1:
                            sleep(1)
                            continue
                else:
                    print("Sensor returned None values")
                    if attempt < max_retries - 1:
                        sleep(1)
                        continue
                        
            except Exception as read_error:
                print(f"Read attempt {attempt + 1} failed: {read_error}")
                if attempt < max_retries - 1:
                    sleep(1)
                    continue
        
        # If we get here, all retries failed
        return {
            "error": "Failed to retrieve valid data from humidity sensor after multiple attempts",
            "device": "pi_pico_w",
            "location": location
            "debug": "Check sensor connections and GPIO pin"
        }, 500
        
    except Exception as e:
        print(f"Sensor reading error: {str(e)}")
        return {
            "error": f"Sensor reading error: {str(e)}",
            "device": "pi_pico_w",
            "location": location
            "debug": "Check sensor wiring and GPIO configuration"
        }, 500

def status():
    return {
        "status": "Pi Pico W Sensor API Running",
        "device": "pi_pico_w"
    }, 200

def create_response(data, status_code=200):
    response_data = json.dumps(data)
    response = f"HTTP/1.1 {status_code} OK\r\n"
    response += "Content-Type: application/json\r\n"
    response += f"Content-Length: {len(response_data)}\r\n"
    response += "Access-Control-Allow-Origin: *\r\n"
    response += "\r\n"
    response += response_data
    return response

def handle_request(request):
    lines = request.split('\n')
    if len(lines) > 0:
        request_line = lines[0].strip()
        if request_line.startswith('GET'):
            if '/reading' in request_line:
                data, status_code = get_sensor_reading()
                return create_response(data, status_code)
            elif '/test' in request_line:
                # Test endpoint to check sensor connection
                data, status_code = test_sensor()
                return create_response(data, status_code)
            elif '/' in request_line:
                data, status_code = status()
                return create_response(data, status_code)
    
    # Default 404 response
    return create_response({"error": "Not found"}, 404)

def test_sensor():
    """Test sensor connection and return diagnostic information"""
    try:
        print("Testing DHT22 sensor connection...")
        
        # Test basic sensor operations
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        
        return {
            "status": "Sensor test completed",
            "device": "pi_pico_w",
            "location": location
            "gpio_pin": 4,
            "temperature": temperature,
            "humidity": humidity,
            "temperature_valid": temperature is not None,
            "humidity_valid": humidity is not None,
            "both_valid": temperature is not None and humidity is not None
        }, 200
    except Exception as e:
        return {
            "status": "Sensor test failed",
            "device": "pi_pico_w",
            "location": location
            "gpio_pin": 4,
            "error": str(e),
            "debug": "Check sensor wiring and power"
        }, 500

def run_server():
    # Set socket options to allow reuse
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        s.bind(('0.0.0.0', 5001))
        s.listen(1)
        print("Pi Pico W Sensor API running on port 5001")
        
        while True:
            try:
                cl, addr = s.accept()
                print('Client connected from', addr)
                request = cl.recv(1024).decode()
                response = handle_request(request)
                cl.send(response.encode())
                cl.close()
            except Exception as e:
                print("Error handling request:", e)
                try:
                    cl.close()
                except:
                    pass
    except OSError as e:
        if e.errno == 98:  # EADDRINUSE
            print("Error: Port 5001 is already in use!")
            print("Please restart the Pico W or wait a moment and try again.")
        else:
            print(f"Socket error: {e}")
    finally:
        try:
            s.close()
        except:
            pass

if __name__ == '__main__':
    run_server() 
