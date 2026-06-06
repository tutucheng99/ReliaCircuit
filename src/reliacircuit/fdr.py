from __future__ import annotations

import numpy as np


def bh(p_values: np.ndarray, q: float) -> np.ndarray:
    """Benjamini-Hochberg rejection mask."""
    p = _validate_p_values(p_values)
    if p.size == 0:
        return np.zeros(0, dtype=bool)
    order = np.argsort(p)
    ranked = p[order]
    thresholds = q * np.arange(1, p.size + 1) / p.size
    passing = ranked <= thresholds
    reject = np.zeros(p.size, dtype=bool)
    if np.any(passing):
        k = int(np.flatnonzero(passing)[-1]) + 1
        reject[order[:k]] = True
    return reject


def by_bh(p_values: np.ndarray, q: float) -> np.ndarray:
    """Benjamini-Yekutieli rejection mask for arbitrary dependence."""
    p = _validate_p_values(p_values)
    if p.size == 0:
        return np.zeros(0, dtype=bool)
    harmonic = np.sum(1.0 / np.arange(1, p.size + 1))
    return bh(p, q / harmonic)


def p_threshold(p_values: np.ndarray, alpha: float) -> np.ndarray:
    """Uncorrected p-value selection baseline."""
    p = _validate_p_values(p_values)
    return p <= alpha


def p_to_e_value(p_values: np.ndarray, gamma: float = 0.5) -> np.ndarray:
    """Convert p-values to e-values using a power calibrator.

    For 0 < gamma < 1, e(p) = (1 - gamma) * p^(-gamma) integrates to one on
    Uniform(0, 1), so it is a valid p-to-e calibrator under exact null p-values.
    """
    if not 0.0 < gamma < 1.0:
        raise ValueError("gamma must be in (0, 1)")
    p = _validate_p_values(p_values)
    clipped = np.clip(p, 1e-300, 1.0)
    return (1.0 - gamma) * np.power(clipped, -gamma)


def e_bh(e_values: np.ndarray, q: float) -> np.ndarray:
    """e-BH rejection mask.

    Sort e-values descending and reject the largest k values when
    e_(k) >= m / (q k). This controls FDR under arbitrary dependence for
    valid e-values.
    """
    e = np.asarray(e_values, dtype=float)
    if e.ndim != 1:
        raise ValueError("e_values must be one-dimensional")
    if np.any(~np.isfinite(e)) or np.any(e < 0.0):
        raise ValueError("e_values must be finite and nonnegative")
    if e.size == 0:
        return np.zeros(0, dtype=bool)
    order = np.argsort(-e)
    ranked = e[order]
    thresholds = e.size / (q * np.arange(1, e.size + 1))
    passing = ranked >= thresholds
    reject = np.zeros(e.size, dtype=bool)
    if np.any(passing):
        k = int(np.flatnonzero(passing)[-1]) + 1
        reject[order[:k]] = True
    return reject


def _validate_p_values(p_values: np.ndarray) -> np.ndarray:
    p = np.asarray(p_values, dtype=float)
    if p.ndim != 1:
        raise ValueError("p_values must be one-dimensional")
    if np.any(~np.isfinite(p)) or np.any((p < 0.0) | (p > 1.0)):
        raise ValueError("p_values must be finite and in [0, 1]")
    return p
