# NexusTrack CAD Assistant

AI-driven CAD-iteration mot lokal Ollama-instans (192.168.0.92:11434).
Tar parameters.txt + förra versionen av carrier-skriptet som baseline och låter
LLM:en föreslå en ny version utifrån en strukturerad prompt-mall.

## Förutsättningar

På AI-noden:
```bash
ollama serve   # alternativt: systemctl start ollama
ollama pull qwen2.5-coder:14b
# Tillgängliggör mot LAN (om inte redan gjort):
#   sudo systemctl edit ollama
#   [Service]
#   Environment="OLLAMA_HOST=0.0.0.0:11434"
#   sudo systemctl restart ollama
```

I WSL/Win11 hos dig:
```bash
# Inga pip-beroenden - använder bara Pythons stdlib.
python3 --version   # 3.10+
```

## Användning

### 1. Verifiera att Ollama svarar och se vilka modeller du har
```bash
cd ~/Robotgräsklippare/NexusTrack-garden-robot/software/tools/cad_assistant
chmod +x probe_ollama.sh
./probe_ollama.sh
```

### 2. Generera Carrier v7
```bash
python3 cad_assistant.py carrier_v7
# eller med explicit modell:
python3 cad_assistant.py carrier_v7 --model qwen2.5-coder:14b
```

Skriptet streamar LLM:ens svar live i terminalen och sparar resultatet i:
```
hardware/CAD/Nexus_Carrier_carrier_v7_<TIMESTAMP>.py
hardware/CAD/Nexus_Carrier_carrier_v7_latest.py   (symlink/kopia)
```

### 3. Öppna i Fusion 360
1. Utilities → Add-Ins → Scripts → "+"
2. Peka ut `Nexus_Carrier_carrier_v7_latest.py`
3. Run. Felmeddelanden visas i MessageBox.

### 4. Iterera
Något fel? Kör om med extra-instruktion:
```bash
python3 cad_assistant.py carrier_v7 --extra "Buntbandsslottarna är för nära kanten - flytta in dem 5 mm"
```

## Filstruktur

```
software/tools/cad_assistant/
├── README.md              # Det här dokumentet
├── probe_ollama.sh        # Diagnos: pingar Ollama + listar modeller
├── cad_assistant.py       # Huvudskript - prompt → Python-skript
└── prompts/
    └── carrier_v7.md      # Prompt-mall för v7
```

Lägg till nya mallar i `prompts/<namn>.md` och kör med `python3 cad_assistant.py <namn>`.

## Felsökning

| Fel | Trolig orsak | Åtgärd |
|---|---|---|
| `Kunde inte nå Ollama` | OLLAMA_HOST=127.0.0.1 i service | Sätt `OLLAMA_HOST=0.0.0.0:11434` |
| `model not found` | Modellen är inte pullad på noden | `ollama pull <modell>` på noden |
| `bSet`-fel i Fusion | Klassisk profil-buggen | Lägg till `--extra "Använd ObjectCollection.create() för alla profiler"` |
| Python-kod kompilerar inte | För liten modell | Byt till `qwen2.5-coder:14b` eller större |

## Miljövariabler

| Variabel | Default | Beskrivning |
|---|---|---|
| `OLLAMA_HOST` | `http://192.168.0.92:11434` | Ollama-endpoint |
| `NEXUS_CAD_MODEL` | `qwen2.5-coder:14b` | Standardmodell |
