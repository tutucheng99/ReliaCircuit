from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import stats


@dataclass(frozen=True)
class EffectInference:
    tau_hat: float
    se: float
    t_stat: float
    p_value: float
    ci_lower: float
    ci_upper: float


def paired_t_p_value(differences: np.ndarray) -> tuple[float, float, float, float]:
    """Return mean, standard error, t statistic, and two-sided p-value."""
    diffs = np.asarray(differences, dtype=float)
    if diffs.ndim != 1 or diffs.size < 2:
        raise ValueError("differences must be a one-dimensional array with n >= 2")
    tau_hat = float(np.mean(diffs))
    se = float(np.std(diffs, ddof=1) / np.sqrt(diffs.size))
    if se == 0.0:
        if tau_hat == 0.0:
            return tau_hat, 0.0, 0.0, 1.0
        return tau_hat, 0.0, np.inf * np.sign(tau_hat), 0.0
    t_stat = tau_hat / se
    p_value = float(2.0 * stats.t.sf(abs(t_stat), df=diffs.size - 1))
    return tau_hat, se, float(t_stat), p_value


def bootstrap_t_ci(
    differences: np.ndarray,
    rng: np.random.Generator,
    n_bootstrap: int = 499,
    confidence: float = 0.95,
    cluster_ids: np.ndarray | None = None,
) -> tuple[float, float]:
    """Bootstrap-t confidence interval for the mean paired difference."""
    diffs = np.asarray(differences, dtype=float)
    if diffs.ndim != 1 or diffs.size < 2:
        raise ValueError("differences must be a one-dimensional array with n >= 2")
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must be in (0, 1)")
    theta_hat = float(np.mean(diffs))
    se_hat = float(np.std(diffs, ddof=1) / np.sqrt(diffs.size))
    if se_hat == 0.0:
        return theta_hat, theta_hat

    boot_t = np.empty(n_bootstrap, dtype=float)
    for b in range(n_bootstrap):
        sample = _bootstrap_sample(diffs, rng, cluster_ids)
        theta_b = float(np.mean(sample))
        se_b = float(np.std(sample, ddof=1) / np.sqrt(sample.size))
        boot_t[b] = 0.0 if se_b == 0.0 else (theta_b - theta_hat) / se_b

    alpha = 1.0 - confidence
    low_q = float(np.quantile(boot_t, 1.0 - alpha / 2.0))
    high_q = float(np.quantile(boot_t, alpha / 2.0))
    return theta_hat - low_q * se_hat, theta_hat - high_q * se_hat


def infer_effect(
    differences: np.ndarray,
    rng: np.random.Generator,
    n_bootstrap: int = 499,
    confidence: float = 0.95,
    cluster_ids: np.ndarray | None = None,
) -> EffectInference:
    tau_hat, se, t_stat, p_value = paired_t_p_value(differences)
    ci_lower, ci_upper = bootstrap_t_ci(
        differences,
        rng=rng,
        n_bootstrap=n_bootstrap,
        confidence=confidence,
        cluster_ids=cluster_ids,
    )
    return EffectInference(
        tau_hat=tau_hat,
        se=se,
        t_stat=t_stat,
        p_value=p_value,
        ci_lower=float(ci_lower),
        ci_upper=float(ci_upper),
    )


def _bootstrap_sample(
    diffs: np.ndarray,
    rng: np.random.Generator,
    cluster_ids: np.ndarray | None,
) -> np.ndarray:
    if cluster_ids is None:
        return diffs[rng.integers(0, diffs.size, size=diffs.size)]

    clusters = np.asarray(cluster_ids)
    if clusters.shape[0] != diffs.shape[0]:
        raise ValueError("cluster_ids must have the same length as differences")
    unique = np.unique(clusters)
    sampled_clusters = unique[rng.integers(0, unique.size, size=unique.size)]
    pieces = [diffs[clusters == cid] for cid in sampled_clusters]
    return np.concatenate(pieces)
