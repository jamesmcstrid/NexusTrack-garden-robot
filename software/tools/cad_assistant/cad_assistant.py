#!/usr/bin/env python3
"""
NexusTrack CAD Assistant — pratar med lokal Ollama-instans och iterar fram
Fusion 360 Python-skript för carrier-plattor och tillbehör.

Workflow:
    1. Läser parameters.txt + v6-skriptet som baseline.
    2. Hämtar prompt-mall från prompts/<target>.md.
    3. Skickar till Ollama via /api/chat (streamar svar live i terminalen).
    4. Sparar resultatet som hardware/CAD/Nexus_Carrier_<target>_<timestamp>.py.
    5. Visar diff mot baseline + erbjuder att uppdatera "latest" symlink.

Användning:
    python cad_assistant.py carrier_v7
    python cad_assistant.py carrier_v7 --model qwen2.5-coder:14b
    python cad_assistant.py carrier_v7 --extra "lägg till mast-fäste längst fram"
"""
from __future__ import annotations
import argparse
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

# --- Sökvägar (relativt repo-roten) ---
REPO_ROOT = Path(__file__).resolve().parents[3]
PARAMS_FILE = REPO_ROOT / "hardware" / "CAD" / "fusion360" / "parameters.txt"
V6_SCRIPT = REPO_ROOT / "hardware" / "CAD" / "Nexus_Carrier_v6_reinforced.py"
CAD_OUT_DIR = REPO_ROOT / "hardware" / "CAD"
PROMPT_DIR = Path(__file__).resolve().parent / "prompts"

DEFAULT_HOST = os.environ.get("OLLAMA_HOST", "http://192.168.0.92:11434")
DEFAULT_MODEL = os.environ.get("NEXUS_CAD_MODEL", "qwen2.5-coder:7b")


def load_baseline() -> tuple[str, str]:
    """Returnerar (parameters.txt, v6-skriptet) som strängar."""
    if not PARAMS_FILE.exists():
        sys.exit(f"FEL: Saknar {PARAMS_FILE}")
    if not V6_SCRIPT.exists():
        sys.exit(f"FEL: Saknar {V6_SCRIPT}")
    return PARAMS_FILE.read_text(encoding="utf-8"), V6_SCRIPT.read_text(encoding="utf-8")


def build_prompt(target: str, extra: str | None) -> tuple[str, str]:
    """Returnerar (system_prompt, user_prompt) för Ollama-chat."""
    template_path = PROMPT_DIR / f"{target}.md"
    if not template_path.exists():
        sys.exit(f"FEL: Hittar inte prompt-mall {template_path}")
    template = template_path.read_text(encoding="utf-8")
    params, v6 = load_baseline()

    user_msg = template.replace("{{V6_SCRIPT}}", f"```python\n{v6}\n```")
    user_msg += f"\n\n## Parametrar (parameters.txt)\n```\n{params}\n```"
    if extra:
        user_msg += f"\n\n## Extra-instruktioner från användaren\n{extra}"

    sys_msg = (
        "Du är en expert på Fusion 360 Python API. "
        "Du svarar med ENBART körklar Python-kod, ingen markdown, ingen prosa. "
        "Var noggrann med ObjectCollection-mönstret för att undvika bSet-buggen."
    )
    return sys_msg, user_msg


def stream_ollama(host: str, model: str, system: str, user: str) -> str:
    """Streamar svar från Ollama /api/chat och returnerar hela texten."""
    url = f"{host.rstrip('/')}/api/chat"
    payload = {
        "model": model,
        "stream": True,
        "options": {"temperature": 0.2, "num_ctx": 16384},
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    out = []
    print(f"\n--- Streamar från {model} på {host} ---\n")
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            for line in resp:
                if not line.strip():
                    continue
                try:
                    chunk = json.loads(line)
                except json.JSONDecodeError:
                    continue
                msg = chunk.get("message", {}).get("content", "")
                if msg:
                    sys.stdout.write(msg)
                    sys.stdout.flush()
                    out.append(msg)
                if chunk.get("done"):
                    break
    except urllib.error.URLError as e:
        sys.exit(f"\nFEL: Kunde inte nå Ollama på {url}: {e}")
    print("\n--- Klart ---\n")
    return "".join(out)


def extract_python(text: str) -> str:
    """Plockar ut Python-koden ur LLM-svaret. Hanterar både markdown-fence och rå kod."""
    # Försök med ```python ... ```
    m = re.search(r"```python\s*\n(.*?)```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    # Fallback: ``` ... ```
    m = re.search(r"```\s*\n(.*?)```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    # Annars: returnera allt från första 'import adsk' till EOF
    idx = text.find("import adsk")
    if idx >= 0:
        return text[idx:].strip()
    return text.strip()


def save_script(target: str, code: str) -> Path:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"Nexus_Carrier_{target}_{ts}.py"
    path = CAD_OUT_DIR / fname
    path.write_text(code, encoding="utf-8")
    # Symlänka "latest"
    latest = CAD_OUT_DIR / f"Nexus_Carrier_{target}_latest.py"
    try:
        if latest.exists() or latest.is_symlink():
            latest.unlink()
        latest.symlink_to(fname)  # relativ link
    except OSError:
        # Windows utan admin-rättigheter -> kopiera istället
        latest.write_text(code, encoding="utf-8")
    return path


def main() -> None:
    ap = argparse.ArgumentParser(description="NexusTrack CAD Assistant")
    ap.add_argument("target", help="Prompt-mall i prompts/<target>.md (t.ex. carrier_v7)")
    ap.add_argument("--model", default=DEFAULT_MODEL, help=f"Ollama-modell (default: {DEFAULT_MODEL})")
    ap.add_argument("--host", default=DEFAULT_HOST, help=f"Ollama-host (default: {DEFAULT_HOST})")
    ap.add_argument("--extra", default=None, help="Extra-instruktion på fri text")
    ap.add_argument("--dry-run", action="store_true", help="Visa prompt utan att skicka")
    args = ap.parse_args()

    sys_msg, user_msg = build_prompt(args.target, args.extra)
    if args.dry_run:
        print("=== SYSTEM ===")
        print(sys_msg)
        print("\n=== USER ===")
        print(user_msg)
        return

    raw = stream_ollama(args.host, args.model, sys_msg, user_msg)
    code = extract_python(raw)
    path = save_script(args.target, code)
    print(f"\n✅ Sparat: {path}")
    print(f"   Latest:  {CAD_OUT_DIR / f'Nexus_Carrier_{args.target}_latest.py'}")
    print(f"\nNästa steg:")
    print(f"   1. Öppna Fusion 360 → Utilities → Add-Ins → Scripts → +")
    print(f"   2. Peka ut: {path}")
    print(f"   3. Tryck Run. Felmeddelanden hamnar i en MessageBox.")
    print(f"   4. Itererar du? Kör skriptet igen med --extra \"...beskriv ändring...\"")


if __name__ == "__main__":
    main()
