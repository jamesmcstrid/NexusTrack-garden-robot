# Patch Guide: Core Carrier v2.0 för 3D-printing med text-gravering

## Översikt

Denna guide uppdaterar [`generate_core_carrier.py`](📐 CAD/fusion360/generate_core_carrier.py:1) till v2.0 med:
- Breadboard-integration (140x180x3mm)
- Text-gravering för komponentidentifiering
- Riktningspil (FRONT)
- Sensor-ID (FC, FL, FR, BL, BR)
- Pin-referenser (Trig/Echo)
- Optimerad för 3D-printing med 0.4mm nozzle

---

## Del 1: Grundläggande dimensionsändringar

### Ändring 1.1: Core Carrier dimensioner
**Rad:** 20-22

```python
# Core Carrier Base Plate v2.0 - 3D Print Optimized
CARRIER_WIDTH = 14.0  # cm (140mm)
CARRIER_LENGTH = 18.0  # cm (180mm) - UPPDATERAD för breadboard
CARRIER_THICKNESS = 0.3  # cm (3mm)
```

### Ändring 1.2: Hörn-fästhål Y-offset
**Rad:** 27

```python
CORNER_HOLE_OFFSET_Y = 7.5  # cm (75mm) from center - UPPDATERAD
```

### Ändring 1.3: Breadboard-parametrar
**Efter rad 70:**

```python
# === BREADBOARD (Kopplingskort) ===
BREADBOARD_LENGTH = 16.55  # cm (165.5mm)
BREADBOARD_WIDTH = 5.55  # cm (55.5mm)
BREADBOARD_DEPTH = 0.15  # cm (1.5mm) - Försänkning
BREADBOARD_OFFSET_X = 0.0  # cm (centrerad)
BREADBOARD_OFFSET_Y = 4.0  # cm (40mm) - Bakre del

# === TEXT ENGRAVING (3D Print Optimized) ===
TEXT_DEPTH = 0.08  # cm (0.8mm) - Djup för text-gravering
TEXT_HEIGHT = 0.5  # cm (5mm) - Texthöjd (läsbar med 0.4mm nozzle)
TEXT_HEIGHT_SMALL = 0.35  # cm (3.5mm) - För pin-referenser
```

---

## Del 2: Text-gravering funktioner

### Ändring 2.1: Lägg till text-helper funktion
**Efter rad 110 (efter helper-funktioner):**

```python
def create_text_engraving(component, text, position_x, position_y, height, depth):
    """Create engraved text on the plate surface."""
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Create sketch for text
        sketch = create_sketch_on_plane(component, "XY")
        sketch.name = f"Text_{text.replace(' ', '_')}"
        
        # Create text
        texts = sketch.sketchTexts
        point = adsk.core.Point3D.create(position_x, position_y, 0)
        
        # Create text input
        text_input = texts.createInput2(text, height)
        text_input.setAsMultiLine(
            point,
            adsk.core.Vector3D.create(1, 0, 0),  # Horizontal
            adsk.core.HorizontalAlignments.CenterHorizontalAlignment,
            adsk.core.VerticalAlignments.MiddleVerticalAlignment,
            0  # Character spacing
        )
        
        text_obj = texts.add(text_input)
        
        # Extrude text as cut (engraving)
        for i in range(sketch.profiles.count):
            profile = sketch.profiles.item(i)
            extrude_profile(
                component,
                profile,
                -depth,
                adsk.fusion.FeatureOperations.CutFeatureOperation
            )
        
        return True
        
    except:
        if ui:
            ui.messageBox(f'Warning: Could not create text "{text}":\n{traceback.format_exc()}')
        return False

def create_arrow_engraving(component, position_x, position_y, length, depth):
    """Create an arrow pointing forward (negative Y direction)."""
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Create sketch for arrow
        sketch = create_sketch_on_plane(component, "XY")
        sketch.name = "Arrow_Front"
        
        lines = sketch.sketchCurves.sketchLines
        
        # Arrow shaft (vertical line)
        shaft_start = adsk.core.Point3D.create(position_x, position_y + length/2, 0)
        shaft_end = adsk.core.Point3D.create(position_x, position_y - length/2, 0)
        lines.addByTwoPoints(shaft_start, shaft_end)
        
        # Arrow head (two lines forming V)
        head_width = length * 0.3
        head_left = adsk.core.Point3D.create(position_x - head_width, position_y - length/2 + head_width, 0)
        head_right = adsk.core.Point3D.create(position_x + head_width, position_y - length/2 + head_width, 0)
        lines.addByTwoPoints(shaft_end, head_left)
        lines.addByTwoPoints(shaft_end, head_right)
        
        # Offset lines to create filled arrow (create closed profile)
        offset_distance = 0.15  # cm (1.5mm width)
        
        # Create a simple filled arrow using rectangles
        # Shaft rectangle
        shaft_rect_width = 0.15  # cm
        create_rectangle_centered_at(sketch, position_x, position_y, shaft_rect_width, length)
        
        # Extrude arrow as cut
        for i in range(sketch.profiles.count):
            profile = sketch.profiles.item(i)
            extrude_profile(
                component,
                profile,
                -depth,
                adsk.fusion.FeatureOperations.CutFeatureOperation
            )
        
        return True
        
    except:
        if ui:
            ui.messageBox(f'Warning: Could not create arrow:\n{traceback.format_exc()}')
        return False
```

