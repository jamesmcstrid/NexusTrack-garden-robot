# NexusTrack Core Carrier Specification

## Översikt

**NexusTrack Core Carrier** är en universell monteringsplatta som rymmer all elektronik och kan monteras på olika plattformar (RC-bil prototyp, bandvagn, framtida moduler).

## Designfilosofi

- **Universell:** Passar både RC-bil och bandvagn
- **Modulär:** Enkel att flytta mellan plattformar
- **Kompakt:** Optimerad storlek för komponenter
- **Robust:** Tillräckligt styv för vibrationer
- **Tillgänglig:** Lätt åtkomst till komponenter och kablar

---

## Dimensioner

### Huvudmått
```
Längd:  160 mm
Bredd:  140 mm
Tjocklek: 3 mm (samma som chassiplattan)
Material: PLA/PETG (3D-printad) eller akryl/aluminium
```

### Motivering
- **160x140 mm** är tillräckligt för alla komponenter men mycket mindre än bandvagnens 500x500 mm
- Passar på de flesta RC-bilar (vanligtvis 200-300mm långa)
- Ger utrymme för kabelhantering runt kanterna
- Centrerad montering möjliggör balanserad viktfördelning
- Kompakt design gör den lätt att flytta mellan plattformar

---

## Komponentlayout

### Monteringspositioner (från centrum)

```
+--------------------------------------------------+
|  [BL]                                      [BR]  |  ← Bakre sensorer
|                                                  |
|   [L298N]              [Mega 2560]              |
|   (37x37)              (96.52x50.8)             |
|                                                  |
|                [USB-C Hub]                       |
|                                                  |
|  [FL]          [OnePlus 8T]              [FR]   |  ← Främre sensorer
|                (10° vinkel)                      |
|                                                  |
|                    [FC]                          |  ← Front center
+--------------------------------------------------+
     140 mm
```

### Komponentspecifikationer

#### 1. Elegoo Mega 2560
- **Position:** Höger bakre kvadrant
- **Fästhål:** 4x M3 (CC-mått: 96.52 x 50.8 mm)
- **Offset från centrum:** +30mm X, +10mm Y
- **Höjd över platta:** 10mm (med distanser)

#### 2. L298N Motor Driver
- **Position:** Vänster bakre kvadrant
- **Fästhål:** 4x M3 (kvadratisk: 37 x 37 mm)
- **Offset från centrum:** -40mm X, +10mm Y
- **Höjd över platta:** 5mm (med distanser)

#### 3. OnePlus 8T Hållare
- **Position:** Främre centrum
- **Vinkel:** 10° framåt (för kamera)
- **Fästhål:** 2x M4 för hållare
- **Offset från centrum:** 0mm X, -30mm Y
- **Höjd över platta:** 15mm (för kabelutrymme under)

#### 4. USB-C Hub (Benfei)
- **Position:** Centrum
- **Fästmetod:** Dubbelhäftande tejp eller kabelbuntband
- **Offset från centrum:** 0mm X, +5mm Y
- **Höjd över platta:** Direkt på platta

#### 5. HC-SR04 Sensorer (5st)
- **Monteringsmetod:** Fästen på plattans kanter
- **Fästhål:** 2x M2.5 per sensor
- **Positioner:**
  - **FC (Front Center):** 0mm X, -70mm Y (främre kant)
  - **FL (Front Left):** -60mm X, -60mm Y (45° vinkel)
  - **FR (Front Right):** +60mm X, -60mm Y (45° vinkel)
  - **BL (Back Left):** -60mm X, +70mm Y (135° vinkel)
  - **BR (Back Right):** +60mm X, +70mm Y (135° vinkel)

---

## Fästhålsspecifikation

### Monteringshål för Core Carrier (till plattform)

