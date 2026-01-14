🛰️ NexusTrack: Framtidsvision & Roadmap
Detta dokument beskriver resan från en sensorstyrd RC-bil till en fullfjädrad autonom trädgårdsrobot med AI-vision.

Fas 1: Det digitala ögat (Streaming & Telemetri)
Mål: Se vad roboten ser i realtid.

[ ] Video-streaming: Aktivera kameran på OnePlus 8T via Termux och streama live-video direkt till Node-RED Dashboard.

[ ] HUD (Heads-Up Display): Lägg till ett lager på videostömmen som visar batteristatus, hastighet och sensoravstånd direkt i bilden.

[ ] Fjärrstyrning via Dashboard: Implementera virtuella joysticks i Node-RED för att kunna ta över kontrollen manuellt vid behov.

Fas 2: AI-Vision (Objektigenkänning & Intelligens)
Mål: Gå från att se hinder till att förstå vad de är.

[ ] TensorFlow Lite Integration: Köra lätta AI-modeller direkt i mobilen för att känna igen objekt (Människor, Djur, Verktyg).

[ ] Smart undvikande: Programmera roboten att stanna och "vinka" om den ser en människa, men köra runt om det är en sten.

[ ] Följa-efter-läge: Implementera "Person Tracking" där roboten följer efter ägaren i trädgården med hjälp av kameran.

Fas 3: Precision & Kartläggning (SLAM)
Mål: Veta exakt var den är och vart den ska.

[ ] Visual SLAM: Använda kameran och mobilens gyroskop för att bygga en digital karta över trädgården.

[ ] GPS-Pathing: Sätta ut "Waypoints" på kartan i Node-RED som roboten sedan navigerar mellan autonomt.

[ ] Precisionsparkering: Skapa en visuell markör (t.ex. en QR-kod) vid laddstationen så att roboten kan docka själv för laddning.

Fas 4: Ekosystem & Röststyrning
Mål: Full integration i det smarta hemmet.

[ ] AI-Röst: Integrera med t.ex. OpenAI:s API så att man kan prata med roboten och ge komplexa kommandon ("Gå och kolla om jag glömde grillen på").

[ ] Väder-intelligens: Koppla Node-RED till väder-API:er så att roboten automatiskt kör in i garaget om det börjar regna.

[ ] Fler-robot-system: Förbereda för en "Nexus-flotta" där flera enheter samarbetar och delar kartdata via MQTT.

💡 Teknikstack för framtiden:
Vision: OpenCV, TensorFlow Lite, MediaPipe.

Kommunikation: WebRTC (för låg latens i video), MQTT v5.

Backend: Node-RED (Logik), InfluxDB (Datalagring för trender).

"Vi bygger inte bara en bil, vi bygger en autonom plattform för framtidens trädgård."