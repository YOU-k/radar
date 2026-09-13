from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
LOCAL_ENV_FILE = Path("/data3/yy/key.env")


def load_sources() -> dict:
    with open(ROOT / "config" / "sources.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_profile() -> str:
    return (ROOT / "config" / "profile.md").read_text(encoding="utf-8")


def load_local_env(path: Path = LOCAL_ENV_FILE) -> None:
    """把本机 key.env 里的 KEY=VALUE 注入环境（已存在的变量不覆盖）。
    文件内容只进环境变量，不打印、不写入任何产物。"""
    import os

    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip("'\"")
        if k and v:
            os.environ.setdefault(k, v)


def llm_api_key() -> str | None:
    import os

    return os.environ.get("LLM_API_KEY") or os.environ.get("DEEPSEEK_API_KEY")
