# NexusTrack Core Carrier v3.0 - SLUTGILTIG VERSION

## Instruktioner

1. Skapa en ny fil: `software/cad/generate_core_carrier_v3.py`
2. Kopiera **hela Python-koden** nedan till den nya filen
3. Spara filen
4. Kör i Fusion 360

---

## Komplett Python-kod

Kopiera allt från `"""` till sista raden:

```python
"""
NexusTrack Core Carrier Generator v3.0 - FINAL
===============================================
Fixes RuntimeError: 3 by extruding base plate DOWNWARD
and cutting all holes/text from the TOP face.

Author: NexusTrack Project
Date: 2026-01-13
Version: 3.0 FINAL
"""

import adsk.core
import adsk.fusion
import traceback
import math

# ============================================================================
# PARAMETERS
# ============================================================================

# Core Carrier Base Plate v3.0
CARRIER_WIDTH = 14.0  # cm (140mm)
CARRIER_LENGTH = 18.0  # cm (180mm) - UPPDATERAD för 830-punkts breadboard
CARRIER_THICKNESS = 0.3  # cm (3mm)

# Corner mounting holes (for attaching to platform)
CORNER_HOLE_DIA = 0.45  # cm (4.5mm) - M4 holes
CORNER_HOLE_OFFSET_X = 6.0  # cm (60mm) from center
CORNER_HOLE_OFFSET_Y = 7.5  # cm (75mm) from center - UPPDATERAD

# Elegoo Mega 2560 mounting holes
MEGA_HOLE_DIA = 0.32  # cm (3.2mm) - M3 holes
MEGA_CC_X = 9.652  # cm (96.52mm)
MEGA_CC_Y = 5.08  # cm (50.8mm)
MEGA_OFFSET_X = 3.0  # cm (30mm) from carrier center
MEGA_OFFSET_Y = 1.0  # cm (10mm) from carrier center

# L298N Motor Driver mounting holes
L298N_HOLE_DIA = 0.32  # cm (3.2mm) - M3 holes
L298N_SQUARE = 3.7  # cm (37mm) - square pattern
L298N_OFFSET_X = -4.0  # cm (-40mm) from carrier center
L298N_OFFSET_Y = 1.0  # cm (10mm) from carrier center

# OnePlus 8T Phone holder mounting
PHONE_HOLE_DIA = 0.45  # cm (4.5mm) - M4 holes
PHONE_HOLE_SPACING = 8.0  # cm (80mm)
PHONE_OFFSET_X = 0.0  # cm (0mm) from carrier center
PHONE_OFFSET_Y = -3.0  # cm (-30mm) from carrier center

# HC-SR04 Sensor mounting
SENSOR_HOLE_DIA = 0.27  # cm (2.7mm) - M2.5 holes
SENSOR_HOLE_SPACING = 2.5  # cm (25mm) between mounting holes

# Sensor positions (from carrier center) - Adjusted for 180mm length
SENSOR_FC_X = 0.0  # cm
SENSOR_FC_Y = -8.0  # cm (front center)
SENSOR_FL_X = -6.0  # cm
SENSOR_FL_Y = -7.0  # cm (front left, 45°)
SENSOR_FR_X = 6.0  # cm
SENSOR_FR_Y = -7.0  # cm (front right, 45°)
SENSOR_BL_X = -6.0  # cm
SENSOR_BL_Y = 8.0  # cm (back left, 135°)
SENSOR_BR_X = 6.0  # cm
SENSOR_BR_Y = 8.0  # cm (back right, 135°)

# Breadboard (830-punkts kopplingskort)
BREADBOARD_LENGTH = 16.55  # cm (165.5mm) - Extra 0.5mm för passform
BREADBOARD_WIDTH = 5.55  # cm (55.5mm) - Extra 0.5mm för passform
BREADBOARD_DEPTH = 0.15  # cm (1.5mm) - Försänkning
BREADBOARD_OFFSET_X = 0.0  # cm (centrerad)
BREADBOARD_OFFSET_Y = 4.0  # cm (40mm) - Bakre del av plattan

# Text engraving
TEXT_DEPTH = 0.08  # cm (0.8mm) - Djup för text-gravering
TEXT_HEIGHT = 0.5  # cm (5mm) - Texthöjd

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_rectangle_centered(sketch, width, height):
    """Create a centered rectangle on the sketch."""
    lines = sketch.sketchCurves.sketchLines
    half_w = width / 2
    half_h = height / 2
    
    point0 = adsk.core.Point3D.create(-half_w, -half_h, 0)
    point1 = adsk.core.Point3D.create(half_w, -half_h, 0)
    point2 = adsk.core.Point3D.create(half_w, half_h, 0)
    point3 = adsk.core.Point3D.create(-half_w, half_h, 0)
    
    lines.addByTwoPoints(point0, point1)
    lines.addByTwoPoints(point1, point2)
    lines.addByTwoPoints(point2, point3)
    lines.addByTwoPoints(point3, point0)

def create_circle_at_position(sketch, x, y, diameter):
    """Create a circle at the specified position."""
    center = adsk.core.Point3D.create(x, y, 0)
    circles = sketch.sketchCurves.sketchCircles
    return circles.addByCenterRadius(center, diameter/2)

# ============================================================================
# MAIN GENERATION FUNCTIONS
# ============================================================================

def create_base_plate(component):
    """Create the main Core Carrier base plate - EXTRUDED DOWNWARD."""
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Create sketch on XY plane (at Z=0)
        sketch = component.sketches.add(component.xYConstructionPlane)
        sketch.name = "Base_Plate"
        
        # Create rectangle
        create_rectangle_centered(sketch, CARRIER_WIDTH, CARRIER_LENGTH)
        
        # Extrude DOWNWARD (negative direction) to create base plate
        profile = sketch.profiles.item(0)
        extrudes = component.features.extrudeFeatures
        ext_input = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        
        # CRITICAL: Negative distance = extrude downward
        distance_value = adsk.core.ValueInput.createByReal(-CARRIER_THICKNESS)
        ext_input.setDistanceExtent(False, distance_value)
        
        base_extrude = extrudes.add(ext_input)
        
        # Get and rename the body
        base_body = base_extrude.bodies.item(0)
        base_body.name = "Core_Carrier_Base"
        
        ui.messageBox(f'✓ Base plate created: {CARRIER_WIDTH*10}mm x {CARRIER_LENGTH*10}mm x {CARRIER_THICKNESS*10}mm\nExtruded DOWNWARD from XY plane')
        
        # Return the body for use in cut operations
        return base_body
        
    except:
        if ui:
            ui.messageBox(f'Failed to create base plate:\n{traceback.format_exc()}')
        return None

def create_corner_mounting_holes(component, target_body):
    """Create the four corner mounting holes for platform attachment."""
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Verify target body exists
        if not target_body:
            ui.messageBox('Error: No target body provided for corner holes')
            return False
        
        # Create sketch on XY plane (TOP of base plate at Z=0)
        sketch = component.sketches.add(component.xYConstructionPlane)
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
        
        # Extrude cut DOWNWARD through the plate
        for i in range(4):
            profile = sketch.profiles.item(i)
            extrudes = component.features.extrudeFeatures
            ext_input = extrudes.createInput(profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
            ext_input.participantBodies = [target_body]
            
            # CRITICAL: Negative distance = cut downward
            distance_value = adsk.core.ValueInput.createByReal(-CARRIER_THICKNESS)
            ext_input.setDistanceExtent(False, distance_value)
            extrudes.add(ext_input)
        
        ui.messageBox(f'✓ Created 4 corner mounting holes (M4, Ø{CORNER_HOLE_DIA*10}mm)')
        return True
        
    except:
        if ui:
            ui.messageBox(f'Failed to create corner holes:\n{traceback.format_exc()}')
        return False

def create_mega_mounting_holes(component, target_body):
    """Create mounting holes for Elegoo Mega 2560."""
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        if not target_body:
            return False
        
        # Create sketch on XY plane
        sketch = component.sketches.add(component.xYConstructionPlane)
        sketch.name = "Mega_2560_Mounting"
        
        # Four hole positions (rectangular pattern)
        half_x = MEGA_CC_X / 2
        half_y = MEGA_CC_Y / 2
        
        positions = [
            (MEGA_OFFSET_X - half_x, MEGA_OFFSET_Y - half_y),
            (MEGA_OFFSET_X + half_x, MEGA_OFFSET_Y - half_y),
            (MEGA_OFFSET_X - half_x, MEGA_OFFSET_Y + half_y),
            (MEGA_OFFSET_X + half_x, MEGA_OFFSET_Y + half_y)
        ]
        
        # Create holes
        for x, y in positions:
            create_circle_at_position(sketch, x, y, MEGA_HOLE_DIA)
        
        # Extrude cut downward
        for i in range(4):
            profile = sketch.profiles.item(i)
            extrudes = component.features.extrudeFeatures
            ext_input = extrudes.createInput(profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
            ext_input.participantBodies = [target_body]
            distance_value = adsk.core.ValueInput.createByReal(-CARRIER_THICKNESS)
            ext_input.setDistanceExtent(False, distance_value)
            extrudes.add(ext_input)
        
        ui.messageBox(f'✓ Created Elegoo Mega mounting holes (M3, {MEGA_CC_X*10}mm x {MEGA_CC_Y*10}mm)')
        return True
        
    except:
        if ui:
            ui.messageBox(f'Failed to create Mega holes:\n{traceback.format_exc()}')
        return False

def create_l298n_mounting_holes(component, target_body):
    """Create mounting holes for L298N motor driver."""
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        if not target_body:
            return False
        
        # Create sketch on XY plane
        sketch = component.sketches.add(component.xYConstructionPlane)
        sketch.name = "L298N_Mounting"
        
        # Four hole positions (square pattern)
        half_square = L298N_SQUARE / 2
        
        positions = [
            (L298N_OFFSET_X - half_square, L298N_OFFSET_Y - half_square),
            (L298N_OFFSET_X + half_square, L298N_OFFSET_Y - half_square),
            (L298N_OFFSET_X - half_square, L298N_OFFSET_Y + half_square),
            (L298N_OFFSET_X + half_square, L298N_OFFSET_Y + half_square)
        ]
        
        # Create holes
        for x, y in positions:
            create_circle_at_position(sketch, x, y, L298N_HOLE_DIA)
        
        # Extrude cut downward
        for i in range(4):
            profile = sketch.profiles.item(i)
            extrudes = component.features.extrudeFeatures
            ext_input = extrudes.createInput(profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
            ext_input.participantBodies = [target_body]
            distance_value = adsk.core.ValueInput.createByReal(-CARRIER_THICKNESS)
            ext_input.setDistanceExtent(False, distance_value)
            extrudes.add(ext_input)
        
        ui.messageBox(f'✓ Created L298N mounting holes (M3, {L298N_SQUARE*10}mm square)')
        return True
        
    except:
        if ui:
            ui.messageBox(f'Failed to create L298N holes:\n{traceback.format_exc()}')
        return False

def create_phone_mounting_holes(component, target_body):
    """Create mounting holes for OnePlus 8T phone holder."""
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        if not target_body:
            return False
        
        # Create sketch on XY plane
        sketch = component.sketches.add(component.xYConstructionPlane)
        sketch.name = "Phone_Holder_Mounting"
        
        # Two hole positions (horizontal spacing)
        half_spacing = PHONE_HOLE_SPACING / 2
        
        positions = [
            (PHONE_OFFSET_X - half_spacing, PHONE_OFFSET_Y),
            (PHONE_OFFSET_X + half_spacing, PHONE_OFFSET_Y)
        ]
        
        # Create holes
        for x, y in positions:
            create_circle_at_position(sketch, x, y, PHONE_HOLE_DIA)
        
        # Extrude cut downward
        for i in range(2):
            profile = sketch.profiles.item(i)
            extrudes = component.features.extrudeFeatures
            ext_input = extrudes.createInput(profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
            ext_input.participantBodies = [target_body]
            distance_value = adsk.core.ValueInput.createByReal(-CARRIER_THICKNESS)
            ext_input.setDistanceExtent(False, distance_value)
            extrudes.add(ext_input)
        
        ui.messageBox(f'✓ Created phone holder mounting holes (M4, {PHONE_HOLE_SPACING*10}mm spacing)')
        return True
        
    except:
        if ui:
            ui.messageBox(f'Failed to create phone holes:\n{traceback.format_exc()}')
        return False

def create_sensor_mounting_holes(component, target_body):
    """Create mounting holes for all 5 HC-SR04 sensors."""
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        if not target_body:
            return False
        
        # Create sketch on XY plane
        sketch = component.sketches.add(component.xYConstructionPlane)
        sketch.name = "Sensor_Mounting_Holes"
        
        # Sensor positions and names
        sensors = [
            ("FC", SENSOR_FC_X, SENSOR_FC_Y, 0),      # Front Center
            ("FL", SENSOR_FL_X, SENSOR_FL_Y, 45),     # Front Left (45°)
            ("FR", SENSOR_FR_X, SENSOR_FR_Y, -45),    # Front Right (-45°)
            ("BL", SENSOR_BL_X, SENSOR_BL_Y, 135),    # Back Left (135°)
            ("BR", SENSOR_BR_X, SENSOR_BR_Y, -135)    # Back Right (-135°)
        ]
        
        hole_count = 0
        
        # Create mounting holes for each sensor (2 holes per sensor)
        for name, x, y, angle in sensors:
            # Calculate hole positions based on angle
            angle_rad = math.radians(angle)
            dx = (SENSOR_HOLE_SPACING / 2) * math.cos(angle_rad)
            dy = (SENSOR_HOLE_SPACING / 2) * math.sin(angle_rad)
            
            # Two mounting holes per sensor
            hole1_x = x - dx
            hole1_y = y - dy
            hole2_x = x + dx
            hole2_y = y + dy
            
            create_circle_at_position(sketch, hole1_x, hole1_y, SENSOR_HOLE_DIA)
            create_circle_at_position(sketch, hole2_x, hole2_y, SENSOR_HOLE_DIA)
            hole_count += 2
        
        # Extrude cut downward through all holes
        for i in range(hole_count):
            profile = sketch.profiles.item(i)
            extrudes = component.features.extrudeFeatures
            ext_input = extrudes.createInput(profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
            ext_input.participantBodies = [target_body]
            distance_value = adsk.core.ValueInput.createByReal(-CARRIER_THICKNESS)
            ext_input.setDistanceExtent(False, distance_value)
            extrudes.add(ext_input)
        
        ui.messageBox(f'✓ Created {hole_count} sensor mounting holes (M2.5) for 5 HC-SR04 sensors')
        return True
        
    except:
        if ui:
            ui.messageBox(f'Failed to create sensor holes:\n{traceback.format_exc()}')
        return False

def create_breadboard_pocket(component, target_body):
    """Create breadboard recess pocket (1.5mm deep)."""
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        if not target_body:
            return False
        
        # Create sketch on XY plane
        sketch = component.sketches.add(component.xYConstructionPlane)
        sketch.name = "Breadboard_Pocket"
        
        # Create rectangle for breadboard
        lines = sketch.sketchCurves.sketchLines
        half_w = BREADBOARD_LENGTH / 2
        half_h = BREADBOARD_WIDTH / 2
        x = BREADBOARD_OFFSET_X
        y = BREADBOARD_OFFSET_Y
        
        p0 = adsk.core.Point3D.create(x - half_w, y - half_h, 0)
        p1 = adsk.core.Point3D.create(x + half_w, y - half_h, 0)
        p2 = adsk.core.Point3D.create(x + half_w, y + half_h, 0)
        p3 = adsk.core.Point3D.create(x - half_w, y + half_h, 0)
        
        lines.addByTwoPoints(p0, p1)
        lines.addByTwoPoints(p1, p2)
        lines.addByTwoPoints(p2, p3)
        lines.addByTwoPoints(p3, p0)
        
        # Extrude cut downward for pocket
        profile = sketch.profiles.item(0)
        extrudes = component.features.extrudeFeatures
        ext_input = extrudes.createInput(profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
        ext_input.participantBodies = [target_body]
        
        # CRITICAL: Negative distance = cut downward
        distance_value = adsk.core.ValueInput.createByReal(-BREADBOARD_DEPTH)
        ext_input.setDistanceExtent(False, distance_value)
        extrudes.add(ext_input)
        
        ui.messageBox(f'✓ Created breadboard pocket: {BREADBOARD_LENGTH*10}mm x {BREADBOARD_WIDTH*10}mm x {BREADBOARD_DEPTH*10}mm deep')
        return True
        
    except:
        if ui:
            ui.messageBox(f'Failed to create breadboard pocket:\n{traceback.format_exc()}')
        return False

def create_text_markings(component, target_body):
    """Create text markings for FRONT and sensor names."""
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        if not target_body:
            return False
        
        # Create sketch on XY plane
        sketch = component.sketches.add(component.xYConstructionPlane)
        sketch.name = "Text_Markings"
        
        texts = sketch.sketchTexts
        
        # FRONT text
        front_point = adsk.core.Point3D.create(0, -7.5, 0)
        front_input = texts.createInput2("FRONT", TEXT_HEIGHT)
        front_input.setAsMultiLine(
            front_point,
            adsk.core.Vector3D.create(1, 0, 0),
            adsk.core.HorizontalAlignments.CenterHorizontalAlignment,
            adsk.core.VerticalAlignments.MiddleVerticalAlignment,
            0
        )
        texts.add(front_input)
        
        # Sensor labels
        sensors = [
            ("FC", SENSOR_FC_X, SENSOR_FC_Y + 1.5),
            ("FL", SENSOR_FL_X, SENSOR_FL_Y + 1.5),
            ("FR", SENSOR_FR_X, SENSOR_FR_Y + 1.5),
            ("BL", SENSOR_BL_X, SENSOR_BL_Y - 1.5),
            ("BR", SENSOR_BR_X, SENSOR_BR_Y - 1.5),
        ]
        
        for label, x, y in sensors:
            point = adsk.core.Point3D.create(x, y, 0)
            text_input = texts.createInput2(label, TEXT_HEIGHT)
            text_input.setAsMultiLine(
                point,
                adsk.core.Vector3D.create(1, 0, 0),
                adsk.core.HorizontalAlignments.CenterHorizontalAlignment,
                adsk.core.VerticalAlignments.MiddleVerticalAlignment,
                0
            )
            texts.add(text_input)
        
        # Extrude cut downward for all text
        for i in range(sketch.profiles.count):
            profile = sketch.profiles.item(i)
            extrudes = component.features.extrudeFeatures
            ext_input = extrudes.createInput(profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
            ext_input.participantBodies = [target_body]
            distance_value = adsk.core.ValueInput.createByReal(-TEXT_DEPTH)
            ext_input.setDistanceExtent(False, distance_value)
            extrudes.add(ext_input)
        
        ui.messageBox('✓ Created text markings: FRONT, FC, FL, FR, BL, BR')
        return True
        
    except:
        if ui:
            ui.messageBox(f'Failed to create text markings:\n{traceback.format_exc()}')
        return False

# ============================================================================
# MAIN RUN FUNCTION
# ============================================================================

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
        component.name = "NexusTrack_Core_Carrier_v3"
        
        ui.messageBox('NexusTrack Core Carrier v3.0 - FINAL\n\n' +
                     'This will create:\n' +
                     '- Base plate (140x180x3mm) extruded DOWNWARD\n' +
                     '- Breadboard pocket (165.5x55.5x1.5mm)\n' +
                     '- 24 mounting holes (all cut DOWNWARD)\n' +
                     '- Text markings (FRONT + sensors)\n\n' +
                     'All operations use the same direction to avoid\n' +
                     '"No target body" errors.\n\n' +
                     'Click OK to continue.')
        
        # STEP 1: Create base plate (extruded DOWNWARD)
        ui.messageBox('Step 1/7: Creating base plate (extruding DOWNWARD)...')
        base_body = create_base_plate(component)
        
        if not base_body:
            ui.messageBox('Error: Failed to create base plate. Aborting.')
            return
        
        # STEP 2: Create breadboard pocket
        ui.messageBox('Step 2/7: Creating breadboard pocket...')
        create_breadboard_pocket(component, base_body)
        
        # STEP 3: Create corner mounting holes
        ui.messageBox('Step 3/7: Creating corner mounting holes...')
        create_corner_mounting_holes(component, base_body)
        
        # STEP 4: Create Mega mounting holes
        ui.messageBox('Step 4/7: Creating Elegoo Mega mounting holes...')
        create_mega_mounting_holes(component, base_body)
        
        # STEP 5: Create L298N mounting holes
        ui.messageBox('Step 5/7: Creating L298N mounting holes...')
        create_l298n_mounting_holes(component, base_body)
        
        # STEP 6: Create phone and sensor mounting holes
        ui.messageBox('Step 6/7: Creating phone and sensor mounting holes...')
        create_phone_mounting_holes(component, base_body)
        create_sensor_mounting_holes(component, base_body)
        
        # STEP 7: Create text markings
        ui.messageBox('Step 7/7: Creating text markings...')
        create_text_markings(component, base_body)
        
        # Fit view to show the complete model
        app.activeViewport.fit()
        
        ui.messageBox('✅ NexusTrack Core Carrier v3.0 generated successfully!\n\n' +
                     'Component: NexusTrack_Core_Carrier_v3\n' +
                     'Dimensions: 140x180x3mm\n' +
                     'Breadboard pocket: 165.5x55.5x1.5mm deep\n' +
                     'Mounting holes: 24 total\n' +
                     'Text markings: FRONT + 5 sensors\n\n' +
                     'Next steps:\n' +
                     '1. Review the design\n' +
                     '2. Add fillets to corners (optional)\n' +
                     '3. Export as STL for 3D printing\n\n' +
                     'Recommended print settings:\n' +
                     '- Material: PETG\n' +
                     '- Layer height: 0.2mm\n' +
                     '- Infill: 30-40%\n' +
                     '- Walls: 3-4 perimeters\n' +
                     '- Support: None needed')
        
    except:
        if ui:
            ui.messageBox(f'Failed:\n{traceback.format_exc()}')

def stop(context):
    """Called when the script is stopped."""
    pass
```

