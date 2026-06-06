from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


CLAIMS = [
    {
        "claim_id": "C1_METHOD",
        "paper_section": "Method",
        "claim": "ReliaCircuit defines split screen-then-test sparse circuit mining with resample-ablation effects, FDR control, and post-selection confidence intervals.",
        "claim_scope_now": "Can be stated as method design and implementation.",
        "evidence": ["docs/method_spec.md", "docs/statistical_claims.md", "src/reliacircuit/pipeline.py", "src/reliacircuit/fdr.py"],
        "missing_for_full_claim": "",
        "status_if_present": "supported",
    },
    {
        "claim_id": "C1_FDR_SYNTHETIC",
        "paper_section": "Synthetic Gate B",
        "claim": "On the known-circuit benchmark, e-BH controls FDP at q=0.1 while uncorrected p-value and top-score baselines do not.",
        "claim_scope_now": "Can be stated for the current synthetic benchmark.",
        "evidence": ["results/paper_assets/table_1_gate_b_fdr_ci.md", "results/synthetic_gate_b/aggregate_metrics.csv"],
        "metrics": "e_bh_pcal fdp_mean=0.0013; p_lt_q fdp_mean=0.2885; top_score_k_active fdp_mean=0.4771",
        "missing_for_full_claim": "Real Gemma/Gemma Scope subject-verb evidence is reported separately under REAL_SUBJECT_VERB; do not use the synthetic FDP benchmark as real-model evidence.",
        "status_if_present": "supported_local",
    },
    {
        "claim_id": "C1_CI_SYNTHETIC",
        "paper_section": "Synthetic Gate B",
        "claim": "Selection-free split-B inference gives calibrated bootstrap confidence intervals in the known-circuit setting.",
        "claim_scope_now": "Can be stated for finite-ATE synthetic evaluation.",
        "evidence": ["results/paper_assets/table_1_gate_b_fdr_ci.md", "results/paper_assets/table_5_ci_frontier.md"],
        "metrics": "screened CI coverage near 0.95 across current runs",
        "missing_for_full_claim": "Real SAE feature-effect CIs are reported for discovered features, but CI calibration is only validated in the synthetic known-circuit setting.",
        "status_if_present": "supported_local",
    },
    {
        "claim_id": "C1_ROBUSTNESS",
        "paper_section": "Synthetic Robustness",
        "claim": "The synthetic frontier records where dependence, weak effects, narrow screens, and nuisance features affect power and false discoveries.",
        "claim_scope_now": "Can be stated as a measured robustness frontier, not a universal theorem.",
        "evidence": ["results/paper_assets/table_3_synthetic_frontier.md", "results/paper_assets/figure_3_synthetic_frontier_fdp_power.png"],
        "missing_for_full_claim": "Larger seed counts can tighten error bars if time allows.",
        "status_if_present": "supported_local",
    },
    {
        "claim_id": "CIRCUIT_SYNTHETIC",
        "paper_section": "Circuit Evaluation",
        "claim": "FDR-selected synthetic circuits preserve more held-out known-circuit behavior than top-score thresholding.",
        "claim_scope_now": "Can be stated for the synthetic held-out circuit evaluation.",
        "evidence": ["results/paper_assets/table_4_circuit_metrics.md", "results/synthetic_gate_b/circuit_aggregate_metrics.csv"],
        "metrics": "e_bh_pcal completeness_r2_mean=0.7874 vs top_score_k_active=0.5428",
        "missing_for_full_claim": "Real subject-verb circuit evidence is reported separately under REAL_SUBJECT_VERB; do not mix synthetic and real circuit metrics.",
        "status_if_present": "supported_local",
    },
    {
        "claim_id": "C2_DEBIAS_SYNTHETIC",
        "paper_section": "Downstream Debiasing",
        "claim": "In the synthetic SHIFT-style benchmark, FDR-controlled removal improves worst-group accuracy with controlled erroneous removal.",
        "claim_scope_now": "Can be stated for the synthetic downstream debiasing benchmark.",
        "evidence": ["results/paper_assets/table_6_downstream_debias.md", "results/synthetic_debias/aggregate_eval.csv"],
        "metrics": "baseline worst_group_acc=0.6199; e_bh_pcal=0.9999; erroneous_removal_rate=0.0000",
        "missing_for_full_claim": "The bounded real BiasInBios probe is negative, so a positive real debiasing claim is not made.",
        "status_if_present": "supported_local",
    },
    {
        "claim_id": "BIASINBIOS_PREP",
        "paper_section": "Real Data Preparation",
        "claim": "BiasInBios schema, prompt construction, gender-pair screening setup, and bounded live dataset/GPU probe are implemented.",
        "claim_scope_now": "Can be stated as real-data preparation plus bounded Gemma/Gemma Scope probe readiness.",
        "evidence": ["docs/bias_in_bios_workflow.md", "results/bias_in_bios_viewer_probe/viewer_probe_report.md", "data/bias_in_bios_viewer_probe/prompts.csv"],
        "missing_for_full_claim": "Full-dataset BiasInBios remains future work; current evidence is a bounded 60-row real probe.",
        "status_if_present": "prepared",
    },
    {
        "claim_id": "REAL_SUBJECT_VERB",
        "paper_section": "Real LLM Evaluation",
        "claim": "ReliaCircuit yields controlled real Gemma/Gemma Scope subject-verb discoveries and held-out joint-circuit metrics on balanced prompts across a fixed four-layer protocol.",
        "claim_scope_now": "Can be stated for the fixed balanced subject-verb protocol at Gemma Scope layers 8, 12, 16, and 20. Report uncentered completeness together with centered R2 and selected/full correlation.",
        "evidence": [
            "results/gpu_smoke/full_gemma_scope.json",
            "data/subject_verb_agreement_balanced/prompts.csv",
            "results/subject_verb_agreement_balanced_l08/exact_ablation_cache.csv",
            "results/subject_verb_agreement_balanced_l08/method_reliability_tracking_comparison.csv",
            "results/subject_verb_agreement_balanced/exact_ablation_cache.csv",
            "results/subject_verb_agreement_balanced/method_reliability_tracking_comparison.csv",
            "results/subject_verb_agreement_balanced_l12/exact_ablation_cache.csv",
            "results/subject_verb_agreement_balanced_l12/method_reliability_tracking_comparison.csv",
            "results/subject_verb_agreement_balanced_l16/exact_ablation_cache.csv",
            "results/subject_verb_agreement_balanced_l16/method_reliability_tracking_comparison.csv",
            "results/real_subject_verb_reliability/real_subject_verb_reliability_report.md",
        ],
        "metrics": "Mean-effect e-BH: L8 discoveries=6, uncentered_completeness=0.9685, centered_r2=0.6436, corr=0.8168; L12 discoveries=7, uncentered_completeness=0.9281, centered_r2=0.1874, corr=0.7259; L16 discoveries=23, uncentered_completeness=0.9632, centered_r2=0.5842, corr=0.7802; L20 discoveries=17, uncentered_completeness=0.5215, centered_r2=-4.4097, corr=0.1493. Tracking-aware single-feature/zero-feature rows are reported separately.",
        "missing_for_full_claim": "",
        "status_if_present": "supported_real",
        "status_if_missing": "missing_real_gpu",
    },
    {
        "claim_id": "REAL_FDR_DECOY",
        "paper_section": "Real LLM Evaluation",
        "claim": "On real Gemma/Gemma Scope subject-verb caches, a screen-score null-decoy stress test shows that e-BH rejects no constructed null decoys, while uncorrected p<q and screen-only top-score selection admit many.",
        "claim_scope_now": "Can be stated as a real-cache negative-control reliability analysis. It proves e-BH is buying test-split reliability against constructed null decoys, not that e-BH circuit quality beats top-score.",
        "evidence": [
            "results/real_subject_verb_reliability/decoy_reliability_summary.csv",
            "results/real_subject_verb_reliability/selection_stability_summary.csv",
            "results/real_subject_verb_reliability/real_q_grid.csv",
            "results/paper_assets/table_9_real_decoy_reliability.md",
            "results/paper_assets/table_10_real_selection_stability.md",
            "results/paper_assets/table_11_real_q_grid.md",
        ],
        "metrics": "Null decoys at q=0.1: e-BH selects 0 decoys at L8/L12/L16/L20; p<q selects 25.3/25.8/25.1/25.6 decoys on average; top-score matched to e-BH selects 3/6/23/15 decoys.",
        "missing_for_full_claim": "",
        "status_if_present": "supported_real_reliability",
        "status_if_missing": "missing_real_reliability",
    },
    {
        "claim_id": "REVIEWER_QF_SENSITIVITY",
        "paper_section": "Reviewer Empirical Gaps",
        "claim": "Reasonable CPU reweightings of the cached subject-verb resample-ablation estimand preserve the core e-BH selections at moderate-to-high overlap.",
        "claim_scope_now": "Can be stated as a cached sensitivity analysis over Q_f-style weighting variants, not as fresh GPU intervention evidence.",
        "evidence": [
            "scripts/run_reviewer_empirical_gaps.py",
            "results/reviewer_empirical_gaps/qf_sensitivity_summary.csv",
            "results/reviewer_empirical_gaps/reviewer_gap_conclusions.csv",
            "results/paper_assets/table_12_reviewer_qf_sensitivity.md",
        ],
        "metrics": "e-BH median Jaccard across non-baseline Q_f variants=0.979",
        "missing_for_full_claim": "Fresh GPU runs with alternative intervention estimands would be stronger, but are not required for the cached Q_f sensitivity claim.",
        "status_if_present": "supported_reviewer_empirical",
        "status_if_missing": "missing_reviewer_empirical",
    },
    {
        "claim_id": "REVIEWER_PVALUE_ROBUSTNESS",
        "paper_section": "Reviewer Empirical Gaps",
        "claim": "A sign-flip normal approximation gives comparable e-BH conclusions to the paired-t p-values, while finite Monte Carlo randomization/bootstrap p-values are too discrete for p-to-e e-BH at practical resample counts.",
        "claim_scope_now": "Can be stated as a p-value sensitivity result for the cached real subject-verb feature effects.",
        "evidence": [
            "scripts/run_reviewer_empirical_gaps.py",
            "results/reviewer_empirical_gaps/pvalue_robustness_summary.csv",
            "results/reviewer_empirical_gaps/reviewer_gap_conclusions.csv",
            "results/paper_assets/table_13_reviewer_pvalue_robustness.md",
        ],
        "metrics": "sign-flip normal e-BH median Jaccard to paired-t=0.929; finite-MC variants select 0 under p-to-e e-BH because the attainable p-value grid is too coarse.",
        "missing_for_full_claim": "This does not prove exact finite-sample optimality of any p-value estimator.",
        "status_if_present": "supported_reviewer_empirical",
        "status_if_missing": "missing_reviewer_empirical",
    },
    {
        "claim_id": "REVIEWER_ADAPTIVE_KNOCKOFF",
        "paper_section": "Reviewer Empirical Gaps",
        "claim": "Screen-covariate weighting, IHW-style binning, and AdaPT-lite recover additional discoveries, but the paired-decoy knockoff-plus diagnostic is over-liberal on this cache and must not be treated as a formal model-X knockoff result.",
        "claim_scope_now": "Can be stated as an empirical comparator table and risk audit, not as a validated replacement for e-BH.",
        "evidence": [
            "scripts/run_reviewer_empirical_gaps.py",
            "results/reviewer_empirical_gaps/method_comparison_summary.csv",
            "results/reviewer_empirical_gaps/decoy_robustness_summary.csv",
            "results/paper_assets/table_14_reviewer_method_comparison.md",
        ],
        "metrics": "adaptive median discoveries=33.5; paired-decoy knockoff median discoveries=256.0",
        "missing_for_full_claim": "Formal covariate-adaptive FDR or model-X knockoff claims would require methods with their assumptions verified for the SAE cache design.",
        "status_if_present": "supported_reviewer_empirical",
        "status_if_missing": "missing_reviewer_empirical",
    },
    {
        "claim_id": "REVIEWER_MULTISPLIT",
        "paper_section": "Reviewer Empirical Gaps",
        "claim": "Multi-split aggregation and four-fold cross-fitting provide stability checks for the real subject-verb selections, with a measured tradeoff against the single split.",
        "claim_scope_now": "Can be stated as a cached stability/sensitivity analysis, not as a universally better default procedure.",
        "evidence": [
            "scripts/run_reviewer_empirical_gaps.py",
            "results/reviewer_empirical_gaps/multisplit_summary.csv",
            "results/reviewer_empirical_gaps/reviewer_gap_conclusions.csv",
            "results/paper_assets/table_15_reviewer_multisplit.md",
        ],
        "metrics": "multi-split/crossfit median Jaccard to single split=0.594",
        "missing_for_full_claim": "More random splits can tighten the stability estimates.",
        "status_if_present": "supported_reviewer_empirical",
        "status_if_missing": "missing_reviewer_empirical",
    },
    {
        "claim_id": "REVIEWER_DECOY_ROBUSTNESS",
        "paper_section": "Reviewer Empirical Gaps",
        "claim": "Across multiple constructed-null decoy schemes, e-BH keeps decoy selections near zero while matched top-score selection fails when decoys are screen-attractive.",
        "claim_scope_now": "Can be stated as a constructed-null stress test separating test-split reliability from screen-rank artifacts.",
        "evidence": [
            "scripts/run_reviewer_empirical_gaps.py",
            "results/reviewer_empirical_gaps/decoy_robustness_summary.csv",
            "results/reviewer_empirical_gaps/reviewer_gap_conclusions.csv",
            "results/paper_assets/table_16_reviewer_decoy_robustness.md",
        ],
        "metrics": "e-BH decoys selected mean=0.001; matched top-score decoys selected mean=5.908",
        "missing_for_full_claim": "Constructed-null decoys are diagnostics, not a proof that all unobserved real null features are controlled beyond the stated FDR assumptions.",
        "status_if_present": "supported_reviewer_empirical",
        "status_if_missing": "missing_reviewer_empirical",
    },
    {
        "claim_id": "REVIEWER_TYPE_SM",
        "paper_section": "Reviewer Empirical Gaps",
        "claim": "In a downstream synthetic debiasing audit with task-irrelevant harmful features, controlled selections have low Type S removal and recover all harmful spurious features.",
        "claim_scope_now": "Can be stated for the synthetic downstream Type S/M operationalization used in the reviewer-gap analysis.",
        "evidence": [
            "scripts/run_reviewer_empirical_gaps.py",
            "results/reviewer_empirical_gaps/type_sm_summary.csv",
            "results/reviewer_empirical_gaps/reviewer_gap_conclusions.csv",
            "results/paper_assets/table_17_reviewer_type_sm.md",
        ],
        "metrics": "e_bh_pcal TypeS=0.000, TypeM=1.00; top_score_k_spurious TypeS=0.000, TypeM=1.00",
        "missing_for_full_claim": "This is a synthetic downstream audit; it is not a positive real BiasInBios debiasing claim.",
        "status_if_present": "supported_reviewer_empirical",
        "status_if_missing": "missing_reviewer_empirical",
    },
    {
        "claim_id": "SECOND_DECOY_BH_BY",
        "paper_section": "Second-Round Reviewer Gaps",
        "claim": "BH and BY are included in the real subject-verb constructed-null decoy stress test across all four layers and all four decoy schemes.",
        "claim_scope_now": "Can be stated as a real-cache constructed-null comparison of e-BH, BH, BY, uncorrected p<q, and matched top-score selection.",
        "evidence": [
            "scripts/run_second_round_reviewer_analyses.py",
            "results/second_round_reviewer/decoy_bh_by_all_schemes.csv",
            "results/second_round_reviewer/second_round_conclusions.csv",
            "results/paper_assets/table_18_second_round_decoy_bh_by.md",
        ],
        "metrics": "Mean constructed-null decoys selected across schemes: e-BH=0.001, BY=0.111, BH=1.233.",
        "missing_for_full_claim": "",
        "status_if_present": "supported_second_round_empirical",
        "status_if_missing": "missing_second_round_empirical",
    },
    {
        "claim_id": "SECOND_GAMMA_SENSITIVITY",
        "paper_section": "Second-Round Reviewer Gaps",
        "claim": "The p-to-e calibrator gamma grid {0.25, 0.5, 0.75} has synthetic and real sensitivity results for discoveries, stability, and synthetic FDP/power.",
        "claim_scope_now": "Can be stated for the requested gamma grid on Gate B synthetic outputs and four-layer real subject-verb caches.",
        "evidence": [
            "scripts/run_second_round_reviewer_analyses.py",
            "results/second_round_reviewer/gamma_sensitivity_synthetic_summary.csv",
            "results/second_round_reviewer/gamma_sensitivity_real.csv",
            "results/paper_assets/table_19_second_round_gamma_synthetic.md",
            "results/paper_assets/table_20_second_round_gamma_real.md",
        ],
        "metrics": "Synthetic max FDP across gamma grid=0.004; real nondefault gamma median Jaccard to gamma=0.5 is 0.611.",
        "missing_for_full_claim": "This is a finite requested grid, not an exhaustive calibrator-family optimization.",
        "status_if_present": "supported_second_round_empirical",
        "status_if_missing": "missing_second_round_empirical",
    },
    {
        "claim_id": "SECOND_REAL_CI_WIDTHS",
        "paper_section": "Second-Round Reviewer Gaps",
        "claim": "Real subject-verb selected features now have per-feature confidence-interval width distributions reported by layer and selection method.",
        "claim_scope_now": "Can be stated for the bootstrap-t CIs already produced by the real cache analyzer.",
        "evidence": [
            "scripts/run_second_round_reviewer_analyses.py",
            "results/second_round_reviewer/real_ci_type_s_per_feature.csv",
            "results/second_round_reviewer/real_ci_type_s_summary.csv",
            "results/paper_assets/table_21_second_round_real_ci_type_s.md",
            "results/paper_assets/figure_7_second_round_real_ci_type_s.png",
        ],
        "metrics": "e-BH selected CI width median=0.0266; median layer-level p90=0.1398.",
        "missing_for_full_claim": "Real CI coverage remains unobservable without ground truth; coverage calibration is still synthetic-only.",
        "status_if_present": "supported_second_round_empirical",
        "status_if_missing": "missing_second_round_empirical",
    },
    {
        "claim_id": "SECOND_REAL_TYPE_S_DIAGNOSTIC",
        "paper_section": "Second-Round Reviewer Gaps",
        "claim": "Real subject-verb discoveries include a Type S sign-instability diagnostic based on CI zero crossings and cluster-bootstrap sign flips.",
        "claim_scope_now": "Can be stated as a diagnostic for unknown-ground-truth real features, not as true Type S error measurement.",
        "evidence": [
            "scripts/run_second_round_reviewer_analyses.py",
            "results/second_round_reviewer/real_ci_type_s_per_feature.csv",
            "results/second_round_reviewer/real_ci_type_s_summary.csv",
            "results/paper_assets/table_21_second_round_real_ci_type_s.md",
            "results/paper_assets/figure_7_second_round_real_ci_type_s.png",
        ],
        "metrics": "e-BH selected Type S diagnostic median rate=0.000; max selected cluster-bootstrap sign-flip rate=0.000.",
        "missing_for_full_claim": "True real Type S error cannot be computed without known feature-level ground truth signs.",
        "status_if_present": "supported_second_round_empirical",
        "status_if_missing": "missing_second_round_empirical",
    },
    {
        "claim_id": "SECOND_COVARIATE_EBH",
        "paper_section": "Second-Round Reviewer Gaps",
        "claim": "A screen-stratified e-BH variant using disjoint q budgets across screen-score strata is evaluated as an arbitrary-dependence covariate-adaptive comparator.",
        "claim_scope_now": "Can be stated as a conservative screen-covariate e-BH comparison; it does not establish that covariate adaptation systematically improves power.",
        "evidence": [
            "scripts/run_second_round_reviewer_analyses.py",
            "results/second_round_reviewer/adaptive_ebh_summary.csv",
            "results/paper_assets/table_22_second_round_adaptive_ebh.md",
            "results/paper_assets/figure_8_second_round_summary.png",
        ],
        "metrics": "Synthetic stratified FDP=0.001; real median discovery gain versus default e-BH=0.0.",
        "missing_for_full_claim": "More adaptive procedures could be explored, but this result answers the requested guarantee-preserving screen-covariate e-BH check.",
        "status_if_present": "supported_second_round_empirical",
        "status_if_missing": "missing_second_round_empirical",
    },
    {
        "claim_id": "SECOND_CLUSTER_PERMUTATION",
        "paper_section": "Second-Round Reviewer Gaps",
        "claim": "Cluster-level tests re-check the real subject-verb discoveries under a more conservative prompt-cluster unit.",
        "claim_scope_now": "Can be stated for cluster-mean t and cluster sign-flip tests on the existing four-layer real caches; finite randomization p-values remain resolution-limited for p-to-e e-BH.",
        "evidence": [
            "scripts/run_second_round_reviewer_analyses.py",
            "results/second_round_reviewer/cluster_permutation_summary.csv",
            "results/paper_assets/table_23_second_round_cluster_permutation.md",
            "results/paper_assets/figure_8_second_round_summary.png",
        ],
        "metrics": "Cluster conservative e-BH median Jaccard to prompt paired-t e-BH=0.840.",
        "missing_for_full_claim": "This is a conservative dependence sensitivity check, not a replacement proof for every possible prompt-dependence structure.",
        "status_if_present": "supported_second_round_empirical",
        "status_if_missing": "missing_second_round_empirical",
    },
    {
        "claim_id": "REAL_LAYER_SCAN",
        "paper_section": "Real LLM Evaluation",
        "claim": "Under a fixed four-layer Gemma Scope protocol, subject-verb circuit discoverability is reported as a layer curve rather than a post-hoc chosen layer.",
        "claim_scope_now": "Can be stated only when all configured L8/L12/L16/L20 balanced subject-verb exact caches, FDR postprocessing, held-out joint circuit caches, and circuit summaries are present.",
        "evidence": [
            "configs/subject_verb_layer_scan_protocol.json",
            "results/subject_verb_agreement_balanced_l08/exact_ablation_cache.csv",
            "results/subject_verb_agreement_balanced_l08/method_reliability_tracking_comparison.csv",
            "results/subject_verb_agreement_balanced_l08/joint_circuit_cache.csv",
            "results/subject_verb_agreement_balanced_l08/circuit_cache_analysis/circuit_method_summary.csv",
            "results/subject_verb_agreement_balanced_l12/exact_ablation_cache.csv",
            "results/subject_verb_agreement_balanced_l12/method_reliability_tracking_comparison.csv",
            "results/subject_verb_agreement_balanced_l12/joint_circuit_cache.csv",
            "results/subject_verb_agreement_balanced_l12/circuit_cache_analysis/circuit_method_summary.csv",
            "results/subject_verb_agreement_balanced_l16/exact_ablation_cache.csv",
            "results/subject_verb_agreement_balanced_l16/method_reliability_tracking_comparison.csv",
            "results/subject_verb_agreement_balanced_l16/joint_circuit_cache.csv",
            "results/subject_verb_agreement_balanced_l16/circuit_cache_analysis/circuit_method_summary.csv",
            "results/subject_verb_agreement_balanced/exact_ablation_cache.csv",
            "results/subject_verb_agreement_balanced/method_reliability_tracking_comparison.csv",
            "results/subject_verb_agreement_balanced/joint_circuit_cache.csv",
            "results/subject_verb_agreement_balanced/circuit_cache_analysis/circuit_method_summary.csv",
            "results/real_subject_verb_reliability/layer_scan_summary.csv",
            "results/paper_assets/table_7_real_subject_verb.md",
        ],
        "metrics": "Fixed protocol layers: L8, L12, L16, L20. Report all layers; do not use L12 as a post-hoc winner.",
        "missing_for_full_claim": "",
        "status_if_present": "supported_real_layer_scan",
        "status_if_missing": "missing_real_layer_scan",
    },
    {
        "claim_id": "REAL_BIASINBIOS",
        "paper_section": "Real Downstream Evaluation",
        "claim": "A bounded real BiasInBios Gemma/Gemma Scope probe was executed, but e-BH selected no features and did not improve worst-group accuracy.",
        "claim_scope_now": "Can be stated only as a bounded negative/diagnostic result, not as positive real debiasing evidence.",
        "evidence": [
            "results/bias_in_bios/exact_ablation_cache.csv",
            "results/bias_in_bios/cache_analysis/selected_features_e_bh_pcal.csv",
            "results/bias_in_bios/bias_in_bios_prediction_cache.csv",
            "results/bias_in_bios/prediction_analysis/method_summary.csv",
        ],
        "metrics": "bounded n=60; e-BH discoveries=0; clean worst_group_acc=0.0; e_bh_pcal worst_group_acc=0.0; top_score overall_acc +0.05 with worst_group_acc unchanged",
        "missing_for_full_claim": "A positive full real BiasInBios debiasing claim would require a larger calibrated run with nonzero controlled discoveries; it is not claimed here.",
        "status_if_present": "bounded_real_negative",
        "status_if_missing": "missing_real_gpu",
    },
    {
        "claim_id": "REPRODUCIBILITY",
        "paper_section": "Reproducibility",
        "claim": "The artifact folder contains reproducibility commands, environment summaries, stage status, tests, and a curated submission package.",
        "claim_scope_now": "Can be stated for the current artifact folder.",
        "evidence": [
            "docs/reproducibility.md",
            "results/paper_assets/reproducibility_checklist.md",
            "results/paper_assets/environment_summary.md",
            "results/gpu_stage_status/gpu_stage_status.md",
            "results/submission_package/submission_package_manifest.csv",
        ],
        "missing_for_full_claim": "Full-sweep runtime rows will be added after the remaining RunPod outputs return.",
        "status_if_present": "supported",
    },
    {
        "claim_id": "COMPUTE_ACCOUNTING",
        "paper_section": "Reproducibility",
        "claim": "Compute metadata records runtime, hardware, and dry-run/real-run provenance.",
        "claim_scope_now": "Can be stated for local, dry-run, subject-verb full GPU, and bounded BiasInBios GPU provenance.",
        "evidence": ["results/paper_assets/compute_metadata_summary.csv", "results/paper_assets/compute_metadata_summary.md"],
        "missing_for_full_claim": "Full-dataset BiasInBios runtime remains future work.",
        "status_if_present": "partial",
    },
    {
        "claim_id": "SUBMISSION_READINESS",
        "paper_section": "Artifact Appendix",
        "claim": "Readiness audit distinguishes required complete evidence from the explicitly excluded positive real BiasInBios debiasing claim.",
        "claim_scope_now": "Can be stated as current-state audit for the completed real subject-verb reliability objective and bounded negative BiasInBios probe.",
        "evidence": ["results/submission_audit/submission_readiness_audit.md", "results/gpu_stage_status/next_gpu_action.md"],
        "missing_for_full_claim": "",
        "status_if_present": "supported",
    },
]


