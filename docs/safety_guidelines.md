# ⚠️ Säkerhetsföreskrifter för NexusTrack

För att säkerställa säker drift av NexusTrack-plattformen ska följande riktlinjer följas:

## ⚡️ Elektrisk säkerhet
* **Korrekt spänning:** Kontrollera alltid utspänningen från Buck Converters med din multimeter innan de ansluts till Elegoo Mega eller OnePlus 8T.
* **Kortslutningsskydd:** Se till att alla kretskort monteras på 3D-printade distanser för att undvika kontakt med ledande ytor.
* **Batterihantering:** Powerbanken ska vara stadigt fastspänd och skyddad från fukt.

## 🚜 Mekanisk säkerhet
* **Klämrisk:** Håll händer borta från bandvagnens drivsystem när motorerna är aktiva.
* **Nödstopp:** Implementera alltid ett mjukvarubaserat nödstopp i Node-RED som bryter MQTT-kommandona omedelbart.
* **Viktbalans:** Placera de tyngsta komponenterna lågt för att förhindra att roboten välter i slänter.

## 🧠 Autonom drift
* **Övervakning:** Kör aldrig roboten helt utan uppsikt under utvecklingsfasen.
* **Sensorkontroll:** Verifiera att alla 5 HC-SR04-sensorer ger korrekta avståndsvärden innan autonom körning påbörjas.