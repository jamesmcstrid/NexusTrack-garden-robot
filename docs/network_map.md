NexusTrack: Datatrafik & Nätverkskarta
Denna karta visar resan från en fysisk hindermätning till en rörlig mätare på din dashboard.

1. Det fysiska lagret (Robot)
Källa: Arduino Mega 2560.

Anslutning: USB-kabel (Serial).

Mottagare: OnePlus 8T.

Protokoll: JSON-strängar via Serial (115200 baud).

2. Trådlösa lagret (Gateway)
Sändare: OnePlus 8T (Headless/Släckt skärm).

Anslutning: Wi-Fi (Lokalnät).

Protokoll: MQTT.

Destination: 192.168.0.36 (Proxmox Host).

3. Serverlagret (Proxmox)
Broker (LXC 103):

Tjänst: Mosquitto MQTT.

Port: 1883.

Topic: nexus/robot1/telemetry.

Dashboard (LXC 104):

Tjänst: Node-RED.

Dashboard URL: http://192.168.0.36:1880/ui/.

Logik: Function-node delar upp JSON till mätare.

Datastruktur (JSON Payload)
Varje meddelande som flödar genom kartan ser ut så här:

JSON

{
  "d_fc": 45,    // Front Center (cm)
  "d_fl": 120,   // Front Left (cm)
  "d_fr": 120,   // Front Right (cm)
  "batt": 85,    // Batteri (%)
  "status": "OK" // Systemstatus
}