---

## Del 3: Komponent-märkning funktioner

### Ändring 3.1: Lägg till komponent-märkning
**Efter text-funktionerna (~rad 200):**

```python
def create_component_labels(component):
    """Create text labels for all components."""
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Elegoo Mega label
        create_text_engraving(
            component,
            "MEGA 2560",
            MEGA_OFFSET_X,
            MEGA_OFFSET_Y + 4.0,  # 40mm above center
            TEXT_HEIGHT,
            TEXT_DEPTH
        )
        
        # L298N label
        create_text_engraving(
            component,
            "L298N DRIVER",
            L298N_OFFSET_X,
            L298N_OFFSET_Y + 3.0,  # 30mm above center
            TEXT_HEIGHT,
            TEXT_DEPTH
        )
        
        # Breadboard label
        create_text_engraving(
            component,
            "830-BB",
            BREADBOARD_OFFSET_X,
            BREADBOARD_OFFSET_Y + 3.5,  # 35mm above center
            TEXT_HEIGHT,
            TEXT_DEPTH
        )
        
        ui.messageBox('Component labels created: MEGA 2560, L298N DRIVER, 830-BB')
        
    except:
        if ui:
            ui.messageBox('Failed to create component labels:\n{}'.format(traceback.format_exc()))

def create_front_indicator(component):
    """Create FRONT arrow and text."""
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Position at front center
        front_x = 0.0
        front_y = -7.5  # 75mm from center (near front edge)
        
        # Create arrow pointing forward
        create_arrow_engraving(
            component,
            front_x,
            front_y,
            1.5,  # 15mm long arrow
            TEXT_DEPTH
        )
        
        # Create "FRONT" text below arrow
        create_text_engraving(
            component,
            "FRONT",
            front_x,
            front_y - 1.2,  # 12mm below arrow
            TEXT_HEIGHT,
            TEXT_DEPTH
        )
        
        ui.messageBox('Front indicator created: Arrow + FRONT text')
        
    except:
        if ui:
            ui.messageBox('Failed to create front indicator:\n{}'.format(traceback.format_exc()))

def create_sensor_labels(component):
    """Create labels for all sensor positions with pin references."""
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Sensor data: (name, x, y, trig_pin, echo_pin)
        sensors = [
            ("FC", SENSOR_FC_X, SENSOR_FC_Y, "22", "23"),
            ("FL", SENSOR_FL_X, SENSOR_FL_Y, "24", "25"),
            ("FR", SENSOR_FR_X, SENSOR_FR_Y, "26", "27"),
            ("BL", SENSOR_BL_X, SENSOR_BL_Y, "28", "29"),
            ("BR", SENSOR_BR_X, SENSOR_BR_Y, "30", "31")
        ]
        
        for name, x, y, trig, echo in sensors:
            # Sensor ID (larger text)
            create_text_engraving(
                component,
                name,
                x,
                y + 1.5,  # 15mm above sensor
                TEXT_HEIGHT,
                TEXT_DEPTH
            )
            
            # Pin reference (smaller text)
            pin_text = f"T{trig}/E{echo}"
            create_text_engraving(
                component,
                pin_text,
                x,
                y - 1.8,  # 18mm below sensor
                TEXT_HEIGHT_SMALL,
                TEXT_DEPTH
            )
        
        ui.messageBox('Sensor labels created: FC, FL, FR, BL, BR with pin references')
        
    except:
        if ui:
            ui.messageBox('Failed to create sensor labels:\n{}'.format(traceback.format_exc()))
```

