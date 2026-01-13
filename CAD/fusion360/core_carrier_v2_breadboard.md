# NexusTrack Core Carrier v2.0 - Med Breadboard

## Ändringslogg från v1.0

**Datum:** 2026-01-13  
**Version:** 2.0  
**Huvudändring:** Integration av breadboard för prototyping

### Nya dimensioner
- **Längd:** 180mm (ökad från 160mm)
- **Bredd:** 140mm (oförändrad)
- **Tjocklek:** 3mm (oförändrad)

### Nya komponenter
- **Breadboard:** 165.5mm × 55.5mm med 1.5mm försänkning
- **Justerade hörn-fästhål:** Y-offset ändrad till 75mm (från 65mm)

---

## Uppdaterade parametrar

### Core Carrier v2.0
```cpp
// === CORE CARRIER v2.0 (Med Breadboard) ===
Carrier_Bredd = 140 mm           // Oförändrad
Carrier_Langd = 180 mm           // UPPDATERAD från 160mm
Carrier_Tjocklek = 3 mm          // Oförändrad
Carrier_Fasthal_D = 4.5 mm       // M4 fästhål
Carrier_Fasthal_Offset_X = 60 mm // Oförändrad
Carrier_Fasthal_Offset_Y = 75 mm // UPPDATERAD från 65mm
```

### Breadboard-fäste
```cpp
// === BREADBOARD (Kopplingskort) ===
Breadboard_Langd = 165.5 mm      // Extra 0.5mm för passform
Breadboard_Bredd = 55.5 mm       // Extra 0.5mm för passform
Breadboard_Djup = 1.5 mm         // Försänkning i plattan
Breadboard_Position_X = 0 mm     // Centrerad
Breadboard_Position_Y = 40 mm    // Bakre del av plattan
```

---

## Komponentlayout v2.0

### Översikt
```
+----------------------------------------------------------+
|  [BL]                                              [BR]  | ← Bakre sensorer
|                                                          |
|              [===== BREADBOARD 165x55 =====]            | ← Breadboard-zon
|                                                          |
|   [L298N]                    [Mega 2560]                |
|   (37x37)                    (96.52x50.8)               |
|                                                          |
|                    [USB-C Hub]                           |
|                                                          |
|  [FL]              [OnePlus 8T]                  [FR]   | ← Främre sensorer
|                    (10° vinkel)                          |
|                                                          |
|                        [FC]                              | ← Front center
+----------------------------------------------------------+
                    140 mm × 180 mm
```

### Komponentpositioner (från centrum)

#### 1. Breadboard (NYT)
- **Position:** 0mm X, +40mm Y (bakre del)
- **Dimensioner:** 165.5mm × 55.5mm
- **Försänkning:** 1.5mm djup i plattan
- **Fästmetod:** Dubbelhäftande tejp eller klämfästen
- **Syfte:** Prototyping av kretsar, extra anslutningar

#### 2. Hörn-fästhål (UPPDATERADE)
- **Position:** ±60mm X, ±75mm Y (justerad för längre platta)
- **Diameter:** 4.5mm (M4)
- **Försänkning:** 8.5mm diameter, 3mm djup

#### 3. Elegoo Mega 2560 (OFÖRÄNDRAD)
- **Position:** +30mm X, +10mm Y
- **Fästhål:** 4x M3 (96.52 x 50.8 mm)

#### 4. L298N Motor Driver (OFÖRÄNDRAD)
- **Position:** -40mm X, +10mm Y
- **Fästhål:** 4x M3 (37 x 37 mm)

#### 5. OnePlus 8T Hållare (OFÖRÄNDRAD)
- **Position:** 0mm X, -30mm Y
- **Fästhål:** 2x M4 (80mm avstånd)
- **Vinkel:** 10° framåt

#### 6. HC-SR04 Sensorer (OFÖRÄNDRADE)
- **FC:** 0mm X, -80mm Y (justerad för längre platta)
- **FL:** -60mm X, -70mm Y
- **FR:** +60mm X, -70mm Y
- **BL:** -60mm X, +80mm Y (justerad för längre platta)
- **BR:** +60mm X, +80mm Y (justerad för längre platta)

---

## Breadboard-integration

### Fördelar med breadboard
- ✅ **Snabb prototyping:** Testa kretsar utan lödning
- ✅ **Flexibilitet:** Lägg till sensorer, LED, knappar
- ✅ **Debugging:** Enkel åtkomst till signaler
- ✅ **Expansion:** Extra GPIO-anslutningar
- ✅ **Lärande:** Experimentera med nya komponenter

### Användningsområden

#### Fas 0 (RC-bil prototyp):
- Testa sensoranslutningar
- Prototypa spänningsdelarkretsar
- Lägg till LED-indikering
- Testa olika pull-up/pull-down konfigurationer

