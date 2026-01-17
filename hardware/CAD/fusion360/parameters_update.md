# NexusTrack Parameters Update - 500x500mm Chassi

## Översikt av ändringar

**Datum:** 2026-01-13  
**Ändring:** Huvudchassit för bandvagnen har uppdaterats från 180x260mm till **500x500mm**  
**Motivering:** Större plattform ger utrymme för moduler (gräsklippare, snöplog, lastflak)

---

## Uppdaterade Master Parameters

### Kopieras till parameters.txt:

```cpp
// NexusTrack Master Parameters v2.0

// === BANDVAGN HUVUDCHASSI (Fas 1+) ===
Platta_Bredd = 500 mm       // Total bredd på chassiplattan (UPPDATERAD från 180mm)
Platta_Langd = 500 mm       // Total längd på chassiplattan (UPPDATERAD från 260mm)
Platta_Tjocklek = 5 mm      // Styvhet (UPPDATERAD från 3mm för större platta)
Platta_Material = "Aluminium 5mm eller Stål 3mm"

// === CORE CARRIER (Universell elektronikplatta) ===
// OFÖRÄNDRAD - Passar både RC-bil och bandvagn
Carrier_Bredd = 140 mm      // Bredd Core Carrier
Carrier_Langd = 160 mm      // Längd Core Carrier
Carrier_Tjocklek = 3 mm     // Samma som original chassi
Carrier_Fasthal_D = 4.5 mm  // M4 fästhål i hörnen
Carrier_Fasthal_Forsenk_D = 8.5 mm  // Försänkning diameter
Carrier_Fasthal_Forsenk_Djup = 3 mm // Försänkning djup
Carrier_Fasthal_Offset_X = 60 mm    // Från centrum till hörn X
Carrier_Fasthal_Offset_Y = 65 mm    // Från centrum till hörn Y
Carrier_Kant_Marginal = 10 mm       // Avstånd hål från kant
Carrier_Montering_X = 0 mm          // Centrum på bandvagn
Carrier_Montering_Y = 100 mm        // 100mm framför centrum (för balans)

// === ELEGOO MEGA 2560 ===
Mega_X = 96.52 mm           // CC-mått Elegoo Mega X
Mega_Y = 50.8 mm            // CC-mått Elegoo Mega Y
Mega_Hal_D = 3.2 mm         // M3 hål diameter
Mega_Offset_X = 30 mm       // Offset från Carrier centrum
Mega_Offset_Y = 10 mm       // Offset från Carrier centrum
Mega_Hoyd = 10 mm           // Höjd över platta (distanser)

// === L298N MOTOR DRIVER ===
L298N_Dist = 37 mm          // Kvadratisk hålbild motorstyrning
L298N_Hal_D = 3.2 mm        // M3 hål diameter
L298N_Offset_X = -40 mm     // Offset från Carrier centrum
L298N_Offset_Y = 10 mm      // Offset från Carrier centrum
L298N_Hoyd = 5 mm           // Höjd över platta (distanser)

// === ONEPLUS 8T HÅLLARE ===
Mobil_Vinkel = 10 deg       // Kamerans lutning framåt
Mobil_Fasthal_D = 4.5 mm    // M4 hål för hållare
Mobil_Fasthal_Avstand = 80 mm // Avstånd mellan fästhål
Mobil_Offset_X = 0 mm       // Offset från Carrier centrum
Mobil_Offset_Y = -30 mm     // Offset från Carrier centrum
Mobil_Hoyd = 15 mm          // Höjd över platta

// === HC-SR04 SENSORER ===
Sensor_Oga_D = 16.5 mm      // Diameter för HC-SR04 ögon
Sensor_Hal_D = 2.7 mm       // M2.5 fästhål
// Positioner relativt Core Carrier centrum
Sensor_FC_X = 0 mm          // Front Center X
Sensor_FC_Y = -70 mm        // Front Center Y
Sensor_FL_X = -60 mm        // Front Left X
Sensor_FL_Y = -60 mm        // Front Left Y
Sensor_FR_X = 60 mm         // Front Right X
Sensor_FR_Y = -60 mm        // Front Right Y
Sensor_BL_X = -60 mm        // Back Left X
Sensor_BL_Y = 70 mm         // Back Left Y
Sensor_BR_X = 60 mm         // Back Right X
Sensor_BR_Y = 70 mm         // Back Right Y

// === BANDVAGN SPECIFIKT ===
Band_Bredd = 100 mm         // Bredd på varje band
Band_Langd = 400 mm         // Längd på band (kontaktyta)
Band_Avstand = 350 mm       // CC-avstånd mellan band
Band_Drivhjul_D = 80 mm     // Diameter drivhjul
Band_Stodhjul_D = 60 mm     // Diameter stödhjul
Band_Antal_Stodhjul = 4     // Per sida

// === MOTORMONTERING ===
Motor_Typ = "775 DC Motor eller liknande"
Motor_Fasthal_D = 4.5 mm    // M4 fästhål
Motor_CC_Avstand = 50 mm    // CC-avstånd fästhål
Motor_Axel_D = 5 mm         // Axeldiameter
Motor_Position_X = 175 mm   // Från chassi centrum (höger/vänster)
Motor_Position_Y = -50 mm   // Från chassi centrum (bak)

// === MODUL-FÄSTEN (Framtida) ===
Modul_Fasthal_Grid = 50 mm  // Grid-avstånd för modulfästen
Modul_Fasthal_D = 6.5 mm    // M6 fästhål för tunga moduler
Modul_Fram_Y = -200 mm      // Främre modul-zon (från centrum)
Modul_Bak_Y = 200 mm        // Bakre modul-zon (från centrum)

// === KABELHANTERING ===
Kabel_Kanal_Bredd = 5 mm    // Bredd på kabelkanaler
Kabel_Kanal_Djup = 2 mm     // Djup på kabelkanaler
Kabel_Genomforing_D = 10 mm // Diameter kabelgenomföringar
Kabelbuntband_Bredd = 3 mm  // Bredd för kabelbuntband-öglor

// === MARKFRIGÅNG ===
Markfrigång_Min = 50 mm     // Minsta markfrigång
Chassi_Hoyd_Over_Mark = 100 mm // Chassiplatta höjd över mark
```

