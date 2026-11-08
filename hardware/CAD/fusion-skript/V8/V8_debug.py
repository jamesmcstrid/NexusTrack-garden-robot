import adsk.core, adsk.fusion, traceback

def run(context):
    """Minimalt sanity-test. Skapar en 5x5x5 cm kub och visar MessageBox."""
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        ui.messageBox("DEBUG STEG 1: Skriptet startar!")

        design = app.activeProduct
        if not design:
            ui.messageBox("DEBUG: app.activeProduct ar None!\nOppna eller skapa ett designdokument forst.")
            return
        ui.messageBox("DEBUG STEG 2: Design hittad")

        root = design.rootComponent
        ui.messageBox("DEBUG STEG 3: rootComponent OK, namn = " + str(root.name))

        # Forsok skapa subkomponent (faller tillbaka till root vid Part Design)
        try:
            occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
            comp = occ.component
            comp.name = "DebugTest"
            ui.messageBox("DEBUG STEG 4a: SubComponent skapad (Assembly-dokument)")
        except RuntimeError as e:
            comp = root
            ui.messageBox("DEBUG STEG 4b: Foll tillbaka till root (Part Design)\nFel: " + str(e))

        # Skapa enkel skiss + kub
        xy = comp.xYConstructionPlane
        sk = comp.sketches.add(xy)
        sk.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, 0, 0),
            adsk.core.Point3D.create(5, 5, 0))
        ui.messageBox("DEBUG STEG 5: Skiss klar, antal profiler: " + str(sk.profiles.count))

        if sk.profiles.count == 0:
            ui.messageBox("DEBUG: Inga profiler i skissen!")
            return

        prof = adsk.core.ObjectCollection.create()
        prof.add(sk.profiles.item(0))
        inp = comp.features.extrudeFeatures.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        inp.setDistanceExtent(False, adsk.core.ValueInput.createByReal(5))
        comp.features.extrudeFeatures.add(inp)
        ui.messageBox("DEBUG KLAR: 5x5x5 cm kub skapad! Allt funkar!")

    except:
        err = "FEL i debug-skript:\n" + traceback.format_exc()
        print(err)
        if ui:
            ui.messageBox(err)
