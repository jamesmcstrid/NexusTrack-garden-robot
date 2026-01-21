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

        extrudes = newComp.features.extrudeFeatures

        # --- PARAMETRAR (cm) ---
        p_w, p_h, p_t = 22.0, 17.0, 0.4          # Basplatta: 22x17 cm, 4mm tjock
        wall_h, wall_t = 2.8, 0.4                # Sensorvägg: 2.8 cm hög, 4mm tjock
        half_wall_w = 2.6                        # Halva väggbredden
        gusset_size = 0.8                        # Triangulär förstärkning
        phone_gap, phone_h = 1.4, 4.0            # Mobilhållare

        xy = newComp.xYConstructionPlane

        # ============================================
        # STEG 1: BASPLATTA
        # ============================================
        baseSketch = newComp.sketches.add(xy)
        baseSketch.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, 0, 0),
            adsk.core.Point3D.create(p_w, p_h, 0))

        if baseSketch.profiles.count == 0:
            ui.messageBox("Ingen profil för basplatta.")
            return

        baseProf = adsk.core.ObjectCollection.create()
        baseProf.add(baseSketch.profiles.item(0))
        baseInput = extrudes.createInput(baseProf, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        baseInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(p_t))
        baseExtrude = extrudes.add(baseInput)
        baseBody = baseExtrude.bodies.item(0)

        # Hitta toppytan (z = p_t)
        topFace = None
        for face in baseBody.faces:
            if face.geometry.surfaceType == adsk.core.SurfaceTypes.PlaneSurfaceType:
                normal = face.geometry.normal
                if abs(normal.z) > 0.9 and face.geometry.origin.z > 0.1:
                    topFace = face
                    break

        if not topFace:
            ui.messageBox("Kunde inte hitta toppytan.")
            return

        # ============================================
        # STEG 2: BORRA MONTERINGSHÅL
        # ============================================
        holeSketch = newComp.sketches.add(topFace)

        # Arduino Mega hål
        for x, y in [(2, 1.5), (2, 11.66), (7.08, 1.5), (7.08, 11.15)]:
            holeSketch.sketchCurves.sketchCircles.addByCenterRadius(
                adsk.core.Point3D.create(x, y, 0), 0.17)

        # L298N hål
        lx = 15.0
        for x, y in [(lx, 4.5), (lx+3.7, 4.5), (lx, 8.2), (lx+3.7, 8.2)]:
            holeSketch.sketchCurves.sketchCircles.addByCenterRadius(
                adsk.core.Point3D.create(x, y, 0), 0.17)

        if holeSketch.profiles.count > 0:
            holeProfs = adsk.core.ObjectCollection.create()
            for p in holeSketch.profiles:
                holeProfs.add(p)
            holeInput = extrudes.createInput(holeProfs, adsk.fusion.FeatureOperations.CutFeatureOperation)
            holeInput.participantBodies = [baseBody]
            holeInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(p_t + 0.1))
            extrudes.add(holeInput)

        # ============================================
        # STEG 3: MOBILHÅLLARE
        # ============================================
        # Uppdatera topFace referens
        topFace = None
        for face in baseBody.faces:
            if face.geometry.surfaceType == adsk.core.SurfaceTypes.PlaneSurfaceType:
                normal = face.geometry.normal
                if abs(normal.z) > 0.9 and face.geometry.origin.z > 0.1:
                    topFace = face
                    break

        if topFace:
            mountSketch = newComp.sketches.add(topFace)
            mx, my = p_w / 2, 13.0
            mw = 10.0
            # Två väggar för mobilhållaren
            mountSketch.sketchCurves.sketchLines.addTwoPointRectangle(
                adsk.core.Point3D.create(mx - mw/2, my, 0),
                adsk.core.Point3D.create(mx + mw/2, my + 0.4, 0))
            mountSketch.sketchCurves.sketchLines.addTwoPointRectangle(
                adsk.core.Point3D.create(mx - mw/2, my + 0.4 + phone_gap, 0),
                adsk.core.Point3D.create(mx + mw/2, my + 0.8 + phone_gap, 0))

            if mountSketch.profiles.count > 0:
                mProfs = adsk.core.ObjectCollection.create()
                for p in mountSketch.profiles:
                    mProfs.add(p)
                mInput = extrudes.createInput(mProfs, adsk.fusion.FeatureOperations.JoinFeatureOperation)
                mInput.participantBodies = [baseBody]
                mInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(phone_h))
                extrudes.add(mInput)

        # ============================================
        # STEG 4: SENSORVÄGGAR MED GUSSETS
        # ============================================
        def create_sensor_wall(name, cx, cy, angle_deg):
            """
            Skapar en sensorvägg med förstärkande triangulära gussets.
            cx, cy = centrum för väggen på basplattan
            angle_deg = riktning väggen pekar (90 = framåt/+Y)
            """
            rad = math.radians(angle_deg)

            # Uppdatera topFace referens
            currentTopFace = None
            for face in baseBody.faces:
                if face.geometry.surfaceType == adsk.core.SurfaceTypes.PlaneSurfaceType:
                    normal = face.geometry.normal
                    if abs(normal.z) > 0.9 and face.geometry.origin.z > 0.1:
                        currentTopFace = face
                        break

            if not currentTopFace:
                return

            # Skapa skiss på toppytan för vägg + gussets
            wallSketch = newComp.sketches.add(currentTopFace)
            lines = wallSketch.sketchCurves.sketchLines

            # Beräkna riktningsvektorer
            cos_a = math.cos(rad)
            sin_a = math.sin(rad)
            # Vinkelrätt mot väggriktningen (för väggbredd)
            perp_cos = math.cos(rad + math.pi/2)
            perp_sin = math.sin(rad + math.pi/2)

            # Vägg-rektangel (footprint på basplattan)
            # Väggen är wall_t tjock i riktningen den pekar
            # och 2*half_wall_w bred vinkelrätt
            w1 = adsk.core.Point3D.create(
                cx + perp_cos * (-half_wall_w) + cos_a * (-wall_t/2),
                cy + perp_sin * (-half_wall_w) + sin_a * (-wall_t/2), 0)
            w2 = adsk.core.Point3D.create(
                cx + perp_cos * (half_wall_w) + cos_a * (-wall_t/2),
                cy + perp_sin * (half_wall_w) + sin_a * (-wall_t/2), 0)
            w3 = adsk.core.Point3D.create(
                cx + perp_cos * (half_wall_w) + cos_a * (wall_t/2),
                cy + perp_sin * (half_wall_w) + sin_a * (wall_t/2), 0)
            w4 = adsk.core.Point3D.create(
                cx + perp_cos * (-half_wall_w) + cos_a * (wall_t/2),
                cy + perp_sin * (-half_wall_w) + sin_a * (wall_t/2), 0)

            lines.addByTwoPoints(w1, w2)
            lines.addByTwoPoints(w2, w3)
            lines.addByTwoPoints(w3, w4)
            lines.addByTwoPoints(w4, w1)

            # GUSSET VÄNSTER - triangel vid vänstra kanten
            g = gusset_size
            gl_base = adsk.core.Point3D.create(
                cx + perp_cos * (-half_wall_w + 0.3) + cos_a * (-wall_t/2),
                cy + perp_sin * (-half_wall_w + 0.3) + sin_a * (-wall_t/2), 0)
            gl_back = adsk.core.Point3D.create(
                cx + perp_cos * (-half_wall_w + 0.3) + cos_a * (-wall_t/2 - g),
                cy + perp_sin * (-half_wall_w + 0.3) + sin_a * (-wall_t/2 - g), 0)
            gl_side = adsk.core.Point3D.create(
                cx + perp_cos * (-half_wall_w - g * 0.5) + cos_a * (-wall_t/2 - g),
                cy + perp_sin * (-half_wall_w - g * 0.5) + sin_a * (-wall_t/2 - g), 0)

            lines.addByTwoPoints(gl_base, gl_back)
            lines.addByTwoPoints(gl_back, gl_side)
            lines.addByTwoPoints(gl_side, gl_base)

            # GUSSET HÖGER - triangel vid högra kanten
            gr_base = adsk.core.Point3D.create(
                cx + perp_cos * (half_wall_w - 0.3) + cos_a * (-wall_t/2),
                cy + perp_sin * (half_wall_w - 0.3) + sin_a * (-wall_t/2), 0)
            gr_back = adsk.core.Point3D.create(
                cx + perp_cos * (half_wall_w - 0.3) + cos_a * (-wall_t/2 - g),
                cy + perp_sin * (half_wall_w - 0.3) + sin_a * (-wall_t/2 - g), 0)
            gr_side = adsk.core.Point3D.create(
                cx + perp_cos * (half_wall_w + g * 0.5) + cos_a * (-wall_t/2 - g),
                cy + perp_sin * (half_wall_w + g * 0.5) + sin_a * (-wall_t/2 - g), 0)

            lines.addByTwoPoints(gr_base, gr_back)
            lines.addByTwoPoints(gr_back, gr_side)
            lines.addByTwoPoints(gr_side, gr_base)

            # Extrudera alla profiler (vägg + gussets)
            if wallSketch.profiles.count > 0:
                wallProfs = adsk.core.ObjectCollection.create()
                for i in range(wallSketch.profiles.count):
                    wallProfs.add(wallSketch.profiles.item(i))

                wallInput = extrudes.createInput(wallProfs, adsk.fusion.FeatureOperations.JoinFeatureOperation)
                wallInput.participantBodies = [baseBody]
                wallInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(wall_h))
                extrudes.add(wallInput)

            # Skapa hål för ultraljudssensorn i en separat skiss
            # Hitta väggytorna och borra hål
            # (Förenklar: skippar sensorhålen för nu, kan läggas till senare)

        # Skapa alla 5 sensorväggar
        create_sensor_wall("FC", p_w/2, p_h - 0.5, 90)       # Front Center
        create_sensor_wall("FL", 2.5, p_h - 1.5, 135)        # Front Left
        create_sensor_wall("FR", p_w - 2.5, p_h - 1.5, 45)   # Front Right
        create_sensor_wall("BL", 2.5, 1.5, 225)              # Back Left
        create_sensor_wall("BR", p_w - 2.5, 1.5, 315)        # Back Right

        # ============================================
        # STEG 5: GRAVYR (VALFRITT)
        # ============================================
        # Skippar gravyr för att undvika komplexitet
        # Kan läggas till manuellt i Fusion 360

        ui.messageBox('Nexus Carrier v6 REINFORCED klar!\n\n' +
                      '- Basplatta 22x17 cm\n' +
                      '- 8 monteringshål (Arduino + L298N)\n' +
                      '- Mobilhållare\n' +
                      '- 5 sensorväggar med gussets\n\n' +
                      'OBS: Sensorhål i väggarna måste borras manuellt.')

    except:
        if ui:
            ui.messageBox('Fel: ' + traceback.format_exc())
