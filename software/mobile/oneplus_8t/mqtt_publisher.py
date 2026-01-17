import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
import subprocess
import json
import time
import os
import serial # Krävs för USB-kommunikation

# --- KONFIGURATION ---
BROKER_IP = "192.168.0.13" # Uppdaterad till din Proxmox IP
PORT = 1883
CLIENT_ID = "robot_oneplus"
SERIAL_PORT = "/dev/ttyUSB0" # Standard för Arduino via OTG
BAUD_RATE = 115200

# --- MQTT CALLBACKS ---
def on_message(client, userdata, msg):
    try:
        command = msg.payload.decode()
        print(f"📥 Mottaget kommando: {command}")
        subprocess.run(['termux-tts-speak', command])
    except Exception as e:
        print(f"Kommando-fel: {e}")

# --- INITIERING ---
client = mqtt.Client(CallbackAPIVersion.VERSION2, CLIENT_ID)
client.on_message = on_message
client.connect(BROKER_IP, PORT, 60)
client.subscribe("robot/command")
client.loop_start()

os.system('termux-wake-lock')

print(f"🚀 Bridge Online! Lyssnar på {SERIAL_PORT}...")

try:
    # Öppna serieporten för Arduino
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    
    while True:
        # 1. LÄS FRÅN ARDUINO (USB)
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            try:
                # Skicka Arduinons JSON-data direkt till din nya topic
                arduino_data = json.loads(line)
                client.publish("nexus/robot1/telemetry", json.dumps(arduino_data))
                print(f"🤖 Arduino -> MQTT: {line}")
            except:
                pass # Ignorera skräp-text

        # 2. LÄS FRÅN TELEFON (Batteri)
        try:
            res = subprocess.run(['termux-battery-status'], capture_output=True, text=True)
            bat = json.loads(res.stdout)
            # Skicka telefonens batteri till en egen topic
            client.publish("nexus/robot1/phone_battery", bat['percentage'])
        except:
            pass

        time.sleep(0.1) # Snabb loop för att inte missa sensordata

except KeyboardInterrupt:
    print("\n🛑 Stänger ner...")
    client.loop_stop()
    os.system('termux-wake-unlock')
