# 3D-print-guide: Carrier v7 prototyp (PLA)

Snabbguide för att printa Carrier v7 i PLA på en standard FDM-printer (Bambu, Prusa, Ender, etc. med 0.4 mm nozzle).

PLA är valt för **prototypfasen** eftersom det är billigt, lätt att skriva ut och lätt att modifiera (slipa, borra, limma). När v7 är validerad och vi går vidare till bandroboten skrivs den om i PETG eller ASA för UV-/värmetålighet.

## Filfödelse

```
software/tools/cad_assistant/  →  python3 cad_assistant.py carrier_v7
hardware/CAD/Nexus_Carrier_carrier_v7_latest.py   ← genererat av AI
        ↓ (öppna i Fusion 360 → Scripts → Run)
hardware/CAD/exports/Nexus_Carrier_v7.stl         ← du exporterar manuellt
        ↓ (importera i slicern)
hardware/CAD/exports/Nexus_Carrier_v7.gcode       ← till SD/USB → printer
```

## Slicer-inställningar (Cura / PrusaSlicer / OrcaSlicer)

| Parameter | Värde | Varför |
|---|---|---|
| Material | PLA (vanligt, inte silk eller wood-fill) | Stadga + dimensionsstabilitet |
| Nozzle | 0.4 mm | Standard, klarar 1.6 mm väggar i 4 perimetrar |
| Lagerhöjd | 0.2 mm | Bra balans mellan kvalitet och tid |
| Toppskal | 5 lager | Sensor-text och plana ytor blir snygga |
| Bottenskal | 4 lager | Tål skruvarnas brickor utan att deformeras |
| Perimetrar | 4 (= 1.6 mm väggjocklek) | Räcker för vibration från motorerna |
| Infill | 25 % gyroid | Gyroid är starkast i flera riktningar — bra mot vridmoment |
| Print-temp | 210 °C (hotend) / 60 °C (bädd) | Standard PLA |
| Print-hastighet | 60 mm/s, perimetrar 40 mm/s | Snyggare hörn vid sensor-väggarna |
| Cooling | 100 % från lager 3 | Skarpare overhangs på buntbandsslots |
| Brim | 5 mm | Bara om plattan studsar — testa utan först |

## Orientering på print-plattan

**Lägg plattan platt**, baksidan ned (där det inte finns gravyr/text).

- Sensor-väggarna pekar uppåt → printas med tree supports (Cura "Tree" eller PrusaSlicer "Organic")
- Lyfthandtagen pekar uppåt → cylindrarna behöver supports under "taket"
- Buntbandsslottarna är hål **rakt igenom** plattan → inga supports behövs
- Pin-referens-text är ingraverad i toppytan → sliceras automatiskt korrekt

Tree supports är **viktiga** eftersom standard-supports lämnar fula ärr på sensor-väggarnas insida och du kan inte komma åt att slipa där sensorn ska sitta.

## Material-tips

- Använd PLA från en **känd tillverkare** (Prusament, Polymaker, Bambu) — billigt PLA varierar i diameter och ger porösa väggar.
- Färg: matt grå eller svart är lättast att se sprickor på. Undvik silk/glossy för bärande prints.
- En rulle räcker minst 5–8 iterationer av v7 (~80 g per print).

## Estimerad printtid

På en Bambu X1C / Prusa MK4 med ovan settings: **5–7 timmar** för hela plattan inklusive sensor-väggar och handtag. Räkna med 8 h på en Ender 3 utan input shaping.

## Efterbehandling

1. **Snitta supports** med kniv. Tree supports lossnar ofta för hand.
2. **Trimma sensor-öppningarna** (Ø16.8 mm) med en rundfil tills HC-SR04-modulen passar utan att spricka — slicern överextruderar ofta första lagret.
3. **Provmontera** Mega + L298N med M3-skruvar **innan** du fäster mobilen — skruvas hålen kärva borrar du upp dem till Ø3.8 mm med en handborr.
4. **Buntbandstest**: trä igenom ett 4 mm buntband i en av slottarna och dra åt. Om det knäcker plattan → höj `Platta_Tjocklek` i parameters.txt och printa om.

## Felsökningstabell

| Symptom | Trolig orsak | Åtgärd |
|---|---|---|
| Sensor-väggarna spricker längs lagret | För få perimetrar / för svalt | Öka till 5 perimetrar, höj temp till 215 °C |
| Mega-hålen är för små för M3 | PLA-krympning | Borra upp till Ø3.8 mm med handborr |
| Plattan flexar när monterad | För låg infill / för tunn platta | Höj infill till 35 %, tjocklek till 5 mm |
| Buntbandet skär in i kanten | Slot för nära kant | Iterera prompten: `--extra "flytta slots 5 mm in från kant"` |
| Lyfthandtagen lossnar | Dålig vidhäftning mellan lager | Höj print-temp 5 °C, sänk fan från lager 3-5 |

## När prototypen är klar

Markera vad som behövde efter-bearbetas (slippa, borra, lima om) och berätta för CAD-assistenten:

```bash
python3 cad_assistant.py carrier_v7 --extra "Sensor-öppningarna behövde slipas — gör dem Ø17.0 mm. Mobilhållarens spår var 0.3 mm för smalt."
```

Då lär sig nästa iteration av PLA-erfarenheten utan att du behöver redigera Fusion-skriptet manuellt.