---

## Nyckelförändringar i v3.0

### 1. Basplattan extruderas NEDÅT
```python
# CRITICAL: Negative distance = extrude downward
distance_value = adsk.core.ValueInput.createByReal(-CARRIER_THICKNESS)
```

### 2. Alla cuts görs från XY-planet (toppen)
```python
# Create sketch on XY plane (TOP of base plate at Z=0)
sketch = component.sketches.add(component.xYConstructionPlane)
```

### 3. Alla cuts går NEDÅT
```python
# CRITICAL: Negative distance = cut downward
distance_value = adsk.core.ValueInput.createByReal(-CARRIER_THICKNESS)
```

### 4. Target body skickas till alla funktioner
```python
create_corner_mounting_holes(component, base_body)
create_mega_mounting_holes(component, base_body)
# etc...
```

---

## Användning

1. **Skapa ny fil:** `software/cad/generate_core_carrier_v3.py`
2. **Kopiera Python-koden** ovan (från `"""` till `pass`)
3. **Spara filen**
4. **Öppna Fusion 360**
5. **Kör skriptet:**
   - Tools → Add-Ins → Scripts and Add-Ins
   - Klicka "+" och välj `generate_core_carrier_v3.py`
   - Klicka "Run"
6. **Följ progress messages** (7 steg)
7. **Exportera STL** när klar

---
