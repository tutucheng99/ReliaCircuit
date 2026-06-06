from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_claim_evidence_matrix as claims


def test_claim_matrix_has_expected_core_claims() -> None:
    matrix = claims.build_claim_matrix(ROOT)

    assert matrix.shape[0] == 26
    assert {
        "C1_FDR_SYNTHETIC",
        "REAL_SUBJECT_VERB",
        "REAL_FDR_DECOY",
        "REAL_LAYER_SCAN",
        "REAL_BIASINBIOS",
        "REVIEWER_QF_SENSITIVITY",
        "REVIEWER_PVALUE_ROBUSTNESS",
        "REVIEWER_ADAPTIVE_KNOCKOFF",
        "REVIEWER_MULTISPLIT",
        "REVIEWER_DECOY_ROBUSTNESS",
        "REVIEWER_TYPE_SM",
        "SECOND_DECOY_BH_BY",
        "SECOND_GAMMA_SENSITIVITY",
        "SECOND_REAL_CI_WIDTHS",
        "SECOND_REAL_TYPE_S_DIAGNOSTIC",
        "SECOND_COVARIATE_EBH",
        "SECOND_CLUSTER_PERMUTATION",
    } <= set(matrix["claim_id"])


def test_real_gpu_claims_reflect_completed_subject_verb_and_bounded_bias_probe() -> None:
    matrix = claims.build_claim_matrix(ROOT).set_index("claim_id")

    assert matrix.loc["REAL_SUBJECT_VERB", "status"] == "supported_real"
    assert matrix.loc["REAL_SUBJECT_VERB", "missing_evidence"] == ""
    assert matrix.loc["REAL_FDR_DECOY", "status"] == "supported_real_reliability"
    assert "selects 0" in matrix.loc["REAL_FDR_DECOY", "metrics"]
    assert matrix.loc["REAL_LAYER_SCAN", "status"] in {"missing_real_layer_scan", "supported_real_layer_scan"}
    if matrix.loc["REAL_LAYER_SCAN", "status"] == "missing_real_layer_scan":
        assert "subject_verb_agreement_balanced_l08" in matrix.loc["REAL_LAYER_SCAN", "missing_evidence"]
    assert matrix.loc["REAL_BIASINBIOS", "status"] == "bounded_real_negative"
    assert "e-BH selected no features" in matrix.loc["REAL_BIASINBIOS", "claim"]


def test_synthetic_fdr_claim_is_supported_locally() -> None:
    matrix = claims.build_claim_matrix(ROOT).set_index("claim_id")

    row = matrix.loc["C1_FDR_SYNTHETIC"]
    assert row["status"] == "supported_local"
    assert "e_bh_pcal fdp_mean=0.0013" in row["metrics"]


def test_write_markdown_includes_status_counts(tmp_path: Path) -> None:
    matrix = claims.build_claim_matrix(ROOT)
    report = tmp_path / "claim_evidence_matrix.md"

    claims.write_markdown(report, matrix)

    text = report.read_text(encoding="utf-8")
    assert "# Claim Evidence Matrix" in text
    assert "bounded_real_negative" in text
