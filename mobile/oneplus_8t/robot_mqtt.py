import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
import subprocess
import json
import time
import os
import serial

# --- KONFIGURATION ---
BROKER_IP = "192.168.0.13"
PORT = 1883
CLIENT_ID = "nexus_bridge_8T"
SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 115200

# Topics
TOPIC_TELEMETRY = "nexus/robot1/telemetry"
TOPIC_PHONE     = "nexus/robot1/phone_status"
TOPIC_GPS       = "nexus/robot1/gps"
TOPIC_COMMAND   = "robot/command"

# --- MQTT CALLBACKS ---
def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print("✅ MQTT Connected!")
        client.subscribe(TOPIC_COMMAND)
    else:
        print(f"❌ MQTT Connection failed: {rc}")

def on_disconnect(client, userdata, rc, properties):
    print(f"⚠️ MQTT Disconnected (code {rc})! Reconnecting...")
    # Biblioteket sköter ofta reconnect själv, men vi loggar det här.

def on_message(client, userdata, msg):
    try:
        command = msg.payload.decode()
        print(f"📥 Kommando mottaget: {command}")
        
        # 1. Skicka vidare till Arduino (om den är ansluten)
        if 'ser' in globals() and ser.is_open:
            ser.write(f"{command}\n".encode())
        
        # 2. Röstfeedback (Termux TTS)
        subprocess.run(['termux-tts-speak', command])
    except Exception as e:
        print(f"❌ Fel vid kommando-hantering: {e}")

# --- HJÄLPFUNKTIONER ---
def connect_serial():
    """Försök ansluta till Arduino med auto-retry"""
    while True:
        try:
            s = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            print(f"✅ Seriell anslutning upprättad: {SERIAL_PORT}")
            return s
        except serial.SerialException as e:
            print(f"⚠️ Seriellt fel: {e}. Försöker igen om 5s...")
            time.sleep(5)

def get_gps_location():
    """Hämta GPS-koordinater via Termux API"""
    try:
        result = subprocess.run(
            ['termux-location', '-p', 'gps'],
            capture_output=True, text=True, timeout=8
        )
        data = json.loads(result.stdout)
        return {
            "lat": data.get('latitude'),
            "lon": data.get('longitude'),
            "acc": data.get('accuracy'),
            "alt": data.get('altitude'),
            "ts": time.time()
        }
    except:
        return None

def get_phone_status():
    """Hämta batteri och temperatur från mobilen"""
    try:
        res = subprocess.run(['termux-battery-status'], capture_output=True, text=True)
        bat = json.loads(res.stdout)
        return {
            "phone_bat": bat['percentage'],
            "phone_temp": bat['temperature'],
            "charging": bat['status'] == 'CHARGING'
        }
    except:
        return None

# --- HUVUDPROGRAM ---
print(f"🚀 Startar Nexus Bridge v3.0...")

# 1. Setup MQTT
client = mqtt.Client(CallbackAPIVersion.VERSION2, CLIENT_ID)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

try:
    client.connect(BROKER_IP, PORT, 60)
    client.loop_start()
except Exception as e:
    print(f"❌ Kunde inte nå MQTT-brokern: {e}")
    exit(1)

# 2. Förhindra viloläge
os.system('termux-wake-lock')

# 3. Anslut till Arduino
ser = connect_serial()

# Timers för att inte överbelasta nätverket
last_phone_update = 0
last_gps_update = 0



try:
    while True:
        current_time = time.time()

        # --- A. LÄS ARDUINO (Prioritet #1 - Realtid) ---
        if ser.in_waiting > 0:
            try:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    # Skicka JSON direkt vidare till MQTT
                    client.publish(TOPIC_TELEMETRY, line)
                    print(f"🤖 Robot -> MQTT: {line}")
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass 
            except serial.SerialException:
                print("❌ Tappade anslutning till Arduino!")
                ser = connect_serial()

        # --- B. MOBILSTATUS (Var 10:e sekund) ---
        if current_time - last_phone_update >= 10:
            status = get_phone_status()
            if status:
                client.publish(TOPIC_PHONE, json.dumps(status))
            last_phone_update = current_time

        # --- C. GPS (Var 5:e sekund) ---
        if current_time - last_gps_update >= 5:
            gps = get_gps_location()
            if gps and gps['lat'] is not None:
                client.publish(TOPIC_GPS, json.dumps(gps))
                print(f"📍 Position: {gps['lat']:.5f}, {gps['lon']:.5f}")
            last_gps_update = current_time

        time.sleep(0.01) # Liten paus för att spara CPU

except KeyboardInterrupt:
    print("\n🛑 Avbryter...")
finally:
    client.loop_stop()
    client.disconnect()
    if 'ser' in globals(): ser.close()
    os.system('termux-wake-unlock')
    print("✅ Systemet säkert avslutat.")