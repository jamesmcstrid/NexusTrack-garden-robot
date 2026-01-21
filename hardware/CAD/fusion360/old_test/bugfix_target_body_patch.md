# Bugfix: "No target body found to cut or intersect"

## Problem

Felmeddelande i Fusion 360:
```
RuntimeError: 3 : No target body found to cut or intersect!
```

Detta händer i `create_corner_mounting_holes()` och andra cut-operationer eftersom Fusion 360 inte vet vilken body som ska skäras.

---

## Lösning

Vi måste:
1. Säkerställa att base plate skapas korrekt
2. Spara referens till base body
3. Sätta target body för alla cut-operationer
4. Använda korrekt extrude-riktning

---

## Patch 1: Uppdatera extrude_profile funktion

**Fil:** `generate_core_carrier.py`  
**Rad:** ~100 (i `extrude_profile` funktionen)

### Före:
```python
def extrude_profile(component, profile, distance, operation=adsk.fusion.FeatureOperations.NewBodyFeatureOperation):
    """Extrude a profile by the specified distance."""
    extrudes = component.features.extrudeFeatures
    ext_input = extrudes.createInput(profile, operation)
    distance_value = adsk.core.ValueInput.createByReal(distance)
    ext_input.setDistanceExtent(False, distance_value)
    return extrudes.add(ext_input)
```

### Efter:
```python
def extrude_profile(component, profile, distance, operation=adsk.fusion.FeatureOperations.NewBodyFeatureOperation, target_body=None):
    """Extrude a profile by the specified distance."""
    extrudes = component.features.extrudeFeatures
    ext_input = extrudes.createInput(profile, operation)
    
    # Set target body for cut operations
    if operation == adsk.fusion.FeatureOperations.CutFeatureOperation and target_body:
        ext_input.participantBodies = [target_body]
    
    distance_value = adsk.core.ValueInput.createByReal(distance)
    ext_input.setDistanceExtent(False, distance_value)
    
    return extrudes.add(ext_input)
```

---

## Patch 2: Uppdatera create_base_plate för att returnera body

**Fil:** `generate_core_carrier.py`  
**Rad:** ~120 (i `create_base_plate` funktionen)

### Före:
```python
def create_base_plate(component):
    """Create the main Core Carrier base plate."""
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Create sketch for base plate
        sketch = create_sketch_on_plane(component, "XY")
        create_rectangle_centered(sketch, CARRIER_WIDTH, CARRIER_LENGTH)
        
        # Extrude to create base plate
        profile = sketch.profiles.item(0)
        base_extrude = extrude_profile(component, profile, CARRIER_THICKNESS)
        
        # Rename the body
        base_extrude.bodies.item(0).name = "Core_Carrier_Base"
        
        ui.messageBox(f'Base plate created: {CARRIER_WIDTH*10}mm x {CARRIER_LENGTH*10}mm x {CARRIER_THICKNESS*10}mm')
        return base_extrude
        
    except:
        if ui:
            ui.messageBox('Failed to create base plate:\n{}'.format(traceback.format_exc()))
        return None
```

### Efter:
```python
def create_base_plate(component):
    """Create the main Core Carrier base plate."""
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Create sketch for base plate
        sketch = create_sketch_on_plane(component, "XY")
        create_rectangle_centered(sketch, CARRIER_WIDTH, CARRIER_LENGTH)
        
        # Extrude to create base plate (upward in Z)
        profile = sketch.profiles.item(0)
        base_extrude = extrude_profile(component, profile, CARRIER_THICKNESS)
        
        # Get and rename the body
        base_body = base_extrude.bodies.item(0)
        base_body.name = "Core_Carrier_Base"
        
        ui.messageBox(f'Base plate created: {CARRIER_WIDTH*10}mm x {CARRIER_LENGTH*10}mm x {CARRIER_THICKNESS*10}mm')
        
        # Return the body for use in cut operations
        return base_body
        
    except:
        if ui:
            ui.messageBox('Failed to create base plate:\n{}'.format(traceback.format_exc()))
        return None
```

---

## Patch 3: Uppdatera create_corner_mounting_holes

**Fil:** `generate_core_carrier.py`  
**Rad:** ~150 (i `create_corner_mounting_holes` funktionen)

### Före:
```python
def create_corner_mounting_holes(component):
    """Create the four corner mounting holes for platform attachment."""
    ui = None
    try:
        # ... existing code ...
        
        # Extrude cut through
        for i in range(4):
            profile = sketch.profiles.item(i)
            extrude_profile(component, profile, -CARRIER_THICKNESS, 
                          adsk.fusion.FeatureOperations.CutFeatureOperation)
```

