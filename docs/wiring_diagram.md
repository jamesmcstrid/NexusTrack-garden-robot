# ⚡ NexusTrack Wiring Guide

## 1. Systemöversikt
Nedan ser du hur komponenterna pratar med varandra. Förhandsvisas bäst med `Ctrl+Shift+V`.

```mermaid
graph TD
    Mega[Elegoo Mega 2560]
    L298N[L298N Motor Driver]
    Sensors[5x HC-SR04 Sensors]
    Power[Breadboard Power Module]
    OnePlus[OnePlus 8T]

    OnePlus -- MQTT/USB --> Mega
    Power -- 5V/GND --> Sensors
    Power -- 5V/GND --> Mega
    Mega -- Pins 22-31 --> Sensors
    Mega -- Pins 2-7 --> L298N
    L298N -- Motor Output --> Wheels[RC-Bils Motorer]

Komponent,Pin (Arduino),Funktion,Notering
L298N ENA/ENB,"2, 7",PWM,Hastighet (vänster/höger)
L298N IN1-IN4,"3, 4, 5, 6",Digital,Riktning motorer
Servo,9,PWM,Styrning (Fas 0: RC-bil)
HC-SR04 FC,"22(T), 23(E)",Dig.,Front Center
HC-SR04 FL,"24(T), 25(E)",Dig.,Front Left (45°)
HC-SR04 FR,"26(T), 27(E)",Dig.,Front Right (45°)
HC-SR04 BL,"28(T), 29(E)",Dig.,Back Left (135°)
HC-SR04 BR,"30(T), 31(E)",Dig.,Back Right (135°)