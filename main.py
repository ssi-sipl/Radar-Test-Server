import json
import paho.mqtt.client as mqtt
import time
from datetime import datetime

# MQTT Configuration
MQTT_BROKER = "localhost"  # Change this to your MQTT broker address
MQTT_PORT = 1883
MQTT_TOPIC = "radar_surveillance"

# Initialize MQTT client
client = mqtt.Client()

try:
    # Connect to MQTT broker
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()

    # Read the JSON file
    with open('detections.json', 'r') as file:
        detections = json.load(file)

    # Publish each detection
    while True:
        for detection in detections:
            # Convert detection to JSON string
            message = json.dumps(detection)
            
            # Publish to MQTT topic
            result = client.publish(MQTT_TOPIC, message)
            
            # Check if publish was successful
            if result[0] == 0:
                print(f"Published detection frame_id: {detection['frame_id']}")
            else:
                print(f"Failed to publish detection frame_id: {detection['frame_id']}")
            
            # Add a small delay between publications (adjust as needed)
            time.sleep(0.5)

except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    # Cleanup
    client.loop_stop()
    client.disconnect()