---

## Jämförelse: Gammalt vs Nytt

| Parameter | Gammalt värde | Nytt värde | Ändring |
|-----------|---------------|------------|---------|
| **Chassi Bredd** | 180 mm | **500 mm** | +320 mm (2.78x) |
| **Chassi Längd** | 260 mm | **500 mm** | +240 mm (1.92x) |
| **Chassi Tjocklek** | 3 mm | **5 mm** | +2 mm (styvare) |
| **Chassi Area** | 0.047 m² | **0.25 m²** | +0.203 m² (5.3x) |
| **Core Carrier** | - | **140x160 mm** | Oförändrad |

---

## Designimplikationer

### 1. Större plattform = Mer funktionalitet

**Fördelar:**
- ✅ Utrymme för gräsklipparmodul (400mm bred)
- ✅ Utrymme för snöplogsmodul
- ✅ Utrymme för lastflak/cargo trailer-koppling
- ✅ Bättre stabilitet (lägre tyngdpunkt möjlig)
- ✅ Större batterikapacitet (mer utrymme)
- ✅ Enklare underhåll (mer arbetsutrymme)

**Utmaningar:**
- ⚠️ Tyngre konstruktion (kräver starkare motorer)
- ⚠️ Dyrare material (5x mer area)
- ⚠️ Svårare att manövrera i trånga utrymmen
- ⚠️ Kräver större bandvagnskomponenter

### 2. Core Carrier förblir kompakt

**Motivering:**
- ✅ Passar fortfarande på RC-bil (Fas 0)
- ✅ All elektronik är kompakt (140x160mm räcker)
- ✅ Kan monteras var som helst på 500x500mm chassit
- ✅ Lätt att flytta mellan plattformar
- ✅ Standardiserad design

### 3. Modulär design

```
+-----------------------------------------------+
|                                               |
|  [Modul-zon fram: Gräsklippare/Snöplog]      |
|                                               |
|            [Core Carrier 140x160]             |
|                                               |
|  [Band vänster]              [Band höger]     |
|                                               |
|  [Modul-zon bak: Lastflak/Trailer-koppling]  |
|                                               |
+-----------------------------------------------+
                  500 x 500 mm
```

---

## CAD-uppdateringar som krävs

### Filer att uppdatera:

1. **📐 CAD/fusion360/02_chassis/**
   - Huvudchassiplatta: 500x500x5mm
   - Förstärkningsribbor för styvhet
   - Modul-fästpunkter (50mm grid)
   - Core Carrier monteringshål (centrum, +100mm Y)

2. **📐 CAD/fusion360/01_track_system/**
   - Bandlängd: 400mm kontaktyta
   - Band CC-avstånd: 350mm
   - Drivhjul: Ø80mm
   - Stödhjul: Ø60mm (4 per sida)

3. **📐 CAD/fusion360/03_motors/**
   - Motormontering för 775 DC-motorer
   - Position: ±175mm X, -50mm Y från centrum
   - Växellåda-integration

4. **📐 CAD/fusion360/core_carrier/** (NY)
   - Core Carrier 140x160x3mm (OFÖRÄNDRAD)
   - Monteringsfästen för 500x500mm chassi
   - Justerbar position (standard: centrum, +100mm Y)

5. **📊 modules/mower/CAD/**
   - Gräsklipparmodul: Max 400mm bredd
   - Montering i främre modul-zon
   - Fäste via M6 skruvar i 50mm grid

---

## Viktanalys (Uppskattad)

### Bandvagn 500x500mm

```
Chassiplatta (5mm aluminium):  3.4 kg
Bandvagnssystem (2 band):      8.0 kg
Motorer (2x 775 DC):           1.2 kg
Core Carrier + elektronik:     0.5 kg
Batteri (LiPo 6S 10Ah):       1.5 kg
Struktur och fästen:           2.0 kg
--------------------------------
Bas-vikt (utan modul):        ~16.6 kg

Gräsklipparmodul:             ~5.0 kg
Snöplogsmodul:                ~8.0 kg
Lastflak (tom):               ~3.0 kg
```

**Total vikt med modul:** 21-25 kg  
**Rekommenderad motoreffekt:** 2x 200W (775 DC-motorer)

---

## Materialrekommendationer

### Chassiplatta 500x500mm

**Alternativ 1: Aluminium 5mm (Rekommenderad)**
- Vikt: 3.4 kg
- Kostnad: ~800 SEK (laserskuren)
- Fördelar: Lätt, rostfri, lätt att bearbeta
- Nackdelar: Dyrare än stål

**Alternativ 2: Stål 3mm**
- Vikt: 5.9 kg
- Kostnad: ~400 SEK (laserskuren)
- Fördelar: Billigare, styvare
- Nackdelar: Tyngre, kan rosta

**Alternativ 3: Komposit (Plywood + Epoxy)**
- Vikt: 2.5 kg
- Kostnad: ~200 SEK (CNC-fräst)
- Fördelar: Billigast, lätt
- Nackdelar: Mindre hållbar, fuktproblem

**Rekommendation:** Aluminium 5mm för bästa balans mellan vikt, styrka och hållbarhet.

---

## Uppdaterad Fas-plan

### Fas 0: RC-bil Prototyp (OFÖRÄNDRAD)
- Core Carrier 140x160mm
- 5x HC-SR04 sensorer
- Elegoo Mega + L298N
- OnePlus 8T
- **Mål:** Validera elektronik och mjukvara

### Fas 1: Bandvagn 500x500mm (UPPDATERAD)
- Nytt chassi 500x500x5mm
- Bandvagnssystem (350mm CC-avstånd)
- 2x 775 DC-motorer
- Flytta Core Carrier från RC-bil
- **Mål:** Funktionell basplattform

### Fas 2: Modul-integration
- Gräsklipparmodul (400mm bred)
- Modul-fästsystem (50mm grid)
- Snabbkopplingar för el och styrning
- **Mål:** Första funktionella modulen

### Fas 3: Produktion och optimering
- Fälttest i olika terränger
- Optimera viktfördelning
- Batterioptimering
- Väderbeständighet
- **Mål:** Produktionsklar design

---

## Nästa steg

### Omedelbart (Innan CAD-arbete):
1. ✅ Uppdatera [`parameters.txt`](📐 CAD/fusion360/parameters.txt:1) med nya värden
2. ✅ Uppdatera [`core_carrier_spec.md`](📐 CAD/fusion360/core_carrier_spec.md:1) med chassi-referens
3. ✅ Dokumentera i [`firmware_architecture.md`](plans/nexus_firmware_architecture.md:1)

### CAD-arbete (Fusion 360):
4. [ ] Skapa nytt chassi 500x500x5mm
5. [ ] Designa bandvagnssystem för 350mm CC-avstånd
6. [ ] Skapa motormonteringar för 775 DC
7. [ ] Designa modul-fästsystem (50mm grid)
8. [ ] Uppdatera Core Carrier monteringsfästen

### Dokumentation:
9. [ ] Skapa assembly-instruktioner för bandvagn
10. [ ] Uppdatera BOM med nya komponenter
11. [ ] Skapa viktanalys och balansdiagram
12. [ ] Dokumentera modul-interface-standard

---

## Sammanfattning

Det nya **500x500mm chassit** ger NexusTrack den flexibilitet och kapacitet som krävs för att vara en riktig arbetsplattform. Genom att behålla **Core Carrier på 140x160mm** säkerställer vi:

1. ✅ Kompatibilitet med RC-bil prototyp (Fas 0)
2. ✅ Enkel överföring till bandvagn (Fas 1)
3. ✅ Standardiserad elektronikmontering
4. ✅ Modulär design för framtida utbyggnad
5. ✅ Skalbar arkitektur

**Nästa steg:** Uppdatera parameters.txt och börja CAD-arbete på det nya chassit.
