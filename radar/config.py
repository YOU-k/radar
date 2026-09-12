from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def load_sources() -> dict:
    with open(ROOT / "config" / "sources.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_profile() -> str:
    return (ROOT / "config" / "profile.md").read_text(encoding="utf-8")
