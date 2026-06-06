from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from reliacircuit.fdr import bh, by_bh, e_bh, p_threshold, p_to_e_value
from reliacircuit.inference import infer_effect
from reliacircuit.synthetic import SyntheticConfig, generate_synthetic_dataset


@dataclass(frozen=True)
class PipelineConfig:
    synthetic: SyntheticConfig
    screen_fraction: float = 0.4
    test_fraction: float = 0.4
    screen_n: int = 96
    q: float = 0.1
    e_gamma: float = 0.5
    n_bootstrap: int = 399
    confidence: float = 0.95


def run_replicate(config: PipelineConfig, replicate: int) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    synthetic_config = SyntheticConfig(**{**config.synthetic.__dict__, "seed": config.synthetic.seed + replicate})
    dataset = generate_synthetic_dataset(synthetic_config)
    rng = np.random.default_rng(synthetic_config.seed + 1_000_003)
    screen_idx, test_idx, heldout_idx = make_splits(
        dataset.n_prompts,
        rng=rng,
        screen_fraction=config.screen_fraction,
        test_fraction=config.test_fraction,
    )
    screen_order, screen_scores = screen_features(dataset, screen_idx, config.screen_n, rng)
    feature_rows = []
    for rank, feature in enumerate(screen_order, start=1):
        diffs = dataset.ablation_differences(feature, test_idx, rng)
        cluster_ids = dataset.cluster_ids[test_idx]
        effect = infer_effect(
            diffs,
            rng=rng,
            n_bootstrap=config.n_bootstrap,
            confidence=config.confidence,
            cluster_ids=cluster_ids,
        )
        true_tau = float(dataset.true_tau[feature])
        population_tau = float(dataset.population_tau[feature])
        feature_rows.append(
            {
                "replicate": replicate,
                "feature": int(feature),
                "screen_rank": rank,
                "screen_score": float(screen_scores[feature]),
                "is_active": bool(dataset.is_active[feature]),
                "population_tau": population_tau,
                "true_tau": true_tau,
                "tau_hat": effect.tau_hat,
                "se": effect.se,
                "t_stat": effect.t_stat,
                "p_value": effect.p_value,
                "e_value": float(p_to_e_value(np.array([effect.p_value]), gamma=config.e_gamma)[0]),
                "ci_lower": effect.ci_lower,
                "ci_upper": effect.ci_upper,
                "ci_covers": bool(effect.ci_lower <= true_tau <= effect.ci_upper),
                "ci_covers_population": bool(effect.ci_lower <= population_tau <= effect.ci_upper),
            }
        )

    features = pd.DataFrame(feature_rows)
    summary = summarize_methods(
        features=features,
        q=config.q,
        n_total_active=synthetic_config.n_active,
        heldout_n=heldout_idx.size,
    )
    circuit_summary = summarize_circuits(
        dataset=dataset,
        features=features,
        method_summary=summary,
        q=config.q,
        heldout_idx=heldout_idx,
    )
    return features, summary, circuit_summary


