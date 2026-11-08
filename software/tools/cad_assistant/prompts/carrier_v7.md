# NexusTrack Carrier v7 — Lyftbar modul (prototyp för RC-bil → bandrobot)

## Roll
Du är en expertingenjör inom Fusion 360 Python API (adsk.core, adsk.fusion).
Du genererar **körklara** Python-skript som direkt kan köras via "Scripts and Add-Ins" i Fusion 360.

## Kontext
Detta är en autonom robotplattform (NexusTrack). Carriern är en 3D-printad
bottenplatta som bär all elektronik och som ska kunna **lyftas i ett stycke**
mellan en RC-bil (prototypfasen) och en framtida bandvagn (Husqvarna 410-modul).

Buntband (4 mm breda) träds genom långsmala slots i plattan och vidare genom
hål i RC-bilens tak/kåpa. Detta gör modulen verktygsfritt portabel.

## Komponenter på plattan (med koordinatsystem från v6)
- Arduino Mega 2560:        96.52 × 50.8 mm, 4 hörnhål Ø3.4 mm
- L298N motorstyrning:      37 × 37 mm hålbild, 4 hål Ø3.4 mm
- OnePlus 8T (mobilhållare): 75 × 165 mm × 9 mm tjocklek, lutas Mobil_Vinkel framåt
- 5× HC-SR04 ultraljud:     45 × 20 mm modul, 2 öppningar Ø16.5 mm per sensor
  - FC = Front Center        (rakt fram)
  - FL = Front Left  +45°
  - FR = Front Right -45°
  - BL = Back  Left  +135°
  - BR = Back  Right -135°

## Krav på v7 (jämfört med v6_reinforced)
1. **Behåll** v6:s grundlogik (skapa ny komponent, basplatta-skiss-extrudera, hitta toppyta, borra hål, extrudera väggar med JoinFeatureOperation).
2. **Lägg till buntbandsslots**: 6 par av 4.5 × 12 mm slots, placerade symmetriskt i 4 hörn + 2 mittpunkter (fram/bak) på plattan. Slottarna ska gå rakt igenom plattan (CutFeatureOperation).
3. **Lyfthandtag**: extrudera 2 × cylindrar Ø8 mm × 15 mm höga, en på vardera kortsida av plattan, så modulen kan lyftas med pekfingrarna.
4. **Sensor-väggarna är 45°/135°-vridna** (samma som v6) men ska ha **gusset-förstärkning** kvar för stadga.
5. **Inga kåpor / lock** — öppen platta för felsökning.
6. **Pin-referens-text**: ingravera (CutFeature 0.8 mm djup) "T22/E23" vid FC, "T24/E25" vid FL, etc., så kabeldragning är självförklarande.

## PLA-toleranser (viktigt — prototyp printas i PLA)
Eftersom första utskriften är PLA på en FDM-printer (typ Bambu/Prusa/Ender med 0.4 mm nozzle):
- **M3-hål**: borra Ø3.6 mm (inte 3.4) — PLA krymper ~0.2 mm radiellt och hål blir tighta.
- **Sensor-öppningar HC-SR04**: Ø16.8 mm (inte 16.5) — sensorerna ska kunna tryckas i utan att spricka.
- **Buntbandsslots**: 4.8 × 12.5 mm (inte 4.5 × 12) — buntbandshuvudet ska passera.
- **Väggjocklek minimum**: 1.6 mm (= 4 perimeter walls á 0.4 mm) för bärande väggar.
- **Plattans tjocklek**: höj till 4 mm (från parameters.txt 3 mm) för PLA — PLA är sprödare än PETG och 3 mm flexar för mycket.
- Lägg till en **kommentar längst upp i skriptet** som listar alla justerade toleranser, så det är lätt att se diffen mot v6 och justera tillbaka för PETG senare.

## Parametrar (importeras från parameters.txt — använd dessa exakta namn)
- `p_w` = Platta_Bredd / 10  (cm i Fusion)
- `p_h` = Platta_Langd / 10
- `p_t` = Platta_Tjocklek / 10
- `mega_x` = Mega_X / 10
- `mega_y` = Mega_Y / 10
- `mobil_vinkel` = Mobil_Vinkel  (grader)
- `sensor_d` = Sensor_Oga_D / 10

## Output-format (mycket viktigt!)
- **Endast Python-kod**, inget förklarande prosa, ingen markdown-kodfence.
- Filen ska börja med `import adsk.core, adsk.fusion, traceback, math` och definiera `def run(context):`.
- All geometri ska skapas i en **ny komponent** (`root.occurrences.addNewComponent`).
- Använd **try/except** med ui.messageBox för felmeddelanden så Fusion inte tystkraschar.
- Använd `ObjectCollection.create()` för att samla profiler innan extrudering — undvik den `bSet`-bugg som plågade v3-v5.

## Återanvänd bevisat fungerande mönster från v6
{{V6_SCRIPT}}

## Generera nu hela `Nexus_Carrier_v7.py`:
