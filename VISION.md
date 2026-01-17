
# 🛰️ NexusTrack: Framtidsvision & Roadmap

> *"Vi bygger inte bara en bil, vi bygger en autonom plattform för framtidens trädgård."*

Detta dokument beskriver resan från dagens sensorstyrda RC-bil till en fullfjädrad intelligent trädgårdsrobot driven av AI-vision och kantdatabehandling (Edge Computing).

---

## 👁️ Fas 1: Det digitala ögat (Streaming & Telemetri)

**Mål:** Ge operatören full visuell kontroll och dataöverblick i realtid.

* [ ] **Low-Latency Video:** Aktivera kameran på OnePlus 8T via Termux och streama live-video med WebRTC för minimal fördröjning till Node-RED.
* [ ] **Nexus-HUD (Heads-Up Display):** Implementera ett grafiskt lager på videoströmmen som visar batteristatus, hastighet och avståndssensorer direkt "i bilden".
* [ ] **Virtuell Cockpit:** Skapa responsiva joysticks i Node-RED Dashboard för sömlös växling mellan autonom drift och manuell fjärrstyrning.

---

## 🧠 Fas 2: AI-Vision (Intelligens & QR-styrning)

**Mål:** Gå från att bara reagera på hinder till att förstå och interagera med omvärlden.

* [ ] **TensorFlow Lite Edge-AI:** Integrera lätta modeller för realtidsdetektering av människor, husdjur och trädgårdsredskap.
* [ ] **Smart undvikande:** Programmera kontextuella beteenden (t.ex. stanna och hälsa på människor, men aktivt köra runt statiska objekt som stenar).
* [ ] **The Nexus Shovel (Fysisk pekpinne):** - [ ] Designa/printa ett ergonomiskt handtag med en QR-kod för visuell guidning.
* [ ] **Visual Servoing:** Implementera logik i OpenCV som beräknar hastighet och vinkel baserat på QR-kodens upplevda area och position.


* [ ] **QR-Command System:** Utveckla ett bibliotek av QR-koder som fungerar som fysiska kommandon (t.ex. "Följ mig", "Gå i depå", "Pausa").

---

## 🗺️ Fas 3: Precision & Kartläggning (SLAM)

**Mål:** Ge roboten ett rumsligt medvetande och förmågan att navigera punkt-till-punkt.

* [ ] **Visual SLAM:** Nyttja mobilens kamera och IMU (gyroskop) för att bygga en lokal karta över trädgården samtidigt som roboten rör sig.
* [ ] **Waypoint Navigation:** Implementera en interaktiv karta i Node-RED där målpunkter kan sättas ut som roboten navigerar till autonomt via GPS och SLAM.
* [ ] **Autonom Dockning:** Skapa visuell precisionsstyrning (via QR-markör) för att roboten självständigt ska kunna backa in i sin laddstation.

---

## 🏠 Fas 4: Ekosystem & Röststyrning

**Mål:** Fullständig integration i det smarta hemmet och avancerad interaktion.

* [ ] **Generativ AI-Röst:** Integrera med OpenAI/Whisper API för att kunna ge naturliga röstkommandon ("Nexus, kolla om robotgräsklipparen har fastnat").
* [ ] **Väder-intelligens:** Koppla Node-RED till lokala väderstationer för att automatiskt söka skydd i garaget vid regn eller extrema temperaturer.
* [ ] **Nexus-Flottan:** Förbereda mjukvarustacken för "Multi-Agent Systems" där flera robotar delar kartdata och samarbetar via MQTT-broker.

🏰 Fas 5: Smart Garden Monitoring (Infrastruktur-stödd navigering)
Mål: Ge roboten "Guds-perspektiv" genom att använda externa kameror för att övervaka och styra rörelser på tomten.

[ ] External Object Tracking: Integrera befintliga övervakningskameror (via RTSP/Frigate) för att identifiera robotens position på tomten med OpenCV-triangulering.

[ ] Safety Geofencing: Skapa dynamiska "No-Go-Zones" i trädgården (t.ex. pool, temporära hinder eller känsliga blomrabatter) som skickar omedelbara stoppkommandon via MQTT om roboten närmar sig.

[ ] Global Path Planning: Låta en central server (Proxmox) räkna ut den mest effektiva rutten baserat på en vy från ovan och skicka waypoints till roboten.

[ ] Predictive Safety: Upptäcka hinder som är utanför robotens egna sensorers räckvidd (t.ex. en bil som kör in på uppfarten) och proaktivt styra undan roboten.

---

## 🛠️ Teknisk Stack

| Område | Tekniker |
| --- | --- |
| **Vision** | OpenCV, TensorFlow Lite, MediaPipe |
| **Kommunikation** | WebRTC, MQTT v5, Socket.io |
| **Backend** | Node-RED, Python (Edge), InfluxDB (Telemetri-historik) |
| **Hårdvara** | Arduino Mega (Reflexer), OnePlus 8T (Hjärna), L298N (Muskler) |

---