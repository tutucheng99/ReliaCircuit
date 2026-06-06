from __future__ import annotations

import os
from pathlib import Path


DEFAULT_ENV_FILE = Path.home() / ".reliacircuit_runpod.env"
SECRET_MARKERS = ("TOKEN", "KEY", "SECRET", "PASSWORD")


def load_env_file(path: Path | None = DEFAULT_ENV_FILE, *, override: bool = False) -> dict[str, str]:
    if path is None:
        return {}
    path = path.expanduser()
    if not path.exists():
        return {}
    loaded: dict[str, str] = {}
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            raise SystemExit(f"invalid env file line {line_number}: expected KEY=VALUE")
        key, value = line.split("=", 1)
        key = key.strip()
        value = strip_quotes(value.strip())
        if not key:
            raise SystemExit(f"invalid env file line {line_number}: empty key")
        if override or key not in os.environ:
            os.environ[key] = value
        loaded[key] = value
    return loaded


def strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def env_status(keys: list[str]) -> dict[str, str]:
    return {key: "set" if os.environ.get(key) else "missing" for key in keys}


def redacted_loaded_env(loaded: dict[str, str]) -> dict[str, str]:
    return {key: "<redacted>" if is_secret_key(key) else value for key, value in loaded.items()}


def is_secret_key(key: str) -> bool:
    upper = key.upper()
    return any(marker in upper for marker in SECRET_MARKERS)
