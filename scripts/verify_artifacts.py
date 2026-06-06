from __future__ import annotations

import argparse
import re
import sys
import zlib
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
MAX_GITHUB_FILE_BYTES = 100 * 1024 * 1024
TEXT_SUFFIXES = {
    ".bib",
    ".cfg",
    ".csv",
    ".json",
    ".md",
    ".py",
    ".sh",
    ".svg",
    ".tex",
    ".toml",
    ".txt",
    ".yml",
    ".yaml",
}
SKIP_DIRS = {".git", ".pytest_cache", ".pytest_tmp_public", ".pytest_tmp_run2", ".test_tmp", "__pycache__"}


REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "CITATION.cff",
    ".gitignore",
    ".env.example",
    "pyproject.toml",
    "setup.py",
    "requirements-cpu.txt",
    "requirements-gpu.txt",
    "runpod_job.sh",
    "configs/subject_verb_layer_scan_protocol.json",
    "configs/synthetic_gate_b.json",
    "configs/synthetic_frontier.json",
    "configs/synthetic_ci_frontier.json",
    "configs/synthetic_debias.json",
    "src/reliacircuit/fdr.py",
    "src/reliacircuit/inference.py",
    "src/reliacircuit/cache_analysis.py",
    "scripts/run_synthetic_gate_b.py",
    "scripts/run_synthetic_frontier.py",
    "scripts/run_synthetic_debias.py",
    "scripts/analyze_ablation_cache.py",
    "scripts/analyze_real_subject_verb_reliability.py",
    "scripts/run_reviewer_empirical_gaps.py",
    "scripts/run_second_round_reviewer_analyses.py",
    "scripts/build_paper_assets.py",
    "scripts/build_claim_evidence_matrix.py",
    "scripts/draw_reliacircuit_final_figures.py",
    "scripts/produce_sae_screen_scores.py",
    "scripts/produce_sae_ablation_cache.py",
    "scripts/produce_sae_circuit_cache.py",
    "scripts/run_gpu_postprocessing.py",
    "scripts/verify_artifacts.py",
    "docs/reproducibility.md",
    "docs/artifact_map.md",
    "docs/gpu_cache_generation.md",
    "docs/cache_schema.md",
    "docs/method_spec.md",
    "docs/statistical_claims.md",
    "paper/reliacircuit.tex",
    "paper/figures/fig1_old_vs_reliacircuit_final.pdf",
    "paper/figures/fig2_method_flow_final.pdf",
    "paper/figures/fig3_decoy_layers_final.pdf",
    "results/paper_assets/claim_evidence_matrix.csv",
    "results/paper_assets/table_1_gate_b_fdr_ci.csv",
    "results/paper_assets/table_8_bounded_bias_probe.csv",
    "results/paper_assets/table_9_real_decoy_reliability.csv",
    "results/paper_assets/table_7_real_subject_verb.csv",
    "results/paper_assets/table_10_real_selection_stability.csv",
    "results/paper_assets/table_11_real_q_grid.csv",
    "results/paper_assets/table_14_reviewer_method_comparison.csv",
    "results/paper_assets/table_16_reviewer_decoy_robustness.csv",
    "results/subject_verb_agreement_balanced/exact_ablation_cache.csv",
    "results/subject_verb_agreement_balanced_l08/exact_ablation_cache.csv",
    "results/subject_verb_agreement_balanced_l12/exact_ablation_cache.csv",
    "results/subject_verb_agreement_balanced_l16/exact_ablation_cache.csv",
]


