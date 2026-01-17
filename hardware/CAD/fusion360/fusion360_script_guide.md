# Fusion 360 Script Guide - NexusTrack Core Carrier

## Översikt

Python-skriptet [`generate_core_carrier.py`](📐 CAD/fusion360/generate_core_carrier.py:1) genererar automatiskt NexusTrack Core Carrier i Fusion 360 med alla monteringshål och komponenter.

## Vad skriptet skapar

### 1. Basplatta
- **Dimensioner:** 140mm × 160mm × 3mm
- **Material:** PETG (3D-print) eller akryl/aluminium (laserskärning)
- **Centrerad** på XY-planet

### 2. Hörn-fästhål (4st)
- **Typ:** M4 genomgående hål
- **Diameter:** 4.5mm
- **Position:** ±60mm X, ±65mm Y från centrum
- **Syfte:** Fästa Core Carrier på RC-bil eller bandvagn

### 3. Elegoo Mega 2560 fästen (4st)
- **Typ:** M3 hål
- **Diameter:** 3.2mm
- **Mönster:** 96.52mm × 50.8mm (CC-mått)
- **Position:** +30mm X, +10mm Y från centrum
- **Höjd:** 10mm distanser rekommenderas

### 4. L298N Motor Driver fästen (4st)
- **Typ:** M3 hål
- **Diameter:** 3.2mm
- **Mönster:** 37mm × 37mm (kvadrat)
- **Position:** -40mm X, +10mm Y från centrum
- **Höjd:** 5mm distanser rekommenderas

### 5. OnePlus 8T hållare (2st)
- **Typ:** M4 hål
- **Diameter:** 4.5mm
- **Avstånd:** 80mm horisontellt
- **Position:** 0mm X, -30mm Y från centrum
- **Vinkel:** 10° framåt (för kamera)

### 6. HC-SR04 Sensorfästen (10st - 2 per sensor)
- **Typ:** M2.5 hål
- **Diameter:** 2.7mm
- **Sensorer:** 5 stycken för 360° täckning
  - **FC (Front Center):** 0mm X, -70mm Y, 0° rotation
  - **FL (Front Left):** -60mm X, -60mm Y, 45° rotation
  - **FR (Front Right):** 60mm X, -60mm Y, -45° rotation
  - **BL (Back Left):** -60mm X, 70mm Y, 135° rotation
  - **BR (Back Right):** 60mm X, 70mm Y, -135° rotation

### 7. Kabelkanaler
- **Bredd:** 5mm
- **Djup:** 2mm (referenslinjer, implementera som grunda spår)
- **Position:** Längs plattans kanter

---

## Installation och användning

### Steg 1: Förberedelser
1. Öppna Fusion 360
2. Skapa ett nytt projekt eller öppna ett befintligt
3. Se till att du har en aktiv design öppen

### Steg 2: Ladda skriptet
1. Gå till **Tools** → **Add-Ins** → **Scripts and Add-Ins**
2. Klicka på fliken **"Scripts"**
3. Klicka på den gröna **"+"** knappen (Add)
4. Navigera till och välj [`generate_core_carrier.py`](📐 CAD/fusion360/generate_core_carrier.py:1)
5. Skriptet läggs till i listan

### Steg 3: Kör skriptet
1. Välj **"generate_core_carrier"** i listan
2. Klicka på **"Run"**
3. Läs välkomstmeddelandet och klicka **OK**
4. Skriptet genererar alla komponenter automatiskt
5. När det är klart visas ett bekräftelsemeddelande

### Steg 4: Granska och justera
1. Zooma ut för att se hela plattan (View → Fit)
2. Kontrollera att alla hål är på rätt plats
3. Lägg till fillets (rundningar) på hörnen om önskat:
   - Välj **Modify** → **Fillet**
   - Välj alla yttre kanter
   - Sätt radie till 3-5mm

### Steg 5: Export

#### För 3D-printing (PETG):
1. Högerklicka på **"NexusTrack_Core_Carrier"** i Browser
2. Välj **"Save As STL"**
3. Spara som `core_carrier_v1.stl`
4. Importera i din slicer (Cura, PrusaSlicer, etc.)
5. Inställningar:
   - Material: PETG
   - Infill: 30-40%
   - Väggar: 3-4 perimetrar
   - Lagerhöjd: 0.2mm

#### För laserskärning (Akryl/Aluminium):
1. Skapa en ny sketch på top face
2. Välj **Create** → **Project/Include** → **Project**
3. Välj alla hål och yttre kontur
4. Högerklicka på sketchen → **"Save As DXF"**
5. Spara som `core_carrier_v1.dxf`
6. Skicka till laserskärare med specifikation:
   - Material: 3mm akryl eller aluminium
   - Alla hål ska skäras igenom

---

## Felsökning

### Problem: "No active Fusion 360 design found"
**Lösning:** Skapa eller öppna en design innan du kör skriptet.

### Problem: Skriptet kraschar
**Lösning:** 
1. Kontrollera att Fusion 360 är uppdaterat
2. Starta om Fusion 360
3. Kör skriptet igen

### Problem: Hål är på fel plats
**Lösning:** 
1. Kontrollera att parametrarna i skriptet matchar [`parameters_update.md`](📐 CAD/fusion360/parameters_update.md:1)
2. Redigera skriptet om nödvändigt
3. Kör igen