def make_splits(
    n: int,
    rng: np.random.Generator,
    screen_fraction: float,
    test_fraction: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if screen_fraction <= 0.0 or test_fraction <= 0.0 or screen_fraction + test_fraction >= 1.0:
        raise ValueError("screen/test fractions must be positive and leave a heldout split")
    order = rng.permutation(n)
    n_screen = int(round(n * screen_fraction))
    n_test = int(round(n * test_fraction))
    screen_idx = order[:n_screen]
    test_idx = order[n_screen : n_screen + n_test]
    heldout_idx = order[n_screen + n_test :]
    return screen_idx, test_idx, heldout_idx


def screen_features(
    dataset,
    prompt_indices: np.ndarray,
    top_n: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    """Cheap attribution-patching proxy used only on split A."""
    idx = np.asarray(prompt_indices, dtype=int)
    patch_rows = rng.integers(0, dataset.patch.shape[0], size=idx.size)
    delta = dataset.clean[idx] - dataset.patch[patch_rows]
    metric = dataset.observed_metric[idx]
    centered_metric = metric - np.mean(metric)
    scores = np.abs(np.mean(delta * centered_metric[:, None], axis=0))
    jitter = rng.uniform(0.0, 1e-12, size=scores.size)
    order = np.argsort(-(scores + jitter))[:top_n]
    return order, scores


def summarize_methods(
    features: pd.DataFrame,
    q: float,
    n_total_active: int,
    heldout_n: int,
) -> pd.DataFrame:
    p = features["p_value"].to_numpy()
    e = features["e_value"].to_numpy()
    methods = {
        "e_bh_pcal": e_bh(e, q),
        "by_bh": by_bh(p, q),
        "bh": bh(p, q),
        "p_lt_q": p_threshold(p, q),
        "top_score_k_active": features["screen_rank"].to_numpy() <= n_total_active,
    }
    rows = []
    active = features["is_active"].to_numpy(dtype=bool)
    ci_covers = features["ci_covers"].to_numpy(dtype=bool)
    for name, reject in methods.items():
        discoveries = int(np.sum(reject))
        false_discoveries = int(np.sum(reject & ~active))
        true_discoveries = int(np.sum(reject & active))
        selected_coverage = np.nan
        if discoveries > 0:
            selected_coverage = float(np.mean(ci_covers[reject]))
        rows.append(
            {
                "replicate": int(features["replicate"].iloc[0]),
                "method": name,
                "discoveries": discoveries,
                "false_discoveries": false_discoveries,
                "true_discoveries": true_discoveries,
                "fdp": false_discoveries / max(discoveries, 1),
                "power": true_discoveries / max(n_total_active, 1),
                "ci_coverage_selected": selected_coverage,
                "screen_recall": float(np.mean(active)) * features.shape[0] / max(n_total_active, 1),
                "ci_coverage_screened": float(np.mean(ci_covers)),
                "heldout_n": int(heldout_n),
            }
        )
    return pd.DataFrame(rows)


def summarize_circuits(
    dataset,
    features: pd.DataFrame,
    method_summary: pd.DataFrame,
    q: float,
    heldout_idx: np.ndarray,
) -> pd.DataFrame:
    p = features["p_value"].to_numpy()
    e = features["e_value"].to_numpy()
    methods = {
        "e_bh_pcal": e_bh(e, q),
        "by_bh": by_bh(p, q),
        "bh": bh(p, q),
        "p_lt_q": p_threshold(p, q),
        "top_score_k_active": features["screen_rank"].to_numpy() <= int(dataset.is_active.sum()),
    }
    full = dataset.paired_behavior_difference(heldout_idx, include_local_effects=False)
    rows = []
    replicate = int(features["replicate"].iloc[0])
    for name, reject in methods.items():
        selected_features = features.loc[reject, "feature"].to_numpy(dtype=int)
        selected = dataset.paired_behavior_difference(
            heldout_idx,
            selected_features,
            include_local_effects=False,
        )
        rows.append(
            {
                "replicate": replicate,
                "method": name,
                "heldout_n": int(len(heldout_idx)),
                "selected_features": int(selected_features.size),
                **_circuit_metrics(full, selected),
            }
        )
    merged = pd.DataFrame(rows).merge(
        method_summary[
            [
                "replicate",
                "method",
                "discoveries",
                "false_discoveries",
                "true_discoveries",
                "fdp",
                "power",
            ]
        ],
        on=["replicate", "method"],
        how="left",
    )
    return merged


def _circuit_metrics(full: np.ndarray, selected: np.ndarray) -> dict[str, float]:
    full = np.asarray(full, dtype=float)
    selected = np.asarray(selected, dtype=float)
    residual = full - selected
    full_mse = float(np.mean(full**2))
    residual_mse = float(np.mean(residual**2))
    selected_mse = float(np.mean(selected**2))
    abs_full = float(np.mean(np.abs(full)))
    abs_selected = float(np.mean(np.abs(selected)))
    completeness = 1.0 - residual_mse / max(full_mse, 1e-12)
    necessity = selected_mse / max(full_mse, 1e-12)
    if np.std(full) == 0.0 or np.std(selected) == 0.0:
        corr = np.nan
    else:
        corr = float(np.corrcoef(full, selected)[0, 1])
    sign_mask = np.abs(full) > 1e-12
    sign_agreement = np.nan
    if np.any(sign_mask):
        sign_agreement = float(np.mean(np.sign(full[sign_mask]) == np.sign(selected[sign_mask])))
    return {
        "heldout_full_mse": full_mse,
        "heldout_residual_mse": residual_mse,
        "heldout_selected_mse": selected_mse,
        "completeness_r2": float(completeness),
        "necessity_fraction": float(necessity),
        "abs_effect_fraction": abs_selected / max(abs_full, 1e-12),
        "selected_full_corr": corr,
        "sign_agreement": sign_agreement,
    }
