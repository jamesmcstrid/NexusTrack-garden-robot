import os
import json
import time
import paho.mqtt.client as mqtt

# --- KONFIGURATION ---
BROKER_IP = "192.168.0.13"  # <--- Ändra till din Proxmox-IP!
TOPIC = "nexus/robot1/telemetry"

client = mqtt.Client()

def get_battery_status():
    # Hämtar data från Termux-API
    status = os.popen('termux-battery-status').read()
    return json.loads(status)

print(f"🚀 Startar robot-sändning till {BROKER_IP}...")
client.connect(BROKER_IP, 1883, 60)

try:
    while True:
        data = get_battery_status()
        # Skapa ett snyggt meddelande
        payload = {
            "battery": data['percentage'],
            "temp": data['temperature'],
            "status": data['status'],
            "timestamp": time.time()
        }
        
        # Skicka till Proxmox
        client.publish(TOPIC, json.dumps(payload))
        print(f"Inskickat: {data['percentage']}% batteri | {data['temperature']}°C")
        
        time.sleep(1) # Vänta 1 sekund
except KeyboardInterrupt:
    print("\n🛑 Stänger ner...")
    client.disconnect()
