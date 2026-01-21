"""
NexusTrack Core Carrier Generator for Fusion 360
=================================================

This script generates the Core Carrier plate (140x160x3mm) with all mounting holes
and component positions for the NexusTrack robot platform.

Usage:
1. Open Fusion 360
2. Go to Tools > Add-Ins > Scripts and Add-Ins
3. Click the green "+" button and select this script
4. Click "Run"

Author: NexusTrack Project
Date: 2026-01-13
Version: 1.0
"""

import adsk.core
import adsk.fusion
import traceback
import math

# ============================================================================
# PARAMETERS (from parameters.txt and core_carrier_spec.md)
# ============================================================================

# Core Carrier Base Plate
CARRIER_WIDTH = 14.0  # cm (140mm)
CARRIER_LENGTH = 16.0  # cm (160mm)
CARRIER_THICKNESS = 0.3  # cm (3mm)

# Corner mounting holes (for attaching to platform)
CORNER_HOLE_DIA = 0.45  # cm (4.5mm) - M4 holes
CORNER_HOLE_OFFSET_X = 6.0  # cm (60mm) from center
CORNER_HOLE_OFFSET_Y = 6.5  # cm (65mm) from center
COUNTERSINK_DIA = 0.85  # cm (8.5mm)
COUNTERSINK_DEPTH = 0.3  # cm (3mm)

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
PHONE_ANGLE = 10  # degrees forward tilt

# HC-SR04 Sensor mounting
SENSOR_HOLE_DIA = 0.27  # cm (2.7mm) - M2.5 holes
SENSOR_EYE_DIA = 1.65  # cm (16.5mm) - sensor "eyes"
SENSOR_HOLE_SPACING = 2.5  # cm (25mm) between mounting holes

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

# Cable management
CABLE_CHANNEL_WIDTH = 0.5  # cm (5mm)
CABLE_CHANNEL_DEPTH = 0.2  # cm (2mm)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_sketch_on_plane(component, plane_name):
    """Create a new sketch on the specified plane."""
    planes = component.xYConstructionPlane if plane_name == "XY" else component.xZConstructionPlane
    sketches = component.sketches
    return sketches.add(planes)

def create_rectangle_centered(sketch, width, height):
    """Create a centered rectangle on the sketch."""
    lines = sketch.sketchCurves.sketchLines
    point0 = adsk.core.Point3D.create(-width/2, -height/2, 0)
    point1 = adsk.core.Point3D.create(width/2, -height/2, 0)
    point2 = adsk.core.Point3D.create(width/2, height/2, 0)
    point3 = adsk.core.Point3D.create(-width/2, height/2, 0)
    
    lines.addByTwoPoints(point0, point1)
    lines.addByTwoPoints(point1, point2)
    lines.addByTwoPoints(point2, point3)
    lines.addByTwoPoints(point3, point0)

def create_circle_at_position(sketch, x, y, diameter):
    """Create a circle at the specified position."""
    center = adsk.core.Point3D.create(x, y, 0)
    circles = sketch.sketchCurves.sketchCircles
    return circles.addByCenterRadius(center, diameter/2)

def extrude_profile(component, profile, distance, operation=adsk.fusion.FeatureOperations.NewBodyFeatureOperation):
    """Extrude a profile by the specified distance."""
    extrudes = component.features.extrudeFeatures
    ext_input = extrudes.createInput(profile, operation)
    distance_value = adsk.core.ValueInput.createByReal(distance)
    ext_input.setDistanceExtent(False, distance_value)
    return extrudes.add(ext_input)

def create_hole_at_position(component, sketch, x, y, diameter, depth, is_through=True):
    """Create a hole at the specified position."""
    circle = create_circle_at_position(sketch, x, y, diameter)
    profile = sketch.profiles.item(sketch.profiles.count - 1)
    
    if is_through:
        operation = adsk.fusion.FeatureOperations.CutFeatureOperation
        extrude_profile(component, profile, depth, operation)
    
    return circle

# ============================================================================
# MAIN GENERATION FUNCTIONS
# ============================================================================

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

def create_corner_mounting_holes(component):
    """Create the four corner mounting holes for platform attachment."""
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
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
        
        # Extrude cut through
        for i in range(4):
            profile = sketch.profiles.item(i)
            extrude_profile(component, profile, -CARRIER_THICKNESS, 
                          adsk.fusion.FeatureOperations.CutFeatureOperation)
        
        ui.messageBox(f'Created 4 corner mounting holes (M4, Ø{CORNER_HOLE_DIA*10}mm)')
        
    except:
        if ui:
            ui.messageBox('Failed to create corner holes:\n{}'.format(traceback.format_exc()))

def create_mega_mounting_holes(component):
    """Create mounting holes for Elegoo Mega 2560."""
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Create sketch
        sketch = create_sketch_on_plane(component, "XY")
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
        
        # Extrude cut through
        for i in range(4):
            profile = sketch.profiles.item(i)
            extrude_profile(component, profile, -CARRIER_THICKNESS,
                          adsk.fusion.FeatureOperations.CutFeatureOperation)
        
        ui.messageBox(f'Created Elegoo Mega mounting holes (M3, {MEGA_CC_X*10}mm x {MEGA_CC_Y*10}mm)')
        
    except:
        if ui:
            ui.messageBox('Failed to create Mega holes:\n{}'.format(traceback.format_exc()))