def main() -> None:
    args = parse_args()
    matrix = build_claim_matrix(ROOT)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    matrix.to_csv(args.output, index=False)
    write_markdown(args.report, matrix)
    print(f"wrote {matrix.shape[0]} claim-evidence rows to {safe_display_path(args.output)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a claim-to-evidence matrix for paper-writing support.")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "results" / "paper_assets" / "claim_evidence_matrix.csv",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=ROOT / "results" / "paper_assets" / "claim_evidence_matrix.md",
    )
    return parser.parse_args()


def build_claim_matrix(root: Path) -> pd.DataFrame:
    rows = []
    for spec in CLAIMS:
        evidence = spec["evidence"]
        missing = [path for path in evidence if not artifact_exists(root, path)]
        status = claim_status(spec, missing)
        rows.append(
            {
                "claim_id": spec["claim_id"],
                "paper_section": spec["paper_section"],
                "status": status,
                "claim": spec["claim"],
                "claim_scope_now": spec["claim_scope_now"],
                "evidence": "; ".join(evidence),
                "metrics": spec.get("metrics", ""),
                "missing_evidence": "; ".join(missing),
                "missing_for_full_claim": spec.get("missing_for_full_claim", ""),
            }
        )
    return pd.DataFrame(rows)


def claim_status(spec: dict[str, Any], missing: list[str]) -> str:
    if missing:
        return spec.get("status_if_missing", "missing")
    return spec["status_if_present"]


def artifact_exists(root: Path, rel_path: str) -> bool:
    path = root / rel_path
    return path.exists() and path.stat().st_size > 0


def write_markdown(path: Path, matrix: pd.DataFrame) -> None:
    status_counts = matrix.groupby("status", as_index=False).size().rename(columns={"size": "claims"})
    lines = [
        "# Claim Evidence Matrix",
        "",
        "This generated matrix maps paper-level claims to concrete artifacts.",
        "It is not paper prose; it is a support ledger for deciding what can",
        "currently be claimed and what still requires real GPU evidence.",
        "",
        "## Status Counts",
        "",
        status_counts.to_markdown(index=False),
        "",
        "## Claims",
        "",
        matrix.to_markdown(index=False),
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def safe_display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    main()
