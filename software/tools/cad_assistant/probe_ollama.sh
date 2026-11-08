#!/usr/bin/env bash
# Probe the local Ollama AI node and list available models.
# Usage:  ./probe_ollama.sh   (uses default 192.168.0.92:11434)
#         OLLAMA_HOST=http://10.0.0.5:11434 ./probe_ollama.sh
set -euo pipefail

OLLAMA_HOST="${OLLAMA_HOST:-http://192.168.0.92:11434}"

echo "=== Pingar Ollama på ${OLLAMA_HOST} ==="
if ! curl -fsS --max-time 5 "${OLLAMA_HOST}/api/tags" >/tmp/ollama_tags.json; then
  echo "FEL: Kunde inte nå ${OLLAMA_HOST}/api/tags"
  echo "Tips:"
  echo "  - Är Ollama-tjänsten igång på noden?  (systemctl status ollama)"
  echo "  - Lyssnar den på alla interfaces?     (OLLAMA_HOST=0.0.0.0 i service-fil)"
  echo "  - Brandvägg på noden?                 (sudo ufw allow 11434)"
  exit 1
fi

echo ""
echo "=== Tillgängliga modeller ==="
python3 -c "
import json, sys
data = json.load(open('/tmp/ollama_tags.json'))
models = data.get('models', [])
if not models:
    print('Inga modeller installerade. Kör t.ex. \"ollama pull qwen2.5-coder:14b\" på noden.')
    sys.exit(0)
print(f'{\"NAMN\":<40} {\"PARAM\":<10} {\"STORLEK\":<10} {\"FAMILJ\":<15}')
print('-' * 80)
for m in models:
    name = m.get('name', '?')
    det = m.get('details', {})
    params = det.get('parameter_size', '?')
    fam = det.get('family', '?')
    size_gb = m.get('size', 0) / (1024**3)
    print(f'{name:<40} {params:<10} {size_gb:>6.1f} GB   {fam:<15}')
"

echo ""
echo "=== Rekommenderad för CAD-script (Python/Fusion 360 API) ==="
echo "Bäst:    qwen2.5-coder:14b eller större  (om du har 16+ GB VRAM)"
echo "OK:      deepseek-coder-v2:16b, codellama:13b"
echo "Snabbt:  qwen2.5-coder:7b  (klarar enklare iterationer)"
echo ""
echo "Sätt vald modell i environment:"
echo "  export NEXUS_CAD_MODEL=qwen2.5-coder:14b"
