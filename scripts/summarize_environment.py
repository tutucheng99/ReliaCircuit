from __future__ import annotations

import argparse
import importlib.metadata
import json
import platform
import re
import sys
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
REQ_SPLIT_RE = re.compile(r"\s*(?:[<>=!~]=?|;|\[)")


def main() -> None:
    args = parse_args()
    requirement_map = collect_requirements(args.requirements)
    summary = build_environment_summary(requirement_map)
    platform_info = collect_platform_info()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(args.output, index=False)
    args.platform_json.write_text(json.dumps(platform_info, indent=2), encoding="utf-8")
    write_report(args.report, summary, platform_info)
    print(f"wrote {summary.shape[0]} environment rows to {safe_display_path(args.output)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize local Python/platform dependency state.")
    parser.add_argument(
        "--requirements",
        type=Path,
        nargs="*",
        default=[ROOT / "requirements-cpu.txt", ROOT / "requirements-gpu.txt"],
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "results" / "paper_assets" / "environment_summary.csv",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=ROOT / "results" / "paper_assets" / "environment_summary.md",
    )
    parser.add_argument(
        "--platform-json",
        type=Path,
        default=ROOT / "results" / "paper_assets" / "environment_platform.json",
    )
    return parser.parse_args()


def collect_requirements(paths: list[Path]) -> dict[str, dict[str, str]]:
    requirements: dict[str, dict[str, str]] = {}
    for path in paths:
        resolved = path if path.is_absolute() else ROOT / path
        label = resolved.stem.replace("requirements-", "")
        if not resolved.exists():
            continue
        for raw_line in resolved.read_text(encoding="utf-8").splitlines():
            parsed = parse_requirement_line(raw_line)
            if parsed is None:
                continue
            name, spec = parsed
            requirements.setdefault(name, {})[f"{label}_spec"] = spec
    return requirements


def parse_requirement_line(line: str) -> tuple[str, str] | None:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None
    name = REQ_SPLIT_RE.split(stripped, maxsplit=1)[0].strip()
    if not name:
        return None
    return canonical_dist_name(name), stripped


def canonical_dist_name(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def build_environment_summary(requirement_map: dict[str, dict[str, str]]) -> pd.DataFrame:
    rows = []
    for name in sorted(requirement_map):
        installed = installed_version(name)
        row = {
            "package": name,
            "installed_version": installed,
            "installed": installed != "",
            "cpu_spec": requirement_map[name].get("cpu_spec", ""),
            "gpu_spec": requirement_map[name].get("gpu_spec", ""),
        }
        rows.append(row)
    return pd.DataFrame(rows)


def installed_version(name: str) -> str:
    candidates = [name, name.replace("-", "_")]
    for candidate in candidates:
        try:
            return importlib.metadata.version(candidate)
        except importlib.metadata.PackageNotFoundError:
            continue
    return ""


def collect_platform_info() -> dict[str, Any]:
    return {
        "python_version": sys.version,
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "implementation": platform.python_implementation(),
    }


def write_report(path: Path, summary: pd.DataFrame, platform_info: dict[str, Any]) -> None:
    missing = summary[~summary["installed"].astype(bool)] if not summary.empty else pd.DataFrame()
    lines = [
        "# Environment Summary",
        "",
        "This file records the local environment used for artifact generation and",
        "verification. GPU pod environments should be recorded separately by",
        "`scripts/gpu_smoke_test.py` and `scripts/summarize_run_metadata.py`.",
        "",
        "## Platform",
        "",
        f"- Python: `{platform_info['python_version'].split()[0]}`",
        f"- Executable: `{platform_info['python_executable']}`",
        f"- Platform: `{platform_info['platform']}`",
        f"- Machine: `{platform_info['machine']}`",
        "",
        "## Packages",
        "",
        summary.to_markdown(index=False) if not summary.empty else "No requirements found.",
        "",
        "## Missing Locally",
        "",
    ]
    if missing.empty:
        lines.append("All listed requirement distributions are installed locally.")
    else:
        lines.append(missing[["package", "cpu_spec", "gpu_spec"]].to_markdown(index=False))
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def safe_display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    main()
