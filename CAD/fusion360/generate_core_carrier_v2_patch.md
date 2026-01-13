# Patch Guide: Uppdatera generate_core_carrier.py till v2.0

## Översikt

Denna guide visar exakt vilka ändringar som behöver göras i [`generate_core_carrier.py`](📐 CAD/fusion360/generate_core_carrier.py:1) för att stödja Core Carrier v2.0 med breadboard-integration.

---

## Ändring 1: Uppdatera Core Carrier dimensioner

**Fil:** `generate_core_carrier.py`  
**Rad:** 20-22

### Före:
```python
# Core Carrier Base Plate
CARRIER_WIDTH = 14.0  # cm (140mm)
CARRIER_LENGTH = 16.0  # cm (160mm)
CARRIER_THICKNESS = 0.3  # cm (3mm)
```

### Efter:
```python
# Core Carrier Base Plate v2.0
CARRIER_WIDTH = 14.0  # cm (140mm)
CARRIER_LENGTH = 18.0  # cm (180mm) - UPPDATERAD för breadboard
CARRIER_THICKNESS = 0.3  # cm (3mm)
```

---

## Ändring 2: Uppdatera hörn-fästhål Y-offset

**Fil:** `generate_core_carrier.py`  
**Rad:** 25-27

### Före:
```python
# Corner mounting holes (for attaching to platform)
CORNER_HOLE_DIA = 0.45  # cm (4.5mm) - M4 holes
CORNER_HOLE_OFFSET_X = 6.0  # cm (60mm) from center
CORNER_HOLE_OFFSET_Y = 6.5  # cm (65mm) from center
```

### Efter:
```python
# Corner mounting holes (for attaching to platform)
CORNER_HOLE_DIA = 0.45  # cm (4.5mm) - M4 holes
CORNER_HOLE_OFFSET_X = 6.0  # cm (60mm) from center
CORNER_HOLE_OFFSET_Y = 7.5  # cm (75mm) from center - UPPDATERAD för längre platta
```

---

## Ändring 3: Lägg till breadboard-parametrar

**Fil:** `generate_core_carrier.py`  
**Rad:** Efter rad 70 (efter sensor-parametrarna)

### Lägg till:
```python
# === BREADBOARD (Kopplingskort) ===
BREADBOARD_LENGTH = 16.55  # cm (165.5mm) - Extra 0.5mm för passform
BREADBOARD_WIDTH = 5.55  # cm (55.5mm) - Extra 0.5mm för passform
BREADBOARD_DEPTH = 0.15  # cm (1.5mm) - Försänkning i plattan
BREADBOARD_OFFSET_X = 0.0  # cm (centrerad)
BREADBOARD_OFFSET_Y = 4.0  # cm (40mm) - Bakre del av plattan
```

---

## Ändring 4: Lägg till helper-funktion för centrerad rektangel

**Fil:** `generate_core_carrier.py`  
**Rad:** Efter rad 95 (efter `create_circle_at_position`)

### Lägg till:
```python
def create_rectangle_centered_at(sketch, center_x, center_y, width, height):
    """Create a rectangle centered at the specified position."""
    lines = sketch.sketchCurves.sketchLines
    half_w = width / 2
    half_h = height / 2
    
    point0 = adsk.core.Point3D.create(center_x - half_w, center_y - half_h, 0)
    point1 = adsk.core.Point3D.create(center_x + half_w, center_y - half_h, 0)
    point2 = adsk.core.Point3D.create(center_x + half_w, center_y + half_h, 0)
    point3 = adsk.core.Point3D.create(center_x - half_w, center_y + half_h, 0)
    
    lines.addByTwoPoints(point0, point1)
    lines.addByTwoPoints(point1, point2)
    lines.addByTwoPoints(point2, point3)
    lines.addByTwoPoints(point3, point0)
```

---

## Ändring 5: Lägg till breadboard recess-funktion

**Fil:** `generate_core_carrier.py`  
**Rad:** Efter rad 350 (efter `create_cable_channels`)

### Lägg till:
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

---

## Ändring 6: Uppdatera run()-funktionen

**Fil:** `generate_core_carrier.py`  
**Rad:** ~420 (i `run()` funktionen)

### Före:
```python
        # Generate all components
        create_base_plate(component)
        create_corner_mounting_holes(component)
        create_mega_mounting_holes(component)
```

### Efter:
```python
        # Generate all components
        create_base_plate(component)
        create_breadboard_recess(component)  # NYT - Lägg till efter base plate
        create_corner_mounting_holes(component)
        create_mega_mounting_holes(component)
```

---

## Ändring 7: Uppdatera sensor-positioner (valfritt)

**Fil:** `generate_core_carrier.py`  
**Rad:** 55-64

### Före:
```python
# Sensor positions (from carrier center)
SENSOR_FC_X = 0.0  # cm
SENSOR_FC_Y = -7.0  # cm (front center)
SENSOR_FL_X = -6.0  # cm
SENSOR_FL_Y = -6.0  # cm (front left, 45°)
SENSOR_FR_X = 6.0  # cm
SENSOR_FR_Y = -6.0  # cm (front right, 45°)
SENSOR_BL_X = -6.0  # cm
SENSOR_BL_Y = 7.0  # cm (back left, 135°)
SENSOR_BR_X = 6.0  # cm
SENSOR_BR_Y = 7.0  # cm (back right, 135°)
```