**4 universella fästhål i hörnen:**
```
Håldiameter: 4.5 mm (för M4 skruv)
Försänkning: 8.5 mm diameter, 3 mm djup (för M4 försänkt huvud)
Position från kant: 10 mm X, 10 mm Y

Koordinater (från centrum):
- Hörn 1: -60mm X, -65mm Y (Vänster fram)
- Hörn 2: +60mm X, -65mm Y (Höger fram)
- Hörn 3: -60mm X, +65mm Y (Vänster bak)
- Hörn 4: +60mm X, +65mm Y (Höger bak)
```

### Monteringshål för komponenter (på Core Carrier)

**Elegoo Mega 2560:**
```
4x M3 hål (3.2 mm diameter)
CC-mått: 96.52 x 50.8 mm
Centrum offset: +30mm X, +10mm Y
```

**L298N Driver:**
```
4x M3 hål (3.2 mm diameter)
Kvadratisk: 37 x 37 mm
Centrum offset: -40mm X, +10mm Y
```

**OnePlus 8T Hållare:**
```
2x M4 hål (4.5 mm diameter)
Avstånd: 80 mm
Centrum offset: 0mm X, -30mm Y
```

**HC-SR04 Sensorer:**
```
10x M2.5 hål (2.7 mm diameter) - 2 per sensor
Positioner: Se komponentlayout ovan
```

---

## Kabelhantering

### Kabelkanaler
- **Bredd:** 5 mm
- **Djup:** 2 mm
- **Position:** Längs plattans kanter mellan komponenter

### Kabelbuntband-fästen
- **Antal:** 6 st
- **Typ:** Integrerade öglor för 3mm kabelbuntband
- **Positioner:** Jämnt fördelade längs kanterna

### Kabelgenomföringar
- **Antal:** 4 st (en per sida)
- **Diameter:** 10 mm
- **Position:** 20 mm från hörnen

---

## Materialval och tillverkning

### Alternativ 1: 3D-printad (Rekommenderad för prototyp)
- **Material:** PETG (bättre än PLA för utomhusbruk)
- **Infill:** 30-40%
- **Väggtjocklek:** 3-4 perimetrar
- **Lager höjd:** 0.2 mm
- **Fördelar:** Snabb iteration, lätt att modifiera
- **Nackdelar:** Mindre styv än metall

### Alternativ 2: Laserskuren akryl
- **Material:** 3 mm transparent eller svart akryl
- **Fördelar:** Snygg finish, bra styvhet
- **Nackdelar:** Dyrare, svårare att modifiera

### Alternativ 3: CNC-fräst aluminium
- **Material:** 3 mm aluminium 6061
- **Fördelar:** Maximal styvhet, värmeledning
- **Nackdelar:** Dyrast, tyngst, kräver CNC

**Rekommendation för Fas 0:** 3D-printad PETG för snabb iteration

---

## Monteringsinstruktioner

### Steg 1: Förbered Core Carrier
1. Printa/tillverka plattan
2. Installera M3 distanser (10mm för Mega, 5mm för L298N)
3. Installera kabelbuntband-fästen om inte integrerade

### Steg 2: Montera komponenter
1. **L298N:** Montera med 4x M3x8mm skruvar
2. **Elegoo Mega:** Montera med 4x M3x12mm skruvar
3. **USB-C Hub:** Fäst med dubbelhäftande tejp i centrum
4. **OnePlus 8T hållare:** Montera med 2x M4x16mm skruvar (10° vinkel)
5. **HC-SR04 sensorer:** Montera med 2x M2.5x8mm skruvar per sensor

### Steg 3: Kablage
1. Anslut L298N till Mega (pins 2-7)
2. Anslut sensorer till Mega (pins 22-31)
3. Anslut USB-C Hub till Mega och OnePlus
4. Organisera kablar med kabelbuntband
5. Säkra lösa kablar i kabelkanaler

### Steg 4: Montera på plattform
1. **RC-bil:** Använd alla 4 hörn-fästhål, montera centrerat
2. **Bandvagn:** Använd alla 4 hörn-fästhål, montera enligt chassi-design

---

## Kompatibilitet