### Efter:
```python
def create_corner_mounting_holes(component, target_body):
    """Create the four corner mounting holes for platform attachment."""
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Verify target body exists
        if not target_body:
            ui.messageBox('Error: No target body provided for corner holes')
            return
        
        # Create sketch on top face
        sketch = create_sketch_on_plane(component, "XY")
        sketch.name = "Corner_Mounting_Holes"
        
        # Four corner positions
        positions = [
            (-CORNER_HOLE_OFFSET_X, -CORNER_HOLE_OFFSET_Y),  # Front left
            (CORNER_HOLE_OFFSET_X, -CORNER_HOLE_OFFSET_Y),   # Front right
            (-CORNER_HOLE_OFFSET_X, CORNER_HOLE_OFFSET_Y),   # Back left
            (CORNER_HOLE_OFFSET_X, CORNER_HOLE_OFFSET_Y)     # Back right
        ]
        
        # Create holes
        for x, y in positions:
            create_circle_at_position(sketch, x, y, CORNER_HOLE_DIA)
        
        # Extrude cut through with target body
        for i in range(4):
            profile = sketch.profiles.item(i)
            extrude_profile(component, profile, -CARRIER_THICKNESS, 
                          adsk.fusion.FeatureOperations.CutFeatureOperation,
                          target_body)
        
        ui.messageBox(f'Created 4 corner mounting holes (M4, Ø{CORNER_HOLE_DIA*10}mm)')
        
    except:
        if ui:
            ui.messageBox('Failed to create corner holes:\n{}'.format(traceback.format_exc()))
```

---

## Patch 4: Uppdatera alla hole-funktioner

Samma mönster för alla hole-funktioner. Lägg till `target_body` parameter:

### create_mega_mounting_holes:
```python
def create_mega_mounting_holes(component, target_body):
    # ... existing code ...
    # Extrude cut through with target body
    for i in range(4):
        profile = sketch.profiles.item(i)
        extrude_profile(component, profile, -CARRIER_THICKNESS,
                      adsk.fusion.FeatureOperations.CutFeatureOperation,
                      target_body)
```

### create_l298n_mounting_holes:
```python
def create_l298n_mounting_holes(component, target_body):
    # ... existing code ...
    # Extrude cut through with target body
    for i in range(4):
        profile = sketch.profiles.item(i)
        extrude_profile(component, profile, -CARRIER_THICKNESS,
                      adsk.fusion.FeatureOperations.CutFeatureOperation,
                      target_body)
```

### create_phone_mounting_holes:
```python
def create_phone_mounting_holes(component, target_body):
    # ... existing code ...
    # Extrude cut through with target body
    for i in range(2):
        profile = sketch.profiles.item(i)
        extrude_profile(component, profile, -CARRIER_THICKNESS,
                      adsk.fusion.FeatureOperations.CutFeatureOperation,
                      target_body)
```

### create_sensor_mounting_holes:
```python
def create_sensor_mounting_holes(component, target_body):
    # ... existing code ...
    # Extrude cut through all holes with target body
    for i in range(hole_count):
        profile = sketch.profiles.item(i)
        extrude_profile(component, profile, -CARRIER_THICKNESS,
                      adsk.fusion.FeatureOperations.CutFeatureOperation,
                      target_body)
```

### create_breadboard_recess:
```python
def create_breadboard_recess(component, target_body):
    # ... existing code ...
    # Extrude cut for recess with target body
    profile = sketch.profiles.item(0)
    extrude_profile(
        component, 
        profile, 
        -BREADBOARD_DEPTH,
        adsk.fusion.FeatureOperations.CutFeatureOperation,
        target_body
    )
```

---

## Patch 5: Uppdatera run() funktionen

**Fil:** `generate_core_carrier.py`  
**Rad:** ~420 (i `run()` funktionen)

### Före:
```python
        # Generate all components
        create_base_plate(component)
        create_corner_mounting_holes(component)
        create_mega_mounting_holes(component)
        # ... etc
```

### Efter:
```python
        # Generate all components
        ui.messageBox('Step 1/8: Creating base plate...')
        base_body = create_base_plate(component)
        
        if not base_body:
            ui.messageBox('Error: Failed to create base plate. Aborting.')
            return
        
        ui.messageBox('Step 2/8: Creating breadboard recess...')
        create_breadboard_recess(component, base_body)
        
        ui.messageBox('Step 3/8: Creating corner mounting holes...')
        create_corner_mounting_holes(component, base_body)
        
        ui.messageBox('Step 4/8: Creating component mounting holes...')
        create_mega_mounting_holes(component, base_body)
        create_l298n_mounting_holes(component, base_body)
        create_phone_mounting_holes(component, base_body)
        create_sensor_mounting_holes(component, base_body)
        
        ui.messageBox('Step 5/8: Creating component labels...')
        create_component_labels(component, base_body)
        
        ui.messageBox('Step 6/8: Creating front indicator...')
        create_front_indicator(component, base_body)
        
        ui.messageBox('Step 7/8: Creating sensor labels...')
        create_sensor_labels(component, base_body)
        
        ui.messageBox('Step 8/8: Creating cable channels...')
        create_cable_channels(component)
```

---

## Patch 6: Uppdatera text-funktioner

Text-gravering behöver också target body:

### create_text_engraving:
```python
def create_text_engraving(component, text, position_x, position_y, height, depth, target_body):
    """Create engraved text on the plate surface."""
    # ... existing code ...
    
    # Extrude text as cut (engraving) with target body
    for i in range(sketch.profiles.count):
        profile = sketch.profiles.item(i)
        extrude_profile(
            component,
            profile,
            -depth,
            adsk.fusion.FeatureOperations.CutFeatureOperation,
            target_body
        )
```

### create_component_labels:
```python
def create_component_labels(component, target_body):
    """Create text labels for all components."""
    # ... existing code ...
    
    # Pass target_body to all create_text_engraving calls
    create_text_engraving(
        component,
        "MEGA 2560",
        MEGA_OFFSET_X,
        MEGA_OFFSET_Y + 4.0,
        TEXT_HEIGHT,
        TEXT_DEPTH,
        target_body  # ADD THIS
    )
    # ... etc for all labels
```

---

## Sammanfattning av ändringar

| Funktion | Ändring | Syfte |
|----------|---------|-------|
| `extrude_profile()` | Lägg till `target_body` parameter | Sätt target för cut-operationer |
| `create_base_plate()` | Returnera `base_body` | Ge referens till andra funktioner |
| `create_corner_mounting_holes()` | Lägg till `target_body` parameter | Använd target i cut |
| `create_mega_mounting_holes()` | Lägg till `target_body` parameter | Använd target i cut |
| `create_l298n_mounting_holes()` | Lägg till `target_body` parameter | Använd target i cut |
| `create_phone_mounting_holes()` | Lägg till `target_body` parameter | Använd target i cut |
| `create_sensor_mounting_holes()` | Lägg till `target_body` parameter | Använd target i cut |
| `create_breadboard_recess()` | Lägg till `target_body` parameter | Använd target i cut |
| `create_text_engraving()` | Lägg till `target_body` parameter | Använd target i cut |
| `create_component_labels()` | Lägg till `target_body` parameter | Skicka vidare till text-funktioner |
| `create_front_indicator()` | Lägg till `target_body` parameter | Skicka vidare till text-funktioner |
| `create_sensor_labels()` | Lägg till `target_body` parameter | Skicka vidare till text-funktioner |
| `run()` | Spara `base_body` och skicka vidare | Koordinera alla operationer |

---

## Testning

Efter att ha gjort ändringarna:

1. **Spara filen**
2. **Starta om Fusion 360** (för att ladda om skriptet)
3. **Kör skriptet**
4. **Verifiera:**
   - Base plate skapas först ✓
   - Inga "No target body" fel ✓
   - Alla hål skärs korrekt ✓
   - Text graveras korrekt ✓

---

## Felsökning

### Om du fortfarande får fel:

**Problem:** "No target body found"
**Lösning:** Kontrollera att `base_body` inte är `None` innan cut-operationer

**Problem:** Hål syns inte
**Lösning:** Kontrollera att `-CARRIER_THICKNESS` används (negativt värde för cut)

**Problem:** Text syns inte
**Lösning:** Kontrollera att `-TEXT_DEPTH` används (negativt värde för cut)

---

## Komplett exempel: create_corner_mounting_holes

Här är den kompletta, fixade versionen:

```python
def create_corner_mounting_holes(component, target_body):
    """Create the four corner mounting holes for platform attachment."""
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Verify target body exists
        if not target_body:
            ui.messageBox('Error: No target body provided for corner holes')
            return
        
        # Create sketch on XY plane (top of base plate)
        sketch = create_sketch_on_plane(component, "XY")
        sketch.name = "Corner_Mounting_Holes"
        
        # Four corner positions
        positions = [
            (-CORNER_HOLE_OFFSET_X, -CORNER_HOLE_OFFSET_Y),  # Front left
            (CORNER_HOLE_OFFSET_X, -CORNER_HOLE_OFFSET_Y),   # Front right
            (-CORNER_HOLE_OFFSET_X, CORNER_HOLE_OFFSET_Y),   # Back left
            (CORNER_HOLE_OFFSET_X, CORNER_HOLE_OFFSET_Y)     # Back right
        ]
        
        # Create circles for holes
        for x, y in positions:
            create_circle_at_position(sketch, x, y, CORNER_HOLE_DIA)
        
        # Extrude cut through with target body
        for i in range(4):
            profile = sketch.profiles.item(i)
            extrude_profile(
                component, 
                profile, 
                -CARRIER_THICKNESS,  # Negative = cut downward
                adsk.fusion.FeatureOperations.CutFeatureOperation,
                target_body  # CRITICAL: Specify which body to cut
            )
        
        ui.messageBox(f'Created 4 corner mounting holes (M4, Ø{CORNER_HOLE_DIA*10}mm)')
        
    except:
        if ui:
            ui.messageBox('Failed to create corner holes:\n{}'.format(traceback.format_exc()))
```

---

## Nästa steg

1. Applicera alla patches i ordning
2. Testa skriptet i Fusion 360
3. Verifiera att alla hål och text skapas korrekt
4. Exportera STL för 3D-printing

**Lycka till!** 🔧