### Efter (justerat för längre platta):
```python
# Sensor positions (from carrier center) - Adjusted for v2.0
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

## Ändring 8: Uppdatera välkomstmeddelande

**Fil:** `generate_core_carrier.py`  
**Rad:** ~410 (i `run()` funktionen)

### Före:
```python
        ui.messageBox('Starting NexusTrack Core Carrier generation...\n\nThis will create:\n- Base plate (140x160x3mm)\n- 4 corner mounting holes (M4)\n- Elegoo Mega holes (M3)\n- L298N holes (M3)\n- Phone holder holes (M4)\n- 5 sensor mounting holes (M2.5)\n- Cable channels\n\nClick OK to continue.')
```

### Efter:
```python
        ui.messageBox('Starting NexusTrack Core Carrier v2.0 generation...\n\nThis will create:\n- Base plate (140x180x3mm)\n- Breadboard recess (165.5x55.5x1.5mm)\n- 4 corner mounting holes (M4)\n- Elegoo Mega holes (M3)\n- L298N holes (M3)\n- Phone holder holes (M4)\n- 5 sensor mounting holes (M2.5)\n- Cable channels\n\nClick OK to continue.')
```

---

## Ändring 9: Uppdatera slutmeddelande

**Fil:** `generate_core_carrier.py`  
**Rad:** ~435 (i `run()` funktionen)

### Före:
```python
        ui.messageBox('✅ NexusTrack Core Carrier generated successfully!\n\nComponent: NexusTrack_Core_Carrier\n\nNext steps:\n1. Review the design\n2. Add fillets to corners (optional)\n3. Export as STL for 3D printing\n4. Export as DXF for laser cutting\n\nSee core_carrier_spec.md for assembly instructions.')
```

### Efter:
```python
        ui.messageBox('✅ NexusTrack Core Carrier v2.0 generated successfully!\n\nComponent: NexusTrack_Core_Carrier\nDimensions: 140x180x3mm\nBreadboard recess: 165.5x55.5x1.5mm\n\nNext steps:\n1. Review the design\n2. Add fillets to corners (optional)\n3. Export as STL for 3D printing\n4. Mount breadboard with double-sided tape\n\nSee core_carrier_v2_breadboard.md for details.')
```

---

## Sammanfattning av ändringar

| Ändring | Rad | Beskrivning |
|---------|-----|-------------|
| 1 | 22 | CARRIER_LENGTH: 16.0 → 18.0 |
| 2 | 27 | CORNER_HOLE_OFFSET_Y: 6.5 → 7.5 |
| 3 | ~70 | Lägg till breadboard-parametrar |
| 4 | ~95 | Lägg till `create_rectangle_centered_at()` |
| 5 | ~350 | Lägg till `create_breadboard_recess()` |
| 6 | ~420 | Anropa `create_breadboard_recess()` i run() |
| 7 | 55-64 | Justera sensor-positioner (valfritt) |
| 8 | ~410 | Uppdatera välkomstmeddelande |
| 9 | ~435 | Uppdatera slutmeddelande |

---

## Testning

Efter att ha gjort ändringarna:

1. **Spara filen** som `generate_core_carrier_v2.py`
2. **Öppna Fusion 360**
3. **Ladda skriptet:** Tools → Add-Ins → Scripts → "+" → Välj filen
4. **Kör skriptet:** Välj "generate_core_carrier_v2" → Run
5. **Verifiera:**
   - Basplatta är 140x180mm
   - Breadboard-försänkning finns (165.5x55.5mm)
   - Hörn-fästhål är på ±60mm X, ±75mm Y
   - Alla andra hål är på rätt plats

---

## Alternativ: Manuell redigering i Fusion 360

Om du föredrar att inte ändra Python-filen kan du:

1. Kör original-skriptet
2. Manuellt i Fusion 360:
   - Ändra längd till 180mm (Modify → Change Parameters)
   - Flytta hörn-fästhål till Y=±75mm
   - Skapa breadboard-försänkning manuellt (Extrude → Cut)

---

## Backup

Innan du gör ändringar:
```bash
cp generate_core_carrier.py generate_core_carrier_v1_backup.py
```

---

## Support

Om du stöter på problem:
1. Kontrollera att alla ändringar är korrekt gjorda
2. Verifiera att Fusion 360 är uppdaterat
3. Testa med original-skriptet först
4. Läs felmeddelanden noggrant

---

## Nästa version (v3.0)

Planerade förbättringar:
- [ ] Parametrisk konfiguration via UI-dialog
- [ ] Automatiska fillets
- [ ] Val mellan v1.0 (utan breadboard) och v2.0 (med breadboard)
- [ ] Export-automation
- [ ] BOM-generering

---

**Lycka till med uppdateringen!** 🚀