### RC-bil prototyp (Fas 0)
- ✅ Passar på de flesta 1:10 och 1:8 RC-bilar
- ✅ Montera med M4 skruvar genom chassit
- ✅ Kan behöva adapter-plattor för vissa modeller
- ✅ Viktfördelning: Placera över bakaxeln för bästa grepp

### Bandvagn (Fas 1+)
- ✅ Passar perfekt på 500x500mm chassi med gott om utrymme
- ✅ Monteras centrerat eller 100mm framför centrum för optimal balans
- ✅ Fästhål matchar chassi-design från parameters.txt
- ✅ Stort utrymme runt Core Carrier för moduler (gräsklippare, snöplog, lastflak)
- ✅ Flexibel placering på det stora chassit beroende på viktfördelning

### Framtida moduler
- ✅ Cargo trailer: Core Carrier kan monteras på trailer
- ✅ Snow blower: Samma Core Carrier, olika bas-plattform
- ✅ Mower: Integrerad i mower-modul design

---

## Viktanalys

### Komponentvikter (uppskattade)
```
Elegoo Mega 2560:    40g
L298N Driver:        30g
HC-SR04 (5st):       40g (8g × 5)
USB-C Hub:           50g
OnePlus 8T:         188g
Core Carrier platta: 80g (PETG) / 120g (akryl) / 200g (aluminium)
Kablar och fästen:   50g
------------------------
Total vikt:         ~480g (PETG) / ~520g (akryl) / ~640g (aluminium)
```

**Rekommendation:** PETG för lägsta vikt i prototypfas

---

## Underhåll och åtkomst

### Lätt åtkomst till:
- ✅ Elegoo Mega USB-port (höger sida)
- ✅ L298N terminaler (vänster sida)
- ✅ OnePlus 8T (kan tas bort utan att demontera annat)
- ✅ USB-C Hub (centrum, lätt att nå)
- ✅ Alla sensorer (monterade på kanter)

### Demonteringsordning:
1. Ta bort OnePlus 8T från hållare
2. Koppla ur USB-C Hub
3. Lossa 4 hörn-skruvar
4. Lyft av hela Core Carrier som en enhet
5. Byt plattform eller utför underhåll

---

## Framtida förbättringar

### Version 2.0 (efter Fas 0)
- [ ] Integrerad strömfördelning (buck converter)
- [ ] LED-indikering för status
- [ ] Buzzer för ljudvarningar
- [ ] IMU-montering (MPU6050)
- [ ] GPS-modul fäste
- [ ] Batteriövervakning
- [ ] Kylflänsar för L298N (om aluminium)

### Version 3.0 (produktion)
- [ ] PCB-integration (custom board istället för Mega)
- [ ] Integrerad motorstyrning
- [ ] IP65-klassning (vattentät)
- [ ] Vibrationsdämpning
- [ ] Snabbkopplingar för moduler

---

## CAD-filer

### Fusion 360 struktur
```
📐 CAD/fusion360/
├── core_carrier/
│   ├── core_carrier_v1.f3d          # Huvudfil
│   ├── mounting_brackets.f3d        # Fästen för komponenter
│   ├── sensor_mounts.f3d            # HC-SR04 fästen
│   └── phone_holder.f3d             # OnePlus 8T hållare (10°)
```

### Export-format
- **STL:** För 3D-printing
- **DXF:** För laserskärning
- **STEP:** För CNC och CAD-kompatibilitet

---

## Sammanfattning

NexusTrack Core Carrier är hjärtat i det modulära systemet. Genom att standardisera elektronikmonteringen på en universell platta kan vi:

1. ✅ Snabbt testa på RC-bil (Fas 0)
2. ✅ Flytta till bandvagn utan omkablage (Fas 1)
3. ✅ Återanvända i framtida moduler
4. ✅ Underhålla och uppgradera enkelt
5. ✅ Skala produktionen när designen är beprövad

**Nästa steg:** Uppdatera parameters.txt och skapa CAD-modell i Fusion 360.
