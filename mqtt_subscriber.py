import paho.mqtt.client as mqtt
import json

# MQTT Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "radar_surveillance"

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code: {rc}")
    # Subscribe to the topic upon successful connection
    client.subscribe(MQTT_TOPIC)
    print(f"Subscribed to topic: {MQTT_TOPIC}")

def on_message(client, userdata, msg):
    try:
        # Decode the JSON message
        detection = json.loads(msg.payload.decode())
        print("\n=== New Detection ===")
        for key, value in detection.items():
            print(f"{key}: {value}")
        print("=" * 20)
    except Exception as e:
        print(f"Error processing message: {str(e)}")

# Initialize MQTT client
client = mqtt.Client()

# Assign callback functions
client.on_connect = on_connect
client.on_message = on_message

try:
    # Connect to MQTT broker
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    
    # Start the loop to process received messages
    print("Starting MQTT subscriber...")
    client.loop_forever()

except KeyboardInterrupt:
    print("\nSubscriber stopped by user")
except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    client.disconnect()