---

## Del 4: Uppdatera huvudfunktionen

### Ändring 4.1: Uppdatera run()-funktionen
**Rad ~420 (i run()-funktionen):**

```python
def run(context):
    """Main entry point for the Fusion 360 script."""
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Get the active design
        design = adsk.fusion.Design.cast(app.activeProduct)
        if not design:
            ui.messageBox('No active Fusion 360 design found. Please create or open a design.')
            return
        
        # Get the root component
        rootComp = design.rootComponent
        
        # Create a new component for the Core Carrier
        occurrence = rootComp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        component = occurrence.component
        component.name = "NexusTrack_Core_Carrier_v2_3DPrint"
        
        ui.messageBox('Starting NexusTrack Core Carrier v2.0 generation...\n\n' +
                     'Optimized for 3D printing with:\n' +
                     '- Base plate (140x180x3mm)\n' +
                     '- Breadboard recess (165.5x55.5x1.5mm)\n' +
                     '- Component labels (MEGA, L298N, 830-BB)\n' +
                     '- Front indicator (arrow + text)\n' +
                     '- Sensor labels (FC, FL, FR, BL, BR)\n' +
                     '- Pin references (Trig/Echo)\n' +
                     '- All mounting holes\n\n' +
                     'Text depth: 0.8mm (readable with 0.4mm nozzle)\n' +
                     'Text height: 5mm (main), 3.5mm (pins)\n\n' +
                     'Click OK to continue.')
        
        # Generate all components in order
        ui.messageBox('Step 1/8: Creating base plate...')
        create_base_plate(component)
        
        ui.messageBox('Step 2/8: Creating breadboard recess...')
        create_breadboard_recess(component)
        
        ui.messageBox('Step 3/8: Creating corner mounting holes...')
        create_corner_mounting_holes(component)
        
        ui.messageBox('Step 4/8: Creating component mounting holes...')
        create_mega_mounting_holes(component)
        create_l298n_mounting_holes(component)
        create_phone_mounting_holes(component)
        create_sensor_mounting_holes(component)
        
        ui.messageBox('Step 5/8: Creating component labels...')
        create_component_labels(component)
        
        ui.messageBox('Step 6/8: Creating front indicator...')
        create_front_indicator(component)
        
        ui.messageBox('Step 7/8: Creating sensor labels...')
        create_sensor_labels(component)
        
        ui.messageBox('Step 8/8: Creating cable channels...')
        create_cable_channels(component)
        
        # Fit view to show the complete model
        app.activeViewport.fit()
        
        ui.messageBox('✅ NexusTrack Core Carrier v2.0 generated successfully!\n\n' +
                     'Component: NexusTrack_Core_Carrier_v2_3DPrint\n' +
                     'Dimensions: 140x180x3mm\n' +
                     'Breadboard recess: 165.5x55.5x1.5mm\n' +
                     'Text engraving: 0.8mm deep\n\n' +
                     'Labels added:\n' +
                     '- MEGA 2560, L298N DRIVER, 830-BB\n' +
                     '- FRONT arrow and text\n' +
                     '- Sensor IDs: FC, FL, FR, BL, BR\n' +
                     '- Pin refs: T22/E23, T24/E25, etc.\n\n' +
                     'Next steps:\n' +
                     '1. Review the design\n' +
                     '2. Add fillets to corners (optional)\n' +
                     '3. Export as STL for 3D printing\n' +
                     '4. Slice with 0.4mm nozzle settings\n\n' +
                     'Recommended print settings:\n' +
                     '- Material: PETG\n' +
                     '- Layer height: 0.2mm\n' +
                     '- Infill: 30-40%\n' +
                     '- Walls: 3-4 perimeters\n' +
                     '- Support: None needed\n\n' +
                     'See core_carrier_v2_breadboard.md for assembly.')
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
```

---

## Del 5: Sensor-positioner (justerade för längre platta)

### Ändring 5.1: Uppdatera sensor-positioner
**Rad 55-64:**