#### Fas 1+ (Bandvagn):
- Strömfördelning (buck converters)
- Signalkonditionering
- Extra sensorer (temperatur, fukt, etc.)
- Debugging-punkter

### Montering av breadboard

#### Metod 1: Dubbelhäftande tejp (Enklast)
1. Rengör ytan i breadboard-zonen
2. Applicera dubbelhäftande tejp på breadboard-undersidan
3. Tryck fast breadboard i försänkningen
4. Kontrollera att det sitter stadigt

#### Metod 2: Klämfästen (Mer permanent)
1. Designa små klämfästen som trycker på breadboard-sidorna
2. 3D-printa fästena
3. Skruva fast fästena på Core Carrier
4. Klicka i breadboard

#### Metod 3: Försänkning med läppar (Bäst)
1. Skapa 1.5mm försänkning i CAD
2. Lägg till små läppar (0.5mm) på långsidorna
3. Breadboard glider in och hålls på plats
4. Kan tas bort för rengöring

---

## Uppdaterade mått och jämförelse

### Dimensionsjämförelse

| Parameter | v1.0 | v2.0 | Ändring |
|-----------|------|------|---------|
| **Längd** | 160mm | **180mm** | +20mm |
| **Bredd** | 140mm | 140mm | Oförändrad |
| **Area** | 224 cm² | **252 cm²** | +28 cm² (12.5%) |
| **Hörn Y-offset** | 65mm | **75mm** | +10mm |
| **Vikt (PETG)** | 80g | **90g** | +10g |

### Komponentutrymme
- **Breadboard-zon:** 165.5mm × 55.5mm (9,185 mm²)
- **Återstående yta:** ~16,000 mm² för komponenter
- **Clearance:** Minst 5mm runt breadboard

---

## CAD-uppdateringar

### Fusion 360 Python-skript ändringar

#### Uppdatera parametrar i generate_core_carrier.py:
```python
# Rad 20-22: Uppdatera Core Carrier dimensioner
CARRIER_WIDTH = 14.0  # cm (140mm) - Oförändrad
CARRIER_LENGTH = 18.0  # cm (180mm) - UPPDATERAD från 16.0
CARRIER_THICKNESS = 0.3  # cm (3mm) - Oförändrad

# Rad 25-27: Uppdatera hörn-fästhål
CORNER_HOLE_OFFSET_X = 6.0  # cm (60mm) - Oförändrad
CORNER_HOLE_OFFSET_Y = 7.5  # cm (75mm) - UPPDATERAD från 6.5

# Lägg till efter rad 70: Breadboard parametrar
# === BREADBOARD ===
BREADBOARD_LENGTH = 16.55  # cm (165.5mm)
BREADBOARD_WIDTH = 5.55  # cm (55.5mm)
BREADBOARD_DEPTH = 0.15  # cm (1.5mm) - försänkning
BREADBOARD_OFFSET_X = 0.0  # cm (centrerad)
BREADBOARD_OFFSET_Y = 4.0  # cm (40mm) - bakre del
```

#### Ny funktion att lägga till:
```python
def create_breadboard_recess(component):
    """Create a recessed area for breadboard mounting."""
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Create sketch for breadboard recess
        sketch = create_sketch_on_plane(component, "XY")
        sketch.name = "Breadboard_Recess"
        
        # Create rectangle for breadboard
        create_rectangle_centered_at(
            sketch, 
            BREADBOARD_OFFSET_X, 
            BREADBOARD_OFFSET_Y,
            BREADBOARD_LENGTH, 
            BREADBOARD_WIDTH
        )
        
        # Extrude cut for recess
        profile = sketch.profiles.item(0)
        extrude_profile(
            component, 
            profile, 
            -BREADBOARD_DEPTH,
            adsk.fusion.FeatureOperations.CutFeatureOperation
        )
        
        ui.messageBox(f'Created breadboard recess: {BREADBOARD_LENGTH*10}mm x {BREADBOARD_WIDTH*10}mm x {BREADBOARD_DEPTH*10}mm deep')
        
    except:
        if ui:
            ui.messageBox('Failed to create breadboard recess:\n{}'.format(traceback.format_exc()))
```

#### Uppdatera run() funktionen:
```python
def run(context):
    # ... existing code ...
    
    # Generate all components
    create_base_plate(component)
    create_breadboard_recess(component)  # NYT - Lägg till efter base plate
    create_corner_mounting_holes(component)
    create_mega_mounting_holes(component)
    # ... rest of code ...
```

---

## Viktanalys v2.0

### Komponentvikter (uppdaterade)
```
Core Carrier platta (PETG):      90g  (+10g från v1.0)
Elegoo Mega 2560:                40g
L298N Driver:                    30g
HC-SR04 (5st):                   40g
USB-C Hub:                       50g
OnePlus 8T:                     188g
Breadboard (400 tie-points):     25g  (NYT)
Kablar och fästen:               50g
Breadboard-komponenter:          20g  (uppskattning)
----------------------------------------
Total vikt:                    ~533g  (+53g från v1.0)
```

