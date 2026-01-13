import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
import subprocess
import json
import time
import os
import serial  # Krävs för att prata med Arduinon via USB

# --- KONFIGURATION ---
BROKER_IP = "192.168.0.13"      # Din Proxmox-IP
PORT = 1883
CLIENT_ID = "nexus_bridge_8T"
SERIAL_PORT = "/dev/ttyUSB0"    # Porten i Termux (kolla med termux-usb -l)
BAUD_RATE = 115200
TOPIC_TELEMETRY = "nexus/robot1/telemetry"
TOPIC_PHONE = "nexus/robot1/phone_status"
TOPIC_COMMAND = "robot/command"

# --- MQTT CALLBACKS ---
def on_message(client, userdata, msg):
    """Gör att mobilen pratar om du skickar text till robot/command"""
    try:
        command = msg.payload.decode()
        print(f"📥 Röstmeddelande: {command}")
        subprocess.run(['termux-tts-speak', command])
    except Exception as e:
        print(f"Kommando-fel: {e}")

# --- INITIERING ---
client = mqtt.Client(CallbackAPIVersion.VERSION2, CLIENT_ID)
client.on_message = on_message

print(f"🔗 Ansluter till Proxmox ({BROKER_IP})...")
try:
    client.connect(BROKER_IP, PORT, 60)
    client.subscribe(TOPIC_COMMAND)
    client.loop_start()
except Exception as e:
    print(f"❌ Kunde inte ansluta till MQTT: {e}")
    exit()

# Förhindra att mobilen somnar
os.system('termux-wake-lock')

print(f"🚀 Bridge Online! Lyssnar på USB: {SERIAL_PORT}")



try:
    # Öppna serieporten (Arduino via OTG)
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    
    while True:
        # 1. LÄS DATA FRÅN ARDUINO (Priority #1)
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            try:
                # Arduinon skickar redan JSON, vi skickar den bara vidare
                arduino_data = json.loads(line)
                client.publish(TOPIC_TELEMETRY, json.dumps(arduino_data))
                print(f"🤖 Arduino -> Dashboard: {line}")
            except json.JSONDecodeError:
                print(f"⚠️ Skräp på serieporten: {line}")

        # 2. LÄS TELEFONENS BATTERI (Var 10:e sekund för att spara kraft)
        if int(time.time()) % 10 == 0:
            try:
                res = subprocess.run(['termux-battery-status'], capture_output=True, text=True)
                bat_data = json.loads(res.stdout)
                client.publish(TOPIC_PHONE, json.dumps({
                    "phone_battery": bat_data['percentage'],
                    "phone_temp": bat_data['temperature']
                }))
            except:
                pass

        time.sleep(0.05) # Snabb loop för att inte missa sensordata

except KeyboardInterrupt:
    print("\n🛑 Stänger ner...")
    client.loop_stop()
    os.system('termux-wake-unlock')
except Exception as e:
    print(f"❌ Allvarligt fel: {e}")