```python
# Sensor positions (from carrier center) - Adjusted for v2.0 (180mm length)
SENSOR_FC_X = 0.0  # cm
SENSOR_FC_Y = -8.0  # cm (front center) - Flyttad längre fram
SENSOR_FL_X = -6.0  # cm
SENSOR_FL_Y = -7.0  # cm (front left, 45°) - Justerad
SENSOR_FR_X = 6.0  # cm
SENSOR_FR_Y = -7.0  # cm (front right, 45°) - Justerad
SENSOR_BL_X = -6.0  # cm
SENSOR_BL_Y = 8.0  # cm (back left, 135°) - Flyttad längre bak
SENSOR_BR_X = 6.0  # cm
SENSOR_BR_Y = 8.0  # cm (back right, 135°) - Flyttad längre bak
```

---

## Sammanfattning av alla ändringar

| # | Ändring | Rad | Beskrivning |
|---|---------|-----|-------------|
| 1.1 | Dimensioner | 22 | CARRIER_LENGTH: 16.0 → 18.0 |
| 1.2 | Hörn-fästhål | 27 | CORNER_HOLE_OFFSET_Y: 6.5 → 7.5 |
| 1.3 | Parametrar | ~70 | Lägg till breadboard + text-parametrar |
| 2.1 | Text-funktioner | ~110 | Lägg till `create_text_engraving()` och `create_arrow_engraving()` |
| 3.1 | Märkning | ~200 | Lägg till `create_component_labels()`, `create_front_indicator()`, `create_sensor_labels()` |
| 4.1 | Huvudfunktion | ~420 | Uppdatera `run()` med alla nya funktioner |
| 5.1 | Sensorer | 55-64 | Justera sensor-positioner för längre platta |

---

## 3D-printing optimeringar

### Text-gravering djup
- **0.8mm djup:** Perfekt för 0.4mm nozzle
- **5mm höjd:** Läsbar text för huvudlabels
- **3.5mm höjd:** Läsbar text för pin-referenser

### Varför 0.8mm djup?
- 2 lager med 0.4mm nozzle = tydlig kontrast
- Inte för djupt (behåller styrka)
- Lätt att fylla med annan färg (optional)

### Slicing-rekommendationer
```
Material: PETG (bäst för utomhusbruk)
Nozzle: 0.4mm
Layer height: 0.2mm
First layer: 0.25mm (bättre adhesion)
Infill: 30-40%
Walls: 3-4 perimeters
Top/bottom layers: 5-6
Support: None needed
Brim: 5mm (rekommenderas)
Print time: ~8 timmar
Filament: ~95g
```

---

## Testning

Efter uppdatering:

1. **Spara som:** `generate_core_carrier_v2_3dprint.py`
2. **Kör i Fusion 360**
3. **Verifiera:**
   - Basplatta: 140x180x3mm ✓
   - Breadboard-försänkning: 165.5x55.5x1.5mm ✓
   - Text synlig och läsbar ✓
   - FRONT-pil pekar rätt håll ✓
   - Alla sensor-labels (FC, FL, FR, BL, BR) ✓
   - Pin-referenser (T22/E23, etc.) ✓
4. **Exportera STL**
5. **Slica och kontrollera text i preview**

---

## Visuell layout

```
+----------------------------------------------------------+
|  [BL]                                              [BR]  |
|  T28/E29                                        T30/E31  |
|                                                          |
|              [===== 830-BB =====]                        |
|                                                          |
|   L298N DRIVER              MEGA 2560                    |
|   [L298N]                   [Mega]                       |
|                                                          |
|                    [USB-C Hub]                           |
|                                                          |
|  [FL]                                            [FR]    |
|  T24/E25          ↓ FRONT                     T26/E27   |
|                    [FC]                                  |
|                  T22/E23                                 |
+----------------------------------------------------------+
                    140 x 180 mm
```

---

## Färgfyllning av text (optional)

Efter printing kan du fylla texten med annan färg:

1. **Metod 1:** Måla med akrylfärg
2. **Metod 2:** Smält in annan färg filament
3. **Metod 3:** Använd färgbyte i slicer (pause at layer)

---

## Nästa steg

1. Uppdatera Python-skriptet enligt denna guide
2. Kör i Fusion 360
3. Exportera STL
4. Slica med rekommenderade inställningar
5. Printa Core Carrier v2.0
6. Montera komponenter enligt labels
7. Testa med RC-bil (Fas 0)

**Lycka till med 3D-printingen!** 🖨️🚀