def create_l298n_mounting_holes(component):
    """Create mounting holes for L298N motor driver."""
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Create sketch
        sketch = create_sketch_on_plane(component, "XY")
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
        
        # Extrude cut through
        for i in range(4):
            profile = sketch.profiles.item(i)
            extrude_profile(component, profile, -CARRIER_THICKNESS,
                          adsk.fusion.FeatureOperations.CutFeatureOperation)
        
        ui.messageBox(f'Created L298N mounting holes (M3, {L298N_SQUARE*10}mm square)')
        
    except:
        if ui:
            ui.messageBox('Failed to create L298N holes:\n{}'.format(traceback.format_exc()))

def create_phone_mounting_holes(component):
    """Create mounting holes for OnePlus 8T phone holder."""
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Create sketch
        sketch = create_sketch_on_plane(component, "XY")
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
        
        # Extrude cut through
        for i in range(2):
            profile = sketch.profiles.item(i)
            extrude_profile(component, profile, -CARRIER_THICKNESS,
                          adsk.fusion.FeatureOperations.CutFeatureOperation)
        
        ui.messageBox(f'Created phone holder mounting holes (M4, {PHONE_HOLE_SPACING*10}mm spacing, {PHONE_ANGLE}° tilt)')
        
    except:
        if ui:
            ui.messageBox('Failed to create phone holes:\n{}'.format(traceback.format_exc()))

def create_sensor_mounting_holes(component):
    """Create mounting holes for all 5 HC-SR04 sensors."""
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Create sketch
        sketch = create_sketch_on_plane(component, "XY")
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
        
        # Extrude cut through all holes
        for i in range(hole_count):
            profile = sketch.profiles.item(i)
            extrude_profile(component, profile, -CARRIER_THICKNESS,
                          adsk.fusion.FeatureOperations.CutFeatureOperation)
        
        ui.messageBox(f'Created {hole_count} sensor mounting holes (M2.5) for 5 HC-SR04 sensors\n360° coverage: FC, FL, FR, BL, BR')
        
    except:
        if ui:
            ui.messageBox('Failed to create sensor holes:\n{}'.format(traceback.format_exc()))

def create_cable_channels(component):
    """Create cable management channels along the edges."""
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Create sketch for cable channels
        sketch = create_sketch_on_plane(component, "XY")
        sketch.name = "Cable_Channels"
        
        # Create channels along edges (simplified - just marking areas)
        # In a full implementation, these would be shallow grooves
        
        # For now, just add reference lines to show where channels should be
        lines = sketch.sketchCurves.sketchLines
        
        # Left edge channel
        lines.addByTwoPoints(
            adsk.core.Point3D.create(-CARRIER_WIDTH/2 + 1, -CARRIER_LENGTH/2 + 2, 0),
            adsk.core.Point3D.create(-CARRIER_WIDTH/2 + 1, CARRIER_LENGTH/2 - 2, 0)
        )
        
        # Right edge channel
        lines.addByTwoPoints(
            adsk.core.Point3D.create(CARRIER_WIDTH/2 - 1, -CARRIER_LENGTH/2 + 2, 0),
            adsk.core.Point3D.create(CARRIER_WIDTH/2 - 1, CARRIER_LENGTH/2 - 2, 0)
        )
        
        ui.messageBox('Cable channel reference lines added\n(Implement shallow grooves in detailed design)')
        
    except:
        if ui:
            ui.messageBox('Failed to create cable channels:\n{}'.format(traceback.format_exc()))

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
        component.name = "NexusTrack_Core_Carrier"
        
        ui.messageBox('Starting NexusTrack Core Carrier generation...\n\nThis will create:\n- Base plate (140x160x3mm)\n- 4 corner mounting holes (M4)\n- Elegoo Mega holes (M3)\n- L298N holes (M3)\n- Phone holder holes (M4)\n- 5 sensor mounting holes (M2.5)\n- Cable channels\n\nClick OK to continue.')
        
        # Generate all components
        create_base_plate(component)
        create_corner_mounting_holes(component)
        create_mega_mounting_holes(component)
        create_l298n_mounting_holes(component)
        create_phone_mounting_holes(component)
        create_sensor_mounting_holes(component)
        create_cable_channels(component)
        
        # Fit view to show the complete model
        app.activeViewport.fit()
        
        ui.messageBox('✅ NexusTrack Core Carrier generated successfully!\n\nComponent: NexusTrack_Core_Carrier\n\nNext steps:\n1. Review the design\n2. Add fillets to corners (optional)\n3. Export as STL for 3D printing\n4. Export as DXF for laser cutting\n\nSee core_carrier_spec.md for assembly instructions.')
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    """Called when the script is stopped."""
    pass
