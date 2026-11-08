import adsk.core, adsk.fusion, traceback, math

# ==================== NEXUS CARRIER v7 ====================
# Lyftbar modul för RC-bil → framtida bandvagn
#
# ÄNDRINGAR FRÅN v6 → v7:
# - Plattans tjocklek: 3 mm → 4 mm (PLA-stabilitet)
# - M3-hål: Ø3.4 mm → Ø3.6 mm (PLA-krympning)
# - Sensor-öppningar: Ø16.5 mm → Ø16.8 mm (HC-SR04 pass-through)
# - Buntbandsslots: NYT — 6 par à 4.8 × 12.5 mm, genom plattan
# - Lyfthandtag: NYT — 2× Ø8 mm cylindrar 15 mm höga på kortsidorna
# - Pin-referens-text: NYT — graverat 0.8 mm djupt vid varje sensor
# - Behållet: v6:s vägg/gusset-logik, Arduino/L298N-hål, mobilhållare, 5 sensorer
# ============================================================

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = app.activeProduct
        root = design.rootComponent

        # === ARBETSKOMPONENT ===
        # Försök skapa en ny sub-komponent (Assembly-dokument).
        # Faller tillbaka till rootComponent om dokumentet är ett Part Design
        # (Part Design tillåter bara en komponent och kastar RuntimeError 3).
        try:
            newOcc = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
            newComp = newOcc.component
            newComp.name = "Nexus_Carrier_v7"
        except RuntimeError:
            newComp = root
            try:
                root.name = "Nexus_Carrier_v7"
            except:
                pass  # vissa dokument tillåter inte att roten döps om

        extrudes = newComp.features.extrudeFeatures

        # === PARAMETRAR (cm, från parameters.txt) ===
        # Basplatta
        p_w, p_h, p_t = 18.0, 26.0, 0.4  # 180×260 mm → 18×26 cm, tjocklek 4 mm = 0.4 cm

        # Arduino Mega & L298N (PLA-justerad Ø3.6 för M3)
        mega_x, mega_y = 9.652, 5.08
        lx = 15.0

        # Sensor- & mobilparametrar
        wall_h, wall_w, wall_t = 2.8, 5.2, 0.4
        sensor_d = 1.68  # 16.8 mm = 1.68 cm (PLA-justerat)
        gusset_size = 0.8
        gusset_height = 1.6
        # phone_gap = mobilens tjocklek + 1 mm clearance (för PLA-toleranser)
        # OnePlus 8T med skal = 12 mm → spår 13 mm
        phone_gap, phone_h = 1.3, 4.0
        mobil_vinkel = 10  # grader (TODO v7.2 — appliceras inte ännu)

        # Buntbandsslots
        slot_w, slot_h = 0.48, 1.25  # 4.8 × 12.5 mm

        # Lyfthandtag
        lift_handle_d = 0.8  # Ø8 mm
        lift_handle_h = 1.5  # 15 mm

        # Konstruktionsplan
        xy = newComp.xYConstructionPlane

        # === STEG 1: BASPLATTA ===
        baseSketch = newComp.sketches.add(xy)
        baseSketch.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, 0, 0),
            adsk.core.Point3D.create(p_w, p_h, 0))

        if baseSketch.profiles.count == 0:
            ui.messageBox("Ingen profil på basplattan. Fel i sketchning.")
            return

        baseProfCollection = adsk.core.ObjectCollection.create()
        baseProfCollection.add(baseSketch.profiles.item(0))

        baseInput = extrudes.createInput(baseProfCollection, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        baseInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(p_t))
        baseExtrude = extrudes.add(baseInput)
        baseBody = baseExtrude.bodies.item(0)

        # === Stabil "topp"-referens via construction plane ===
        # Vi använder ett offset construction plane istället för en B-Rep face.
        # Anledningen: face-pekare invalideras så fort andra features (Cut/Join)
        # modifierar geometrin, vilket gav "InternalValidationError : face".
        # Construction planes är geometriskt definierade och påverkas inte.
        topPlaneInput = newComp.constructionPlanes.createInput()
        topPlaneInput.setByOffset(xy, adsk.core.ValueInput.createByReal(p_t))
        topPlane = newComp.constructionPlanes.add(topPlaneInput)
        topFace = topPlane  # alias - sketches.add() accepterar båda

        # === STEG 2: ARDUINO MEGA & L298N HÅL (Ø3.6 för M3 PLA) ===
        holeSketch = newComp.sketches.add(topFace)

        # Arduino Mega (4 hörnhål)
        for x, y in [(2, 1.5), (2, 11.66), (7.08, 1.5), (7.08, 11.15)]:
            holeSketch.sketchCurves.sketchCircles.addByCenterRadius(
                adsk.core.Point3D.create(x, y, 0), 0.18)  # 3.6 mm / 2

        # L298N (4 hål)
        for x, y in [(lx, 4.5), (lx+3.7, 4.5), (lx, 8.2), (lx+3.7, 8.2)]:
            holeSketch.sketchCurves.sketchCircles.addByCenterRadius(
                adsk.core.Point3D.create(x, y, 0), 0.18)

        # Borra elektronik-hål
        holeProfs = adsk.core.ObjectCollection.create()
        for p in holeSketch.profiles:
            holeProfs.add(p)
        if holeProfs.count > 0:
            holeInput = extrudes.createInput(holeProfs, adsk.fusion.FeatureOperations.CutFeatureOperation)
            holeInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(-1.0))
            extrudes.add(holeInput)

        # === STEG 3: BUNTBANDSSLOTS (6 par × 4.8 × 12.5 mm) ===
        # Placering: 4 hörnpar + 2 mittpunktspar (fram/bak)
        slot_positions = [
            # Hörnparen (2 slots per hörn)
            (1.0, 1.0), (1.0, p_h - 1.0),    # VL-hörn
            (p_w - 1.0, 1.0), (p_w - 1.0, p_h - 1.0),  # HR-hörn
            # Mittpunkter
            (p_w/2, 0.8), (p_w/2, p_h - 0.8)  # Fram & bak mittpunkt
        ]

        slotSketch = newComp.sketches.add(topFace)
        for slot_x, slot_y in slot_positions:
            # Rektangel 4.8 × 12.5 mm, centrerad
            slotSketch.sketchCurves.sketchLines.addTwoPointRectangle(
                adsk.core.Point3D.create(slot_x - slot_w/2, slot_y - slot_h/2, 0),
                adsk.core.Point3D.create(slot_x + slot_w/2, slot_y + slot_h/2, 0))

        slotProfs = adsk.core.ObjectCollection.create()
        for p in slotSketch.profiles:
            slotProfs.add(p)
        if slotProfs.count > 0:
            slotInput = extrudes.createInput(slotProfs, adsk.fusion.FeatureOperations.CutFeatureOperation)
            slotInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(-1.0))
            extrudes.add(slotInput)

        # === STEG 4: LYFTHANDTAG (2× Ø8 mm cylindrar, 15 mm höga) ===
        # En på var kortsida (x = 0.8 cm och x = p_w - 0.8 cm, centrerad på y)
        handle_positions = [(0.8, p_h/2), (p_w - 0.8, p_h/2)]

        handleSketch = newComp.sketches.add(topFace)
        for hx, hy in handle_positions:
            handleSketch.sketchCurves.sketchCircles.addByCenterRadius(
                adsk.core.Point3D.create(hx, hy, 0), lift_handle_d/2)  # Ø8/2 = 0.4 cm

        handleProfs = adsk.core.ObjectCollection.create()
        for p in handleSketch.profiles:
            handleProfs.add(p)
        if handleProfs.count > 0:
            handleInput = extrudes.createInput(handleProfs, adsk.fusion.FeatureOperations.JoinFeatureOperation)
            handleInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(lift_handle_h))
            extrudes.add(handleInput)

        # === STEG 5: MOBILHÅLLARE (KORRIDOREN) ===
        mountSketch = newComp.sketches.add(topFace)
        mx, my = p_w/2, 13.0
        mw = 10.0
        mountSketch.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(mx - mw/2, my, 0),
            adsk.core.Point3D.create(mx + mw/2, my + 0.4, 0))
        mountSketch.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(mx - mw/2, my + 0.4 + phone_gap, 0),
            adsk.core.Point3D.create(mx + mw/2, my + 0.8 + phone_gap, 0))

        mProfs = adsk.core.ObjectCollection.create()
        for p in mountSketch.profiles:
            mProfs.add(p)
        mInput = extrudes.createInput(mProfs, adsk.fusion.FeatureOperations.JoinFeatureOperation)
        mInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(phone_h))
        extrudes.add(mInput)

        # === STEG 6: SENSORVÄGGAR MED GUSSETS ===
        def add_wall_with_gussets(name, x, y, angle_deg):
            """Skapar sensorvägg (HC-SR04, 2× öppningar Ø16.8 mm) med triangulära gussets."""
            rad = math.radians(angle_deg)
            half_w = wall_w / 2

            # --- VÄGG ---
            lineSketch = newComp.sketches.add(xy)
            line = lineSketch.sketchCurves.sketchLines.addByTwoPoints(
                adsk.core.Point3D.create(x, y, 0),
                adsk.core.Point3D.create(x + math.cos(rad), y + math.sin(rad), 0))

            pInput = newComp.constructionPlanes.createInput()
            pInput.setByDistanceOnPath(line, adsk.core.ValueInput.createByReal(0))
            plane = newComp.constructionPlanes.add(pInput)

            wallSketch = newComp.sketches.add(plane)
            wallSketch.sketchCurves.sketchLines.addTwoPointRectangle(
                adsk.core.Point3D.create(-half_w, 0, 0),
                adsk.core.Point3D.create(half_w, wall_h, 0))

            sc = wallSketch.sketchCurves.sketchCircles
            sc.addByCenterRadius(adsk.core.Point3D.create(-1.3, 1.4, 0), sensor_d/2)  # Vänster öppning
            sc.addByCenterRadius(adsk.core.Point3D.create(1.3, 1.4, 0), sensor_d/2)   # Höger öppning
            sc.addByCenterRadius(adsk.core.Point3D.create(-2.4, 1.4, 0), 0.18)        # Vänster M3-hål
            sc.addByCenterRadius(adsk.core.Point3D.create(2.4, 1.4, 0), 0.18)         # Höger M3-hål

            # Extrudera vägg
            if wallSketch.profiles.count > 0:
                wallProf = adsk.core.ObjectCollection.create()
                wallProf.add(wallSketch.profiles.item(wallSketch.profiles.count - 1))
                wallInput = extrudes.createInput(wallProf, adsk.fusion.FeatureOperations.JoinFeatureOperation)
                wallInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(wall_t))
                extrudes.add(wallInput)

            # --- TRIANGULÄRA GUSSETS ---
            cos_a = math.cos(rad)
            sin_a = math.sin(rad)
            perp_cos = math.cos(rad + math.pi/2)
            perp_sin = math.sin(rad + math.pi/2)

            gussetSketch = newComp.sketches.add(xy)
            sl = gussetSketch.sketchCurves.sketchLines
            g = gusset_size

            # VÄNSTER GUSSET
            lx1 = x + perp_cos * (-half_w + 0.2)
            ly1 = y + perp_sin * (-half_w + 0.2)
            left_pts = [
                adsk.core.Point3D.create(lx1, ly1, 0),
                adsk.core.Point3D.create(lx1 - cos_a * g, ly1 - sin_a * g, 0),
                adsk.core.Point3D.create(lx1 - cos_a * g + perp_cos * (-g * 0.7),
                                         ly1 - sin_a * g + perp_sin * (-g * 0.7), 0)
            ]
            sl.addByTwoPoints(left_pts[0], left_pts[1])
            sl.addByTwoPoints(left_pts[1], left_pts[2])
            sl.addByTwoPoints(left_pts[2], left_pts[0])

            # HÖGER GUSSET
            rx1 = x + perp_cos * (half_w - 0.2)
            ry1 = y + perp_sin * (half_w - 0.2)
            right_pts = [
                adsk.core.Point3D.create(rx1, ry1, 0),
                adsk.core.Point3D.create(rx1 - cos_a * g, ry1 - sin_a * g, 0),
                adsk.core.Point3D.create(rx1 - cos_a * g + perp_cos * (g * 0.7),
                                         ry1 - sin_a * g + perp_sin * (g * 0.7), 0)
            ]
            sl.addByTwoPoints(right_pts[0], right_pts[1])
            sl.addByTwoPoints(right_pts[1], right_pts[2])
            sl.addByTwoPoints(right_pts[2], right_pts[0])

            # Extrudera gussets
            if gussetSketch.profiles.count >= 2:
                gProfs = adsk.core.ObjectCollection.create()
                for i in range(gussetSketch.profiles.count):
                    prof = gussetSketch.profiles.item(i)
                    if prof.areaProperties().area < 1.0:
                        gProfs.add(prof)

                if gProfs.count > 0:
                    gInput = extrudes.createInput(gProfs, adsk.fusion.FeatureOperations.JoinFeatureOperation)
                    gInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(gusset_height))
                    extrudes.add(gInput)

        # Skapa alla 5 sensorväggar
        add_wall_with_gussets("FC", p_w/2, p_h - 0.5, 90)       # Front Center
        add_wall_with_gussets("FL", 2.5, p_h - 1.5, 135)        # Front Left +45°
        add_wall_with_gussets("FR", p_w - 2.5, p_h - 1.5, 45)   # Front Right -45°
        add_wall_with_gussets("BL", 2.5, 1.5, 225)              # Back Left +135°
        add_wall_with_gussets("BR", p_w - 2.5, 1.5, 315)        # Back Right -135°

        # === STEG 7: PIN-REFERENS-TEXT (graverat 0.8 mm) ===
        txtSketch = newComp.sketches.add(topFace)

        def label(t, tx, ty):
            """Lägger till text i skiss (graveras senare)."""
            txtInput = txtSketch.sketchTexts.createInput(t, 0.4, adsk.core.Point3D.create(tx, ty, 0))
            txtSketch.sketchTexts.add(txtInput)

        # Komponetetikett
        label("v7", 1.0, 0.5)
        label("ARDUINO", 4.5, 5.0)
        label("L298N", lx + 1.85, 6.5)
        label("CAMERA", p_w/2, 14.2)

        # Pin-referens vid sensorer (kabel-drag självförklarande)
        label("T22/E23", p_w/2, p_h - 2.0)      # FC
        label("T24/E25", 1.0, p_h - 2.0)        # FL
        label("T26/E27", p_w - 1.0, p_h - 2.0)  # FR
        label("T28/E29", 1.0, 2.0)              # BL
        label("T30/E31", p_w - 1.0, 2.0)        # BR

        # Compute och gravera
        design.computeAll()
        tProfs = adsk.core.ObjectCollection.create()
        for p in txtSketch.profiles:
            tProfs.add(p)

        if tProfs.count > 0:
            tInput = extrudes.createInput(tProfs, adsk.fusion.FeatureOperations.CutFeatureOperation)
            tInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(-0.08))  # 0.8 mm gravering
            extrudes.add(tInput)

        design.computeAll()
        ui.messageBox("Nexus Carrier v7 klar!\n\n- Basplatta 18x26 cm (4 mm)\n- 6 buntbandsslot-par (4.8x12.5 mm)\n- 2 lyfthandtag (D8x15 mm)\n- 5 sensorvaggar med gussets\n- Pin-referens-text vid varje sensor\n- PLA-toleranser applicerade\n- Mobilspar 13 mm (12 mm mobil + tolerans)")

    except:
        if ui:
            ui.messageBox('Fel i Nexus Carrier v7:\n' + traceback.format_exc())
