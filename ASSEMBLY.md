
# 🚀 NexusTrack Go-Live Checklist

Denna lista säkerställer att hårdvara, mjukvara och nätverk lirar ihop innan första autonoma körningen.

## 1. Hårdvara & Kablage (Musklerna)

Kontrollera att varje pin sitter på rätt plats på din **Arduino Mega 2560**.

### Motorstyrning (L298N)

* [ ] **Motor Vänster:** ENA -> Pin 2, IN1 -> Pin 3, IN2 -> Pin 4.
* [ ] **Motor Höger:** ENB -> Pin 7, IN3 -> Pin 5, IN4 -> Pin 6.
* [ ] **Kraft:** Batteri (+) till L298N 12V, Batteri (-) till L298N GND.
* [ ] **Gemensam Jord:** En svart kabel går från L298N GND till en GND-pin på Arduinon. **(Viktigt!)**

### Styrning (Servo)

* [ ] **Signal (Gul/Vit):** Kopplad till Pin 9.
* [ ] **Ström:** Röd till 5V, Brun/Svart till GND.

### Sensor-matris (HC-SR04)

| Sensor | Trig Pin | Echo Pin | Placering | Check |
| --- | --- | --- | --- | --- |
| **FC** | 22 | 23 | Fram Center | [ ] |
| **FL** | 24 | 25 | Fram Vänster | [ ] |
| **FR** | 26 | 27 | Fram Höger | [ ] |
| **BL** | 28 | 29 | Bak Vänster | [ ] |
| **BR** | 30 | 31 | Bak Höger | [ ] |

---

## 2. System-anslutning (Nerverna)

* [ ] **USB-OTG:** OnePlus 8T kopplad till Arduino Mega via USB-kabel.
* [ ] **Server:** Proxmox-servern är igång.
* [ ] **MQTT Broker:** Container `.13` är online.
* [ ] **Node-RED:** Container `.36` är online.

---

## 3. Mjukvara & Logik (Hjärnan)

* [ ] **Arduino:** `nexus_firmware.ino` är uppladdad till Mega.
* [ ] **Termux:** Kör `python ~/bridge.py` på mobilen.
* [ ] **Verifiering:** Terminalen i Termux visar `✅ MQTT Connected!` och `✅ Seriell anslutning upprättad!`.
* [ ] **Node-RED Dashboard:** Öppna `http://192.168.0.36:1880/ui` och se att mätarna reagerar.

---

## 4. Pre-Flight Test (Bänktestet)

*Gör detta innan du ställer ner bilen på marken!*

* [ ] **Pall-test:** Lyft upp bilen så hjulen hänger fritt.
* [ ] **Hinder-test:** För handen framför främre sensorn (FC).
* [ ] Hjulen stannar omedelbart.
* [ ] Servon svänger (vänster eller höger).
* [ ] Hjulen börjar backa efter 0.5 sekunder.


* [ ] **Dashboard-test:** Ser du att "Status" i Node-RED ändras till `OBSTACLE_DETECTED` och sedan `EVADING`?
* [ ] **Röst-test:** Skriv "Hej Robot" i Dashboarden. Hör du mobilen prata?

---

## 5. Go-Live (Autonom körning)

* [ ] **Yta:** Placera roboten på en plan yta med minst 2 meter fritt utrymme framåt.
* [ ] **Nödstopp:** Ha datorn nära med Dashboarden öppen för att kunna stänga av om något går snett.
* [ ] **Start:** Slå på strömbrytaren till motorerna.
* [ ] **SUCCESS:** Roboten navigerar själv och undviker hinder! 🏆

---

### 🛠 Felsökningstips:

* **Hjulen går åt fel håll?** Skifta plats på de två kablarna som går från motorn till L298N-plinten.
* **Ingen data i Node-RED?** Kolla att mobilen har Wi-Fi och att `bridge.py` inte har kraschat.
* **Servon darrar?** Kolla så att strömförsörjningen är stabil och att GND är ordentligt kopplad.

