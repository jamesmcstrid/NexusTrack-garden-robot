import adsk.core, adsk.fusion, traceback, math

# ==================== NEXUS CARRIER v8.1 ====================
# Tvåvånings robotplattform för Ender 3 (235×235 mm buildvolym)
#
# ÄNDRINGAR FRÅN v8 → v8.1 (BUGFIXES):
# - Bug 1 (rad 282-287): Sensor-vägg profile-val nu max-area-baserat istället för index
#   * Åtgärd: Loop genom profiler, välj den med störst area (rektangel-med-hål)
# - Bug 2 (rad 227): Mobilhållare väggas bredd ökat från 1.3 cm → 10.0 cm
#   * Åtgärd: Ändrat mw = 1.3 → mw = 10.0 för att passa 74 mm mobil
# - Bug 3: Gussets för mobilhållare tillagda (efter rad 253)
#   * Åtgärd: 4 triangulära gussets (2 per vägg) på utsidorna, 1×2×1 cm
#
# TIDIGARE ÄNDRINGAR (v7 → v8):
# - Arkitektur: 1 platta → 3 bodies (Lower_Floor, Upper_Floor, Pillar)
# - Lower_Floor (18×13×0.4 cm): Arduino Mega + L298N elektronik
#   * Mega hålbild 96.52×50.8 mm, placerad framåt (x∈[2,12.52], y∈[1,6.08])
#   * L298N 37×37 mm höger om Mega
#   * Breadboard-zon visuell text "BB 830" centrerad på y=10 cm
#   * 4 pelar-hål Ø3.6 mm för genomgångsbultar (placering justerad för no-crop)
#   * 6 buntbandsslots 4.8×12.5 mm
#   * Pin-text "MEGA" och "L298N"
# - Upper_Floor (18×13×0.4 cm): Mobilhållare + 5 HC-SR04 sensorer
#   * Mobilhållare 13 mm spår, tilt-kil +2.3 mm för 10° lutning
#   * 5 sensorväggar samma som v7 men anpassade för 13 cm djup
#   * 4 pelar-hål i SAMMA position som Lower_Floor
#   * Pin-referens-text vid varje sensor (T22/E23, etc.)
#   * Lyfthandtag SKIPPED (utrymme för sensorer prioriterat)
# - Pillar: 1× Ø10×40 mm cylinder med M3-genomgångshål centralt
#   Placerad sidoställd för printning; användaren printar 4× denna.
# - Stackning: Lower vid z=0, Upper vid z=4.4 cm (+4 mm platta + 40 mm pelare)
# - PLA-toleranser: Ø3.6 mm för M3, Ø16.8 mm för HC-SR04
# ============================================================

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        ui.messageBox("CHECKPOINT 1: Skriptet startar (v8.1 debug)")
        design = app.activeProduct
        root = design.rootComponent

        # === ARBETSKOMPONENT ===
        try:
            newOcc = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
            newComp = newOcc.component
            newComp.name = "Nexus_Carrier_v8"
        except RuntimeError:
            newComp = root
            try:
                root.name = "Nexus_Carrier_v8"
            except:
                pass

        extrudes = newComp.features.extrudeFeatures
        ui.messageBox("CHECKPOINT 2: Komponent skapad")

        # === PARAMETRAR (cm) ===
        # Plattorna
        p_w, p_h, p_t = 18.0, 13.0, 0.4  # 180×130 mm, 4 mm tjocklek

        # Elektronik
        mega_x, mega_y = 9.652, 5.08
        lx = 15.0
        l298n_dist = 3.7

        # Sensorer & mobilhållare
        wall_h, wall_w, wall_t = 2.8, 5.2, 0.4
        sensor_d = 1.68  # 16.8 mm HC-SR04
        gusset_size = 0.8
        gusset_height = 1.6
        phone_gap, phone_h = 1.3, 4.0
        mobil_vinkel = 10  # grader

        # Buntbandsslots
        slot_w, slot_h = 0.48, 1.25

        # Pelar
        pillar_d = 1.0  # Ø10 mm
        pillar_h = 4.0  # 40 mm
        pillar_hole_d = 0.18  # Ø3.6 mm M3-hål

        # Pelarhål i plattorna (justerat för no-crop med komponenter)
        # Placering: långt in från kanterna, mellan elektronikzoner
        pillar_holes = [(1.5, 6.5), (16.5, 6.5), (5.0, 12.5), (13.0, 12.5)]

        # Konstruktionsplaner
        xy = newComp.xYConstructionPlane

        # ===== LOWER_FLOOR =====
        # === STEG L1: BASPLATTA ===
        baseSketch = newComp.sketches.add(xy)
        baseSketch.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, 0, 0),
            adsk.core.Point3D.create(p_w, p_h, 0))

        if baseSketch.profiles.count == 0:
            ui.messageBox("Ingen profil på Lower-platta. Fel i sketchning.")
            return

        baseProfCollection = adsk.core.ObjectCollection.create()
        baseProfCollection.add(baseSketch.profiles.item(0))

        baseInput = extrudes.createInput(baseProfCollection, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        baseInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(p_t))
        baseExtrude = extrudes.add(baseInput)
        baseBody = baseExtrude.bodies.item(0)

        # Offset construction plane för Lower-topp
        lowerTopPlaneInput = newComp.constructionPlanes.createInput()
        lowerTopPlaneInput.setByOffset(xy, adsk.core.ValueInput.createByReal(p_t))
        lowerTopPlane = newComp.constructionPlanes.add(lowerTopPlaneInput)

        # === STEG L2: ELEKTRONIK-HÅL (Mega + L298N) ===
        lowerHoleSketch = newComp.sketches.add(lowerTopPlane)

        # Arduino Mega (4 hörnhål på v7-positions)
        mega_holes = [(2, 1), (2, 1 + mega_y), (2 + mega_x, 1), (2 + mega_x, 1 + mega_y)]
        for x, y in mega_holes:
            lowerHoleSketch.sketchCurves.sketchCircles.addByCenterRadius(
                adsk.core.Point3D.create(x, y, 0), pillar_hole_d)

        # L298N (4 hål, 37×37 mm höger om Mega)
        l298n_holes = [(lx, 1), (lx + l298n_dist, 1), (lx, 1 + l298n_dist), (lx + l298n_dist, 1 + l298n_dist)]
        for x, y in l298n_holes:
            lowerHoleSketch.sketchCurves.sketchCircles.addByCenterRadius(
                adsk.core.Point3D.create(x, y, 0), pillar_hole_d)

        # Pelarhål
        for px, py in pillar_holes:
            lowerHoleSketch.sketchCurves.sketchCircles.addByCenterRadius(
                adsk.core.Point3D.create(px, py, 0), pillar_hole_d)

        lowerHoleProfs = adsk.core.ObjectCollection.create()
        for p in lowerHoleSketch.profiles:
            lowerHoleProfs.add(p)
        if lowerHoleProfs.count > 0:
            lowerHoleInput = extrudes.createInput(lowerHoleProfs, adsk.fusion.FeatureOperations.CutFeatureOperation)
            lowerHoleInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(-1.0))
            extrudes.add(lowerHoleInput)

        # === STEG L3: BUNTBANDSSLOTS ===
        lower_slot_positions = [
            (1.0, 1.0), (1.0, p_h - 1.0),
            (p_w - 1.0, 1.0), (p_w - 1.0, p_h - 1.0),
            (p_w/2, 0.8), (p_w/2, p_h - 0.8)
        ]

        lowerSlotSketch = newComp.sketches.add(lowerTopPlane)
        for slot_x, slot_y in lower_slot_positions:
            lowerSlotSketch.sketchCurves.sketchLines.addTwoPointRectangle(
                adsk.core.Point3D.create(slot_x - slot_w/2, slot_y - slot_h/2, 0),
                adsk.core.Point3D.create(slot_x + slot_w/2, slot_y + slot_h/2, 0))

        lowerSlotProfs = adsk.core.ObjectCollection.create()
        for p in lowerSlotSketch.profiles:
            lowerSlotProfs.add(p)
        if lowerSlotProfs.count > 0:
            lowerSlotInput = extrudes.createInput(lowerSlotProfs, adsk.fusion.FeatureOperations.CutFeatureOperation)
            lowerSlotInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(-1.0))
            extrudes.add(lowerSlotInput)

        # === STEG L4: PIN-TEXT (MEGA, L298N, BB) ===
        lowerTxtSketch = newComp.sketches.add(lowerTopPlane)

        def label(txt_obj, t, tx, ty):
            """Lägger till text i skiss."""
            txtInput = txt_obj.sketchTexts.createInput(t, 0.4, adsk.core.Point3D.create(tx, ty, 0))
            txt_obj.sketchTexts.add(txtInput)

        label(lowerTxtSketch, "MEGA", 3.5, 3.5)
        label(lowerTxtSketch, "L298N", lx + 1.2, 2.5)
        label(lowerTxtSketch, "BB 830", p_w/2, 10.0)
        label(lowerTxtSketch, "v8", 1.0, 0.5)

        design.computeAll()
        lowerTxtProfs = adsk.core.ObjectCollection.create()
        for p in lowerTxtSketch.profiles:
            lowerTxtProfs.add(p)

        if lowerTxtProfs.count > 0:
            lowerTxtInput = extrudes.createInput(lowerTxtProfs, adsk.fusion.FeatureOperations.CutFeatureOperation)
            lowerTxtInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(-0.08))
            extrudes.add(lowerTxtInput)

        design.computeAll()

        # ===== UPPER_FLOOR (versatt i z = +4.4 cm) =====
        # Skapa construction plane för Upper-basen
        upperBasePlaneInput = newComp.constructionPlanes.createInput()
        upperBasePlaneInput.setByOffset(xy, adsk.core.ValueInput.createByReal(p_t + pillar_h))
        upperBasePlane = newComp.constructionPlanes.add(upperBasePlaneInput)

        # === STEG U1: BASPLATTA (NewBodyFeatureOperation för ny body) ===
        upperBaseSketch = newComp.sketches.add(upperBasePlane)
        upperBaseSketch.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, 0, 0),
            adsk.core.Point3D.create(p_w, p_h, 0))

        if upperBaseSketch.profiles.count == 0:
            ui.messageBox("Ingen profil på Upper-platta.")
            return

        upperBaseProfCollection = adsk.core.ObjectCollection.create()
        upperBaseProfCollection.add(upperBaseSketch.profiles.item(0))

        upperBaseInput = extrudes.createInput(upperBaseProfCollection, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        upperBaseInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(p_t))
        upperBaseExtrude = extrudes.add(upperBaseInput)
        upperBaseBody = upperBaseExtrude.bodies.item(0)

        # Offset plane för Upper-topp
        upperTopPlaneInput = newComp.constructionPlanes.createInput()
        upperTopPlaneInput.setByOffset(upperBasePlane, adsk.core.ValueInput.createByReal(p_t))
        upperTopPlane = newComp.constructionPlanes.add(upperTopPlaneInput)

        # === STEG U2: PELAR-HÅL (samma som Lower) ===
        ui.messageBox("CHECKPOINT 4: Lower_Floor helt klar, startar Upper")
        upperHoleSketch = newComp.sketches.add(upperTopPlane)
        for px, py in pillar_holes:
            upperHoleSketch.sketchCurves.sketchCircles.addByCenterRadius(
                adsk.core.Point3D.create(px, py, 0), pillar_hole_d)

        upperHoleProfs = adsk.core.ObjectCollection.create()
        for p in upperHoleSketch.profiles:
            upperHoleProfs.add(p)
        if upperHoleProfs.count > 0:
            upperHoleInput = extrudes.createInput(upperHoleProfs, adsk.fusion.FeatureOperations.CutFeatureOperation)
            upperHoleInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(-1.0))
            extrudes.add(upperHoleInput)

        # === STEG U3: MOBILHÅLLARE (13 mm spår med tilt-kil) ===
        # Spår-vägg 1 (botten)
        mobileWall1Sketch = newComp.sketches.add(upperTopPlane)
        mx = p_w/2
        my = 4.0  # Position i y för mobilhållare
        mw = 10.0  # Hållare-bredd 10 cm (≈ 74 mm mobil + 13 mm marginal)

        mobileWall1Sketch.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(mx - mw/2, my, 0),
            adsk.core.Point3D.create(mx + mw/2, my + 0.4, 0))

        mProfs1 = adsk.core.ObjectCollection.create()
        for p in mobileWall1Sketch.profiles:
            mProfs1.add(p)
        mInput1 = extrudes.createInput(mProfs1, adsk.fusion.FeatureOperations.JoinFeatureOperation)
        mInput1.setDistanceExtent(False, adsk.core.ValueInput.createByReal(phone_h))
        extrudes.add(mInput1)

        # Spår-vägg 2 (topp, med tilt-offset)
        mobileWall2Sketch = newComp.sketches.add(upperTopPlane)
        tilt_offset = 0.23  # 2.3 mm tilt för 10° lutning

        mobileWall2Sketch.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(mx - mw/2, my + phone_gap + tilt_offset, 0),
            adsk.core.Point3D.create(mx + mw/2, my + phone_gap + tilt_offset + 0.4, 0))

        mProfs2 = adsk.core.ObjectCollection.create()
        for p in mobileWall2Sketch.profiles:
            mProfs2.add(p)
        mInput2 = extrudes.createInput(mProfs2, adsk.fusion.FeatureOperations.JoinFeatureOperation)
        mInput2.setDistanceExtent(False, adsk.core.ValueInput.createByReal(phone_h))
        extrudes.add(mInput2)

        # === STEG U3B: GUSSETS FÖR MOBILHÅLLARE (BUG FIX 3) ===
        # 4 triangulära gussets: 2 per vägg, på utsidorna
        # Vägg 1 gussets (negativ y-riktning)
        mobileGusset1Sketch = newComp.sketches.add(upperTopPlane)
        gusset_base = 1.0  # 1 cm bas
        gusset_height_mobile = 1.5  # 1.5 cm höjd

        # Vägg 1, vänster gusset
        g1_x = mx - mw/2
        g1_y = my
        mobileGusset1Sketch.sketchCurves.sketchLines.addByTwoPoints(
            adsk.core.Point3D.create(g1_x, g1_y, 0),
            adsk.core.Point3D.create(g1_x - gusset_height_mobile, g1_y - gusset_base, 0))
        mobileGusset1Sketch.sketchCurves.sketchLines.addByTwoPoints(
            adsk.core.Point3D.create(g1_x - gusset_height_mobile, g1_y - gusset_base, 0),
            adsk.core.Point3D.create(g1_x, g1_y - 0.4, 0))
        mobileGusset1Sketch.sketchCurves.sketchLines.addByTwoPoints(
            adsk.core.Point3D.create(g1_x, g1_y - 0.4, 0),
            adsk.core.Point3D.create(g1_x, g1_y, 0))

        # Vägg 1, höger gusset
        g1_x_right = mx + mw/2
        mobileGusset1Sketch.sketchCurves.sketchLines.addByTwoPoints(
            adsk.core.Point3D.create(g1_x_right, g1_y, 0),
            adsk.core.Point3D.create(g1_x_right + gusset_height_mobile, g1_y - gusset_base, 0))
        mobileGusset1Sketch.sketchCurves.sketchLines.addByTwoPoints(
            adsk.core.Point3D.create(g1_x_right + gusset_height_mobile, g1_y - gusset_base, 0),
            adsk.core.Point3D.create(g1_x_right, g1_y - 0.4, 0))
        mobileGusset1Sketch.sketchCurves.sketchLines.addByTwoPoints(
            adsk.core.Point3D.create(g1_x_right, g1_y - 0.4, 0),
            adsk.core.Point3D.create(g1_x_right, g1_y, 0))

        mGusset1Profs = adsk.core.ObjectCollection.create()
        for p in mobileGusset1Sketch.profiles:
            mGusset1Profs.add(p)
        if mGusset1Profs.count > 0:
            mGusset1Input = extrudes.createInput(mGusset1Profs, adsk.fusion.FeatureOperations.JoinFeatureOperation)
            mGusset1Input.setDistanceExtent(False, adsk.core.ValueInput.createByReal(1.0))
            extrudes.add(mGusset1Input)

        # Vägg 2 gussets (positiv y-riktning)
        mobileGusset2Sketch = newComp.sketches.add(upperTopPlane)
        g2_y = my + phone_gap + tilt_offset

        # Vägg 2, vänster gusset
        g2_x = mx - mw/2
        mobileGusset2Sketch.sketchCurves.sketchLines.addByTwoPoints(
            adsk.core.Point3D.create(g2_x, g2_y + 0.4, 0),
            adsk.core.Point3D.create(g2_x - gusset_height_mobile, g2_y + 0.4 + gusset_base, 0))
        mobileGusset2Sketch.sketchCurves.sketchLines.addByTwoPoints(
            adsk.core.Point3D.create(g2_x - gusset_height_mobile, g2_y + 0.4 + gusset_base, 0),
            adsk.core.Point3D.create(g2_x, g2_y + 0.4, 0))
        mobileGusset2Sketch.sketchCurves.sketchLines.addByTwoPoints(
            adsk.core.Point3D.create(g2_x, g2_y + 0.4, 0),
            adsk.core.Point3D.create(g2_x, g2_y, 0))
        mobileGusset2Sketch.sketchCurves.sketchLines.addByTwoPoints(
            adsk.core.Point3D.create(g2_x, g2_y, 0),
            adsk.core.Point3D.create(g2_x - gusset_height_mobile, g2_y + 0.4 + gusset_base, 0))

        # Vägg 2, höger gusset
        g2_x_right = mx + mw/2
        mobileGusset2Sketch.sketchCurves.sketchLines.addByTwoPoints(
            adsk.core.Point3D.create(g2_x_right, g2_y + 0.4, 0),
            adsk.core.Point3D.create(g2_x_right + gusset_height_mobile, g2_y + 0.4 + gusset_base, 0))
        mobileGusset2Sketch.sketchCurves.sketchLines.addByTwoPoints(
            adsk.core.Point3D.create(g2_x_right + gusset_height_mobile, g2_y + 0.4 + gusset_base, 0),
            adsk.core.Point3D.create(g2_x_right, g2_y + 0.4, 0))
        mobileGusset2Sketch.sketchCurves.sketchLines.addByTwoPoints(
            adsk.core.Point3D.create(g2_x_right, g2_y + 0.4, 0),
            adsk.core.Point3D.create(g2_x_right, g2_y, 0))
        mobileGusset2Sketch.sketchCurves.sketchLines.addByTwoPoints(
            adsk.core.Point3D.create(g2_x_right, g2_y, 0),
            adsk.core.Point3D.create(g2_x_right + gusset_height_mobile, g2_y + 0.4 + gusset_base, 0))

        mGusset2Profs = adsk.core.ObjectCollection.create()
        for p in mobileGusset2Sketch.profiles:
            mGusset2Profs.add(p)
        if mGusset2Profs.count > 0:
            mGusset2Input = extrudes.createInput(mGusset2Profs, adsk.fusion.FeatureOperations.JoinFeatureOperation)
            mGusset2Input.setDistanceExtent(False, adsk.core.ValueInput.createByReal(1.0))
            extrudes.add(mGusset2Input)

        # === STEG U4: SENSORVÄGGAR MED GUSSETS (5 stycken, anpassade för 13 cm djup) ===
        ui.messageBox("CHECKPOINT 5: Mobilhållare klar, startar sensorer")
        def add_wall_with_gussets_upper(name, x, y, angle_deg):
            """Sensorvägg för Upper_Floor med gussets."""
            rad = math.radians(angle_deg)
            half_w = wall_w / 2

            # Vägg — skissa på upperTopPlane (Z=4.4 cm) så väggen sitter på övre plattan
            lineSketch = newComp.sketches.add(upperTopPlane)
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
            sc.addByCenterRadius(adsk.core.Point3D.create(-1.3, 1.4, 0), sensor_d/2)
            sc.addByCenterRadius(adsk.core.Point3D.create(1.3, 1.4, 0), sensor_d/2)
            sc.addByCenterRadius(adsk.core.Point3D.create(-2.4, 1.4, 0), pillar_hole_d)
            sc.addByCenterRadius(adsk.core.Point3D.create(2.4, 1.4, 0), pillar_hole_d)

            if wallSketch.profiles.count > 0:
                # BUG FIX: Välj profil med störst area (rektangel-med-hål) istället för sista profilen
                max_area = -1
                max_prof = None
                for i in range(wallSketch.profiles.count):
                    prof = wallSketch.profiles.item(i)
                    area = prof.areaProperties().area
                    if area > max_area:
                        max_area = area
                        max_prof = prof

                wallProf = adsk.core.ObjectCollection.create()
                if max_prof:
                    wallProf.add(max_prof)
                    wallInput = extrudes.createInput(wallProf, adsk.fusion.FeatureOperations.JoinFeatureOperation)
                    wallInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(wall_t))
                    extrudes.add(wallInput)

            # Gussets för sensorvägg
            cos_a = math.cos(rad)
            sin_a = math.sin(rad)
            perp_cos = math.cos(rad + math.pi/2)
            perp_sin = math.sin(rad + math.pi/2)

            gussetSketch = newComp.sketches.add(upperTopPlane)
            sl = gussetSketch.sketchCurves.sketchLines
            g = gusset_size

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

        # Sensorpositioner (anpassade for 13 cm djup)
        add_wall_with_gussets_upper("FC", p_w/2, p_h - 0.5, 90)
        add_wall_with_gussets_upper("FL", 2.5, p_h - 1.5, 135)
        add_wall_with_gussets_upper("FR", p_w - 2.5, p_h - 1.5, 45)
        add_wall_with_gussets_upper("BL", 2.5, 1.5, 225)
        add_wall_with_gussets_upper("BR", p_w - 2.5, 1.5, 315)

        # === STEG U5: PIN-TEXT VID SENSORER ===
        ui.messageBox("CHECKPOINT 6: 5 sensorer klara")
        upperTxtSketch = newComp.sketches.add(upperTopPlane)

        def upperLabel(t, tx, ty):
            txtInput = upperTxtSketch.sketchTexts.createInput(t, 0.4, adsk.core.Point3D.create(tx, ty, 0))
            upperTxtSketch.sketchTexts.add(txtInput)

        upperLabel("v8.1", 1.0, 0.5)
        upperLabel("T22/E23", p_w/2, p_h - 2.0)
        upperLabel("T24/E25", 1.0, p_h - 2.0)
        upperLabel("T26/E27", p_w - 1.0, p_h - 2.0)
        upperLabel("T28/E29", 1.0, 2.0)
        upperLabel("T30/E31", p_w - 1.0, 2.0)

        design.computeAll()
        upperTProfs = adsk.core.ObjectCollection.create()
        for p in upperTxtSketch.profiles:
            upperTProfs.add(p)

        if upperTProfs.count > 0:
            uTInput = extrudes.createInput(upperTProfs, adsk.fusion.FeatureOperations.CutFeatureOperation)
            uTInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(-0.08))
            extrudes.add(uTInput)

        # === STEG P: PILLAR (1 cylinder, anvandaren printar 4x) ===
        ui.messageBox("CHECKPOINT 7: Pin-text klar, startar pelare")
        pillarSketch = newComp.sketches.add(xy)
        pillar_x = -5.0  # vid sidan av plattorna
        pillar_y = 0.0
        pillarSketch.sketchCurves.sketchCircles.addByCenterRadius(
            adsk.core.Point3D.create(pillar_x, pillar_y, 0), pillar_d/2)

        pillarProfs = adsk.core.ObjectCollection.create()
        for p in pillarSketch.profiles:
            pillarProfs.add(p)
        pInputCyl = extrudes.createInput(pillarProfs, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        pInputCyl.setDistanceExtent(False, adsk.core.ValueInput.createByReal(pillar_h))
        pillarExtrude = extrudes.add(pInputCyl)
        pillarBody = pillarExtrude.bodies.item(0)
        try:
            pillarBody.name = "Pillar"
        except:
            pass

        # Pillar M3-hal
        pillarHoleSketch = newComp.sketches.add(xy)
        pillarHoleSketch.sketchCurves.sketchCircles.addByCenterRadius(
            adsk.core.Point3D.create(pillar_x, pillar_y, 0), pillar_hole_d/2)
        phProfs = adsk.core.ObjectCollection.create()
        for p in pillarHoleSketch.profiles:
            phProfs.add(p)
        if phProfs.count > 0:
            phInput = extrudes.createInput(phProfs, adsk.fusion.FeatureOperations.CutFeatureOperation)
            phInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(pillar_h * 1.2))
            extrudes.add(phInput)

        design.computeAll()
        ui.messageBox("Nexus Carrier v8.1 ALLT KLART!\n\n"
                      "- Lower_Floor 18x13 cm (Mega + L298N + breadboard-zon)\n"
                      "- Upper_Floor 18x13 cm (mobil + 5 sensorer + tilt)\n"
                      "- Pillar Ø10x40 mm (printa 4x)\n"
                      "- Mobilhallare nu 10 cm bred + 4 gussets\n"
                      "- Sensorvaggar fixade (max-area profile)\n"
                      "- Stackning: Lower z=0, Upper z=4.4 cm")

    except:
        err = 'Fel i Nexus Carrier v8.1:\n' + traceback.format_exc()
        try:
            print(err)  # till Text Commands-panelen
        except:
            pass
        if ui:
            ui.messageBox(err)
        else:
            # ui ar None - skriptet dog innan ui sattes. Anvand global adsk
            # (inte lokal import - det skadar resten av funktionen via Python scoping)
            try:
                _app = adsk.core.Application.get()
                if _app and _app.userInterface:
                    _app.userInterface.messageBox('FEL (ui var None):\n' + err)
            except:
                pass
