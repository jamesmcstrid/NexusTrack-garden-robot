import adsk.core, adsk.fusion, traceback, math

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = app.activeProduct
        root = design.rootComponent
        
        # 1. NY KOMPONENT
        newOcc = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        newComp = newOcc.component
        newComp.name = "Nexus_Carrier_v6_Reinforced"

        # VIKTIGT: Använd komponentens egna extrude-features
        extrudes = newComp.features.extrudeFeatures

        # --- PARAMETRAR (cm) ---
        p_w, p_h, p_t = 22.0, 17.0, 0.4          # Basplatta
        wall_h, wall_w, wall_t = 2.8, 5.2, 0.4  # Sensorvägg
        gusset_size = 0.8                        # Förstärkning
        gusset_height = 1.6                      # 60% av wall_h
        phone_gap, phone_h = 1.4, 4.0           # Mobilhållare
        xy = newComp.xYConstructionPlane

        # --- STEG 1: SKAPA BASPLATTAN ---
        baseSketch = newComp.sketches.add(xy)
        baseSketch.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, 0, 0),
            adsk.core.Point3D.create(p_w, p_h, 0))

        # Hämta första profilen direkt (rektangeln skapar alltid en profil)
        if baseSketch.profiles.count == 0:
            ui.messageBox("Ingen profil hittades. Försök igen.")
            return

        baseProfCollection = adsk.core.ObjectCollection.create()
        baseProfCollection.add(baseSketch.profiles.item(0))

        baseInput = extrudes.createInput(baseProfCollection, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        baseInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(p_t))
        baseExtrude = extrudes.add(baseInput)
        baseBody = baseExtrude.bodies.item(0)

        # Hitta toppytan
        topFace = None
        for face in baseBody.faces:
            if face.geometry.surfaceType == adsk.core.SurfaceTypes.PlaneSurfaceType and face.geometry.origin.z > 0.1:
                topFace = face
                break

        # --- STEG 2: BORRA HÅL (BAKRE DELEN) ---
        holeSketch = newComp.sketches.add(topFace)
        # Arduino Mega (Bak)
        for x, y in [(2,1.5), (2,11.66), (7.08,1.5), (7.08,11.15)]:
            holeSketch.sketchCurves.sketchCircles.addByCenterRadius(adsk.core.Point3D.create(x, y, 0), 0.17)
        # L298N (Bak)
        lx = 15.0
        for x, y in [(lx, 4.5), (lx+3.7, 4.5), (lx, 8.2), (lx+3.7, 8.2)]:
            holeSketch.sketchCurves.sketchCircles.addByCenterRadius(adsk.core.Point3D.create(x, y, 0), 0.17)

        # Utför borrning
        holeProfs = adsk.core.ObjectCollection.create()
        for p in holeSketch.profiles: holeProfs.add(p)
        if holeProfs.count > 0:
            extrudes.add(extrudes.createInput(holeProfs, adsk.fusion.FeatureOperations.CutFeatureOperation)).setDistanceExtent(False, adsk.core.ValueInput.createByReal(-1.0))

        # --- STEG 3: MOBILHÅLLARE (KORRIDOREN) ---
        # Placeras mellan elektronik (max y=11.66) och frontsensorer (y=16)
        mountSketch = newComp.sketches.add(topFace)
        mx, my = p_w/2, 13.0
        mw = 10.0
        mountSketch.sketchCurves.sketchLines.addTwoPointRectangle(adsk.core.Point3D.create(mx-mw/2, my, 0), adsk.core.Point3D.create(mx+mw/2, my+0.4, 0))
        mountSketch.sketchCurves.sketchLines.addTwoPointRectangle(adsk.core.Point3D.create(mx-mw/2, my+0.4+phone_gap, 0), adsk.core.Point3D.create(mx+mw/2, my+0.8+phone_gap, 0))
        
        mProfs = adsk.core.ObjectCollection.create()
        for p in mountSketch.profiles: mProfs.add(p)
        mInput = extrudes.createInput(mProfs, adsk.fusion.FeatureOperations.JoinFeatureOperation)
        mInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(phone_h))
        extrudes.add(mInput)

        # --- STEG 4: SENSORVÄGGAR MED TRIANGULÄRA GUSSETS ---
        def add_wall_with_gussets(name, x, y, angle_deg):
            """Skapar sensorvägg med förstärkande gussets på båda sidor."""
            rad = math.radians(angle_deg)
            half_w = wall_w / 2  # 2.6 cm

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
            sc.addByCenterRadius(adsk.core.Point3D.create(-1.3, 1.4, 0), 0.825)  # Vänster ultraljudsrör
            sc.addByCenterRadius(adsk.core.Point3D.create(1.3, 1.4, 0), 0.825)   # Höger ultraljudsrör
            sc.addByCenterRadius(adsk.core.Point3D.create(-2.4, 1.4, 0), 0.17)   # Vänster skruv
            sc.addByCenterRadius(adsk.core.Point3D.create(2.4, 1.4, 0), 0.17)    # Höger skruv

            # Extrudera väggen (sista profilen = rektangel minus hål)
            if wallSketch.profiles.count > 0:
                wallProf = adsk.core.ObjectCollection.create()
                wallProf.add(wallSketch.profiles.item(wallSketch.profiles.count - 1))
                wallInput = extrudes.createInput(wallProf, adsk.fusion.FeatureOperations.JoinFeatureOperation)
                wallInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(wall_t))
                extrudes.add(wallInput)

            # --- TRIANGULÄRA GUSSETS ---
            # Beräkna riktningsvektorer
            cos_a = math.cos(rad)
            sin_a = math.sin(rad)
            perp_cos = math.cos(rad + math.pi/2)  # Vinkelrätt mot väggriktningen
            perp_sin = math.sin(rad + math.pi/2)

            gussetSketch = newComp.sketches.add(xy)
            sl = gussetSketch.sketchCurves.sketchLines
            g = gusset_size

            # VÄNSTER GUSSET - triangel vid vänstra kanten av väggen
            lx1 = x + perp_cos * (-half_w + 0.2)  # Lite innanför kanten
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

            # HÖGER GUSSET - triangel vid högra kanten av väggen
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
                    # Endast små triangulära profiler
                    if prof.areaProperties().area < 1.0:
                        gProfs.add(prof)

                if gProfs.count > 0:
                    gInput = extrudes.createInput(gProfs, adsk.fusion.FeatureOperations.JoinFeatureOperation)
                    gInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(gusset_height))
                    extrudes.add(gInput)

        # Skapa alla 5 sensorväggar med förstärkningar
        add_wall_with_gussets("FC", p_w/2, p_h-0.5, 90)       # Front Center - rakt fram
        add_wall_with_gussets("FL", 2.5, p_h-1.5, 135)        # Front Left - 45° vänster
        add_wall_with_gussets("FR", p_w-2.5, p_h-1.5, 45)     # Front Right - 45° höger
        add_wall_with_gussets("BL", 2.5, 1.5, 225)            # Back Left
        add_wall_with_gussets("BR", p_w-2.5, 1.5, 315)        # Back Right

        # --- STEG 5: GRAVYR ---
        txtSketch = newComp.sketches.add(topFace)
        def label(t, tx, ty):
            txtInput = txtSketch.sketchTexts.createInput(t, 0.4, adsk.core.Point3D.create(tx, ty, 0))
            txtSketch.sketchTexts.add(txtInput)

        label("ARDUINO MEGA", 4.5, 5.0)
        label("L298N DRIVER", lx+1.85, 6.5)
        label("FC", p_w/2, p_h-2.5)
        label("CAMERA SLOT", p_w/2, 14.2)
        label("v6-REINFORCED", 1.0, 0.5)

        design.computeAll()
        tProfs = adsk.core.ObjectCollection.create()
        for p in txtSketch.profiles:
            tProfs.add(p)

        if tProfs.count > 0:
            tInput = extrudes.createInput(tProfs, adsk.fusion.FeatureOperations.CutFeatureOperation)
            tInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(-0.05))
            extrudes.add(tInput)

        ui.messageBox('Nexus Carrier v6 REINFORCED klar!\n\n5 sensorväggar med triangulära gussets.')
    except:
        if ui: ui.messageBox('Fel: ' + traceback.format_exc())