### Problem: Vill ändra dimensioner
**Lösning:**
1. Öppna [`generate_core_carrier.py`](📐 CAD/fusion360/generate_core_carrier.py:1) i en texteditor
2. Ändra parametrarna i början av filen (rad 20-70)
3. Spara och kör skriptet igen

---

## Anpassningar och modifieringar

### Ändra plattans storlek
```python
# I generate_core_carrier.py, rad 20-22:
CARRIER_WIDTH = 14.0  # Ändra till önskad bredd (cm)
CARRIER_LENGTH = 16.0  # Ändra till önskad längd (cm)
CARRIER_THICKNESS = 0.3  # Ändra till önskad tjocklek (cm)
```

### Lägga till fler monteringshål
1. Kopiera en befintlig funktion (t.ex. `create_mega_mounting_holes`)
2. Ändra namn och parametrar
3. Anropa funktionen i `run()` funktionen

### Ändra sensorpositioner
```python
# I generate_core_carrier.py, rad 55-64:
SENSOR_FC_X = 0.0  # Ändra X-position
SENSOR_FC_Y = -7.0  # Ändra Y-position
# etc...
```

---

## Parametrar och koordinatsystem

### Koordinatsystem
- **Origo (0,0,0):** Centrum av plattan
- **X-axel:** Höger = positiv, Vänster = negativ
- **Y-axel:** Fram = negativ, Bak = positiv
- **Z-axel:** Upp = positiv

### Enheter
- Alla mått i skriptet är i **centimeter (cm)**
- Fusion 360 konverterar automatiskt till mm vid export

### Referenstabell

| Komponent | X-offset | Y-offset | Håltyp | Antal |
|-----------|----------|----------|--------|-------|
| Hörn-fästen | ±60mm | ±65mm | M4 (4.5mm) | 4 |
| Elegoo Mega | +30mm | +10mm | M3 (3.2mm) | 4 |
| L298N | -40mm | +10mm | M3 (3.2mm) | 4 |
| OnePlus 8T | 0mm | -30mm | M4 (4.5mm) | 2 |
| Sensor FC | 0mm | -70mm | M2.5 (2.7mm) | 2 |
| Sensor FL | -60mm | -60mm | M2.5 (2.7mm) | 2 |
| Sensor FR | +60mm | -60mm | M2.5 (2.7mm) | 2 |
| Sensor BL | -60mm | +70mm | M2.5 (2.7mm) | 2 |
| Sensor BR | +60mm | +70mm | M2.5 (2.7mm) | 2 |

---

## Nästa steg efter generering

### 1. Validering
- [ ] Kontrollera alla hålpositioner mot [`core_carrier_spec.md`](📐 CAD/fusion360/core_carrier_spec.md:1)
- [ ] Verifiera att komponenterna inte kolliderar
- [ ] Kontrollera clearance runt alla hål (minst 3mm)

### 2. Förbättringar
- [ ] Lägg till fillets på hörnen (3-5mm radie)
- [ ] Lägg till text/logotyp (gravyr eller relief)
- [ ] Skapa kabelkanaler som faktiska spår (0.2mm djup)
- [ ] Lägg till kabelbuntband-öglor

### 3. Tillverkning
- [ ] Exportera STL för 3D-printing
- [ ] Exportera DXF för laserskärning
- [ ] Beställ material (PETG filament eller 3mm akryl)
- [ ] Beställ distanser och skruvar (se BOM)

### 4. Montering
- [ ] Följ monteringsinstruktioner i [`core_carrier_spec.md`](📐 CAD/fusion360/core_carrier_spec.md:1)
- [ ] Montera komponenter i rätt ordning
- [ ] Testa på RC-bil (Fas 0)
- [ ] Flytta till bandvagn (Fas 1)

---

## Relaterade dokument

- [`core_carrier_spec.md`](📐 CAD/fusion360/core_carrier_spec.md:1) - Detaljerad specifikation
- [`parameters_update.md`](📐 CAD/fusion360/parameters_update.md:1) - Alla parametrar och mått
- [`parameters.txt`](📐 CAD/fusion360/parameters.txt:1) - Master parameters för Fusion 360
- [`nexus_firmware_architecture.md`](plans/nexus_firmware_architecture.md:1) - Firmware-arkitektur

---

## Support och bidrag

### Rapportera problem
Om du hittar buggar eller har förbättringsförslag:
1. Dokumentera problemet
2. Inkludera Fusion 360-version
3. Bifoga skärmdumpar om möjligt

### Bidra med förbättringar
1. Forka projektet
2. Gör dina ändringar i skriptet
3. Testa noggrant
4. Skicka pull request med beskrivning

---

## Version History

### v1.0 (2026-01-13)
- Initial release
- Basplatta 140x160x3mm
- 4 hörn-fästhål (M4)
- Elegoo Mega fästen (4x M3)
- L298N fästen (4x M3)
- OnePlus 8T hållare (2x M4)
- 5 sensorfästen (10x M2.5)
- Kabelkanal-referenser

### Planerade förbättringar (v2.0)
- [ ] Automatiska fillets
- [ ] Parametrisk konfiguration via UI
- [ ] Export-automation
- [ ] Komponent-visualisering (3D-modeller)
- [ ] Kollisionskontroll
- [ ] BOM-generering

---

## Licens

Detta skript är en del av NexusTrack-projektet och följer projektets MIT-licens.

**Fri att använda, modifiera och distribuera.**