---

## Användningsscenarier

### Scenario 1: Grundläggande setup (Fas 0)
**Breadboard används för:**
- LED-indikering (status, sensorer)
- Pull-up resistorer för sensorer
- Spänningsdelarkretsar
- Debugging-punkter

**Komponenter på breadboard:**
- 5x LED + resistorer (status)
- 5x 10kΩ resistorer (pull-ups)
- Jumper-kablar för testpunkter

### Scenario 2: Avancerad prototyping
**Breadboard används för:**
- Buck converter (12V → 5V)
- Signalkonditionering
- Extra sensorer (temperatur, fukt)
- Buzzer för ljudvarningar

**Komponenter på breadboard:**
- LM2596 buck converter-modul
- DHT22 temperatur/fuktsensor
- Piezo buzzer
- Kondensatorer för filtrering

### Scenario 3: Produktion (Fas 2+)
**Breadboard ersätts med:**
- Custom PCB med samma footprint
- Integrerad strömförsörjning
- Permanent lödda komponenter
- Professionell finish

---

## Tillverkning

### 3D-printing (PETG)
```
Filament: ~95g PETG
Tid: ~8 timmar (0.2mm lager)
Kostnad: ~30 SEK

Inställningar:
- Infill: 30-40%
- Väggar: 3-4 perimetrar
- Support: Nej (om breadboard-försänkning är grund)
- Brim: Rekommenderas för adhesion
```

### Laserskärning (Akryl 3mm)
```
Material: 252 cm² akryl
Kostnad: ~80 SEK

OBS: Breadboard-försänkning kan inte laserskäras.
Alternativ:
1. Skippa försänkning, använd dubbelhäftande tejp
2. CNC-fräs försänkningen separat
3. Använd 3D-printing istället
```

### CNC-fräsning (Aluminium 3mm)
```
Material: 252 cm² aluminium
Kostnad: ~200 SEK

Fördelar:
- Kan fräsa breadboard-försänkning
- Bästa styvhet
- Professionell finish
- Värmeledning för komponenter
```

---

## Kompatibilitet

### RC-bil prototyp (Fas 0)
- ✅ Passar fortfarande på de flesta RC-bilar
- ✅ 180mm längd är acceptabel
- ⚠️ Kontrollera clearance på din specifika RC-bil
- ✅ Breadboard perfekt för snabb prototyping

### Bandvagn 500x500mm (Fas 1+)
- ✅ Passar perfekt med gott om utrymme
- ✅ Kan monteras centrerat eller framskjutet
- ✅ Breadboard användbar för fälttest
- ✅ Kan senare ersättas med custom PCB

---

## Migration från v1.0 till v2.0

### Om du redan har v1.0:
1. **Behåll v1.0** om du inte behöver breadboard
2. **Bygg v2.0** som komplement för prototyping
3. **Uppgradera** genom att printa ny platta

### Kompatibilitet:
- ✅ Alla komponenter från v1.0 passar på v2.0
- ✅ Samma monteringshål (justerade Y-positioner)
- ✅ Samma firmware och kablar
- ✅ Kan byta mellan v1.0 och v2.0 på samma plattform

---

## Nästa steg

### Omedelbart:
1. [ ] Uppdatera [`generate_core_carrier.py`](📐 CAD/fusion360/generate_core_carrier.py:1) med nya mått
2. [ ] Lägg till `create_breadboard_recess()` funktion
3. [ ] Testa skriptet i Fusion 360
4. [ ] Exportera STL/DXF

### Prototyping:
5. [ ] Printa/tillverka Core Carrier v2.0
6. [ ] Montera breadboard
7. [ ] Testa med LED och enkla kretsar
8. [ ] Dokumentera användbara breadboard-konfigurationer

### Produktion:
9. [ ] Designa custom PCB med samma footprint som breadboard
10. [ ] Integrera strömförsörjning och signalkonditionering
11. [ ] Testa PCB-prototyp
12. [ ] Uppdatera till Core Carrier v3.0 med integrerad PCB

---

## Sammanfattning

Core Carrier v2.0 lägger till **breadboard-integration** för maximal flexibilitet under prototypfasen. De uppdaterade måtten (140mm × 180mm) ger:

- ✅ Plats för standard breadboard (165mm)
- ✅ Behåller kompatibilitet med RC-bil och bandvagn
- ✅ Möjliggör snabb prototyping och testning
- ✅ Kan senare ersättas med custom PCB
- ✅ Endast 20mm längre än v1.0

**Rekommendation:** Använd v2.0 för Fas 0 (RC-bil prototyp) och migrera till custom PCB i Fas 2+.
