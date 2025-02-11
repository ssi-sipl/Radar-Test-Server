### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Install mosquitto

```bash
sudo apt install mosquitto
```

### 3. Change the config.py file and add the correct MQTT credentials

```bash
nano config.py
```

### 3. Run the script to publish detections

```bash
python main.py
```

### 4. Run the subscriber script to receive detections

```bash
python mqtt_subscriber.py
```