FORBIDDEN_PATHS = [
    "data/bias_in_bios/bias_in_bios_normalized.csv",
    "data/bias_in_bios/train.csv",
    "data/bias_in_bios/dev.csv",
    "data/bias_in_bios/test.csv",
    "data/bias_in_bios/prompts.csv",
    "data/bias_in_bios/paired_prompts.csv",
    "data/bias_in_bios/pair_ablation_manifest.csv",
    "data/bias_in_bios_viewer_probe",
    "results/hf_access_probe",
    "results/hf_access_probe_retry",
    "results/" + "runpod_" + "background",
    "results/" + "runpod_" + "ssh",
    "results/" + "runpod_" + "ssh_returned",
    "results/" + "runpod_" + "ingest_smoke",
    "results/" + "runpod_" + "authorization",
    "results/submission_package",
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify the anonymous public ReliaCircuit release.")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    failures: list[str] = []
    failures.extend(check_required_files(root))
    failures.extend(check_forbidden_paths(root))
    failures.extend(check_file_sizes(root))
    failures.extend(check_table_shapes(root))
    failures.extend(scan_sensitive_text(root))
    failures.extend(scan_binary_metadata(root))
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        raise SystemExit(1)
    print("public artifact verification passed")


def check_required_files(root: Path) -> list[str]:
    return [f"missing required file: {rel}" for rel in REQUIRED_FILES if not (root / rel).is_file()]


def check_forbidden_paths(root: Path) -> list[str]:
    failures: list[str] = []
    for rel in FORBIDDEN_PATHS:
        if (root / rel).exists():
            failures.append(f"forbidden public-release path exists: {rel}")
    return failures


def check_file_sizes(root: Path) -> list[str]:
    failures: list[str] = []
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if path.is_file() and path.stat().st_size > MAX_GITHUB_FILE_BYTES:
            failures.append(f"file exceeds GitHub ordinary file limit: {path.relative_to(root).as_posix()}")
    return failures


def check_table_shapes(root: Path) -> list[str]:
    expected_rows = {
        "results/subject_verb_agreement_balanced/exact_ablation_cache.csv": 77824,
        "results/subject_verb_agreement_balanced_l08/exact_ablation_cache.csv": 77824,
        "results/subject_verb_agreement_balanced_l12/exact_ablation_cache.csv": 77824,
        "results/subject_verb_agreement_balanced_l16/exact_ablation_cache.csv": 77824,
    }
    failures: list[str] = []
    for rel, rows in expected_rows.items():
        path = root / rel
        if not path.is_file():
            continue
        frame = pd.read_csv(path)
        if frame.shape[0] != rows:
            failures.append(f"{rel} has {frame.shape[0]} rows, expected {rows}")

    gate = pd.read_csv(root / "results" / "paper_assets" / "table_1_gate_b_fdr_ci.csv")
    method_col = "Method" if "Method" in gate.columns else "method"
    fdp_col = "FDP" if "FDP" in gate.columns else "fdp_mean"
    ebh = gate[gate[method_col].astype(str).str.contains("e_bh", regex=False)]
    if ebh.empty:
        failures.append("table_1_gate_b_fdr_ci.csv has no e-BH row")
    elif float(ebh.iloc[0][fdp_col]) > 0.01:
        failures.append("e-BH FDP in table_1_gate_b_fdr_ci.csv is unexpectedly high")
    p_lt_q = gate[gate[method_col].astype(str).eq("p_lt_q")]
    if p_lt_q.empty or float(p_lt_q.iloc[0][fdp_col]) < 0.20:
        failures.append("synthetic p<q FDP check did not reproduce the expected failure mode")
    top_score = gate[gate[method_col].astype(str).str.contains("top_score", regex=False)]
    if top_score.empty or float(top_score.iloc[0][fdp_col]) < 0.40:
        failures.append("synthetic top-score FDP check did not reproduce the expected failure mode")

    bias = pd.read_csv(root / "results" / "paper_assets" / "table_8_bounded_bias_probe.csv")
    if "e_bh_pcal" not in set(bias["method"].astype(str)):
        failures.append("bounded BiasInBios table is missing e_bh_pcal")

    decoy = pd.read_csv(root / "results" / "paper_assets" / "table_9_real_decoy_reliability.csv")
    if set(decoy["layer"].astype(str)) != {"L8", "L12", "L16", "L20"}:
        failures.append("real decoy reliability table does not cover the four fixed layers")
    decoy_ebh = decoy[decoy["method"].astype(str).eq("e_bh_pcal")]
    if decoy_ebh.empty:
        failures.append("real decoy reliability table is missing e_bh_pcal")
    elif float(decoy_ebh["known_null_decoys_selected_mean"].max()) != 0.0:
        failures.append("real e-BH decoy table no longer has zero selected decoys")

    layer_scan = pd.read_csv(root / "results" / "paper_assets" / "table_7_real_subject_verb.csv")
    layer_ebh = layer_scan[layer_scan["method"].astype(str).eq("e_bh_pcal")]
    if set(layer_ebh["layer"].astype(str)) != {"L8", "L12", "L16", "L20"}:
        failures.append("layer-scan table does not cover all fixed e-BH layers")
    if float(layer_ebh[layer_ebh["layer"].eq("L16")]["discoveries"].iloc[0]) < 20:
        failures.append("layer-scan table no longer localizes the larger L16 e-BH circuit")

    q_grid = pd.read_csv(root / "results" / "paper_assets" / "table_11_real_q_grid.csv")
    q_ebh = q_grid[(q_grid["method"].astype(str).eq("e_bh_pcal")) & (q_grid["estimand"].astype(str).eq("mean_effect"))]
    if set(q_ebh["layer"].astype(str)) != {"L8", "L12", "L16", "L20"}:
        failures.append("real q-grid table is missing e-BH layers")
    if not {0.01, 0.05, 0.10, 0.20, 0.30}.issubset(set(q_ebh["q"].round(2))):
        failures.append("real q-grid table is missing expected q values")

    stability = pd.read_csv(root / "results" / "paper_assets" / "table_10_real_selection_stability.csv")
    stab_ebh = stability[
        (stability["method"].astype(str).eq("e_bh_pcal"))
        & (stability["estimand"].astype(str).eq("mean_effect"))
    ]
    if set(stab_ebh["layer"].astype(str)) != {"L8", "L12", "L16", "L20"}:
        failures.append("selection-stability table is missing e-BH layers")
    if float(stab_ebh["jaccard_mean"].min()) < 0.60:
        failures.append("selection-stability table no longer matches the expected e-BH stability range")

    robust = pd.read_csv(root / "results" / "paper_assets" / "table_16_reviewer_decoy_robustness.csv")
    expected_decoy_schemes = {
        "centered_permutation",
        "high_score_signflip",
        "low_score_signflip",
        "random_score_signflip",
    }
    if not expected_decoy_schemes.issubset(set(robust["decoy_scheme"].astype(str))):
        failures.append("reviewer decoy-robustness table is missing expected decoy schemes")
    robust_ebh = robust[robust["method"].astype(str).eq("e_bh_pcal")]
    if robust_ebh.empty or float(robust_ebh["known_null_fdp_mean"].max()) > 0.001:
        failures.append("reviewer decoy-robustness e-BH FDP check failed")
    elif set(robust_ebh["layer"].astype(str)) != {"L8", "L12", "L16", "L20"}:
        failures.append("reviewer decoy-robustness e-BH rows are missing layers")
    elif not expected_decoy_schemes.issubset(set(robust_ebh["decoy_scheme"].astype(str))):
        failures.append("reviewer decoy-robustness e-BH rows are missing decoy schemes")

    methods = pd.read_csv(root / "results" / "paper_assets" / "table_14_reviewer_method_comparison.csv")
    method_names = set(methods["method"].astype(str))
    if "paired_knockoff_plus" not in method_names:
        failures.append("reviewer method-comparison table is missing paired_knockoff_plus")
    method_ebh = methods[methods["method"].astype(str).eq("e_bh_pcal")]
    if set(method_ebh["layer"].astype(str)) != {"L8", "L12", "L16", "L20"}:
        failures.append("reviewer method-comparison e-BH rows are missing fixed layers")
    if not set(method_ebh["selection_rule"].astype(str)).issubset({"e_bh_p_calibrated"}):
        failures.append("reviewer method-comparison e-BH rows have an unexpected selection rule")
    return failures


def scan_sensitive_text(root: Path) -> list[str]:
    patterns = sensitive_patterns()
    failures: list[str] = []
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        rel = path.relative_to(root).as_posix()
        if rel == "scripts/verify_artifacts.py":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for label, pattern in patterns.items():
            match = pattern.search(text)
            if match:
                failures.append(f"{label} in {rel}: {shorten(match.group(0))}")
    return failures


def scan_binary_metadata(root: Path) -> list[str]:
    """Scan printable metadata in binary figures without treating compressed pixels as text."""
    patterns = sensitive_patterns()
    failures: list[str] = []
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        suffix = path.suffix.lower()
        if suffix == ".png":
            chunks = png_text_chunks(path)
        elif suffix == ".pdf":
            chunks = pdf_metadata_strings(path)
        else:
            continue
        for chunk in chunks:
            for label, pattern in patterns.items():
                match = pattern.search(chunk)
                if match:
                    failures.append(f"{label} in binary metadata {rel}: {shorten(match.group(0))}")
    return failures


def sensitive_patterns() -> dict[str, re.Pattern[str]]:
    return {
        "email address": re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"),
        "HF token": re.compile(r"hf_[A-Za-z0-9_=\-]{20,}"),
        "OpenSSH key block": re.compile(r"BEGIN " + r"(OPENSSH|RSA|DSA|EC) " + r"PRIVATE " + r"KEY"),
        "local Windows user path": re.compile(r"C:" + re.escape("\\") + r"Users" + re.escape("\\"), re.IGNORECASE),
        "known local username": re.compile("tu" + "tu9", re.IGNORECASE),
        "institution marker": re.compile("George" + r"\s+" + "Washington|" + "G" + "WU", re.IGNORECASE),
        "RunPod public host": re.compile(r"[a-z0-9\-]+\." + r"runpod\.(net|io)", re.IGNORECASE),
        "IPv4 address": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
        "returned pod staging path": re.compile("runpod_" + r"(ssh_returned|background|ingest|authorization)", re.IGNORECASE),
    }


def png_text_chunks(path: Path) -> list[str]:
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        return []
    chunks: list[str] = []
    pos = 8
    while pos + 12 <= len(data):
        length = int.from_bytes(data[pos : pos + 4], "big")
        chunk_type = data[pos + 4 : pos + 8]
        start = pos + 8
        end = start + length
        if end + 4 > len(data):
            break
        payload = data[start:end]
        if chunk_type == b"tEXt":
            chunks.append(payload.decode("latin-1", errors="ignore"))
        elif chunk_type == b"iTXt":
            chunks.append(payload.decode("utf-8", errors="ignore"))
        elif chunk_type == b"zTXt":
            try:
                keyword, compressed = payload.split(b"\x00", 1)
                if compressed:
                    compressed = compressed[1:]
                text = keyword + b"\x00" + zlib.decompress(compressed)
                chunks.append(text.decode("latin-1", errors="ignore"))
            except (ValueError, zlib.error):
                chunks.append(payload.decode("latin-1", errors="ignore"))
        pos = end + 4
    return chunks


def pdf_metadata_strings(path: Path) -> list[str]:
    text = path.read_bytes().decode("latin-1", errors="ignore")
    chunks = [
        match.group(0)
        for match in re.finditer(r"/(?:Author|Creator|Producer|Title|Subject)\s*\((?:\\.|[^)])*\)", text)
    ]
    chunks.extend(match.group(0) for match in re.finditer(r"<x:xmpmeta[\s\S]*?</x:xmpmeta>", text))
    return chunks


def shorten(value: str, limit: int = 80) -> str:
    value = value.replace("\n", " ")
    return value if len(value) <= limit else value[:limit] + "..."


if __name__ == "__main__":
    main()
