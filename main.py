import json
import paho.mqtt.client as mqtt
import time
from datetime import datetime

# MQTT Configuration
MQTT_BROKER = "localhost"  # Change this to your MQTT broker address
MQTT_PORT = 1883
MQTT_TOPIC = "radar_surveillance"
MQTT_USERNAME = "your_username"  # Add your MQTT username here
MQTT_PASSWORD = "your_password"  # Add your MQTT password here

# Initialize MQTT client
client = mqtt.Client()

# Set MQTT authentication credentials
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

try:
    # Connect to MQTT broker
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()

    # Read the JSON file
    with open('detections.json', 'r') as file:
        detections = json.load(file)

    # Calculate sleep time for 294 detections in 0.1 seconds
    BATCH_SIZE = 294  # 7 * 42 detections
    TIME_WINDOW = 0.1  # 0.1 seconds
    SLEEP_TIME = TIME_WINDOW / BATCH_SIZE  # Time between each detection

    # Publish detections
    while True:
        batch_start_time = time.time()
        
        for i in range(BATCH_SIZE):
            # Get detection (cycling through the detections list if needed)
            detection = detections[i % len(detections)]
            
            # Convert detection to JSON string
            message = json.dumps(detection)
            
            # Publish to MQTT topic
            result = client.publish(MQTT_TOPIC, message)
            
            # Check if publish was successful
            if result[0] == 0:
                print(f"Published detection frame_id: {detection['frame_id']}")
            else:
                print(f"Failed to publish detection frame_id: {detection['frame_id']}")
            
            # Add precise delay between publications
            time.sleep(SLEEP_TIME)
        
        # Wait until the next 0.1 second window
        elapsed_time = time.time() - batch_start_time
        if elapsed_time < TIME_WINDOW:
            time.sleep(TIME_WINDOW - elapsed_time)

except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    # Cleanup
    client.loop_stop()
    client.disconnect()
