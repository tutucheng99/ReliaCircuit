from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy import stats

from reliacircuit.fdr import bh, by_bh, e_bh, p_threshold, p_to_e_value


@dataclass(frozen=True)
class DebiasConfig:
    n_train: int = 1600
    n_test: int = 1600
    n_features: int = 256
    n_task: int = 24
    n_spurious: int = 24
    n_proxy: int = 24
    n_blocks: int = 32
    within_block_corr: float = 0.25
    task_signal: float = 1.0
    spurious_signal: float = 1.0
    proxy_signal: float = 1.0
    task_weight: float = 0.9
    spurious_weight: float = 0.8
    train_alignment_prob: float = 0.9
    test_alignment_prob: float = 0.5
    screen_fraction: float = 0.4
    test_fraction: float = 0.4
    q: float = 0.1
    e_gamma: float = 0.5
    seed: int = 0


@dataclass
class DebiasDataset:
    x_train: np.ndarray
    y_train: np.ndarray
    g_train: np.ndarray
    x_test: np.ndarray
    y_test: np.ndarray
    g_test: np.ndarray
    weights: np.ndarray
    task_features: np.ndarray
    spurious_features: np.ndarray
    proxy_features: np.ndarray

    @property
    def n_features(self) -> int:
        return int(self.weights.size)

    @property
    def is_task(self) -> np.ndarray:
        mask = np.zeros(self.n_features, dtype=bool)
        mask[self.task_features] = True
        return mask

    @property
    def is_spurious(self) -> np.ndarray:
        mask = np.zeros(self.n_features, dtype=bool)
        mask[self.spurious_features] = True
        return mask

    @property
    def is_proxy(self) -> np.ndarray:
        mask = np.zeros(self.n_features, dtype=bool)
        mask[self.proxy_features] = True
        return mask


def generate_debias_dataset(config: DebiasConfig) -> DebiasDataset:
    rng = np.random.default_rng(config.seed)
    if config.n_task + config.n_spurious + config.n_proxy >= config.n_features:
        raise ValueError("n_task + n_spurious + n_proxy must be smaller than n_features")
    all_features = np.arange(config.n_features)
    task = np.sort(rng.choice(all_features, size=config.n_task, replace=False))
    remaining = np.setdiff1d(all_features, task)
    spurious = np.sort(rng.choice(remaining, size=config.n_spurious, replace=False))
    remaining = np.setdiff1d(remaining, spurious)
    proxy = np.sort(rng.choice(remaining, size=config.n_proxy, replace=False))

    y_train, g_train = sample_labels(rng, config.n_train, config.train_alignment_prob)
    y_test, g_test = sample_labels(rng, config.n_test, config.test_alignment_prob)
    x_train = sample_features(rng, config, y_train, g_train, task, spurious, proxy)
    x_test = sample_features(rng, config, y_test, g_test, task, spurious, proxy)

    weights = np.zeros(config.n_features, dtype=float)
    weights[task] = config.task_weight * rng.uniform(0.8, 1.2, size=config.n_task)
    weights[spurious] = config.spurious_weight * rng.uniform(0.8, 1.2, size=config.n_spurious)

    return DebiasDataset(
        x_train=x_train,
        y_train=y_train,
        g_train=g_train,
        x_test=x_test,
        y_test=y_test,
        g_test=g_test,
        weights=weights,
        task_features=task,
        spurious_features=spurious,
        proxy_features=proxy,
    )


def sample_labels(rng: np.random.Generator, n: int, alignment_prob: float) -> tuple[np.ndarray, np.ndarray]:
    y = rng.choice([-1, 1], size=n)
    aligned = rng.random(n) < alignment_prob
    g = np.where(aligned, y, -y)
    return y.astype(int), g.astype(int)


def sample_features(
    rng: np.random.Generator,
    config: DebiasConfig,
    y: np.ndarray,
    g: np.ndarray,
    task_features: np.ndarray,
    spurious_features: np.ndarray,
    proxy_features: np.ndarray,
) -> np.ndarray:
    mean = np.zeros((y.size, config.n_features), dtype=float)
    mean[:, task_features] = config.task_signal * y[:, None]
    mean[:, spurious_features] = config.spurious_signal * g[:, None]
    mean[:, proxy_features] = config.proxy_signal * g[:, None]
    x = block_correlated_noise(
        rng,
        n_rows=y.size,
        n_features=config.n_features,
        n_blocks=config.n_blocks,
        corr=config.within_block_corr,
    )
    return x + mean


def block_correlated_noise(
    rng: np.random.Generator,
    n_rows: int,
    n_features: int,
    n_blocks: int,
    corr: float,
) -> np.ndarray:
    x = np.empty((n_rows, n_features), dtype=float)
    edges = np.linspace(0, n_features, num=n_blocks + 1, dtype=int)
    shared_scale = np.sqrt(corr)
    private_scale = np.sqrt(1.0 - corr)
    for start, end in zip(edges[:-1], edges[1:]):
        shared = rng.normal(0.0, 1.0, size=(n_rows, 1))
        private = rng.normal(0.0, 1.0, size=(n_rows, end - start))
        x[:, start:end] = shared_scale * shared + private_scale * private
    return x


def run_debias_replicate(config: DebiasConfig, replicate: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    cfg = DebiasConfig(**{**config.__dict__, "seed": config.seed + replicate})
    dataset = generate_debias_dataset(cfg)
    rng = np.random.default_rng(cfg.seed + 9173)
    screen_idx, infer_idx = split_train_indices(cfg, rng)
    feature_stats = feature_gender_effects(dataset, screen_idx, infer_idx, cfg)
    eval_table = evaluate_removal_methods(dataset, feature_stats, cfg, rng)
    feature_stats.insert(0, "replicate", replicate)
    eval_table.insert(0, "replicate", replicate)
    return feature_stats, eval_table


def split_train_indices(config: DebiasConfig, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    order = rng.permutation(config.n_train)
    n_screen = int(round(config.n_train * config.screen_fraction))
    n_infer = int(round(config.n_train * config.test_fraction))
    return order[:n_screen], order[n_screen : n_screen + n_infer]


def feature_gender_effects(
    dataset: DebiasDataset,
    screen_idx: np.ndarray,
    infer_idx: np.ndarray,
    config: DebiasConfig,
) -> pd.DataFrame:
    x_screen = dataset.x_train[screen_idx]
    y_screen = dataset.y_train[screen_idx]
    g_screen = dataset.g_train[screen_idx]
    screen_scores = np.abs(residualized_gender_coefficients(x_screen, y_screen, g_screen))

    rows = []
    x_infer = dataset.x_train[infer_idx]
    y_infer = dataset.y_train[infer_idx]
    g_infer = dataset.g_train[infer_idx]
    residual_x, residual_g = residualize_against_label(x_infer, y_infer, g_infer)
    denom = float(np.mean(residual_g**2))
    if denom <= 1e-12:
        raise ValueError("gender residual has near-zero variance; lower train_alignment_prob")
    for feature in range(dataset.n_features):
        influence = dataset.weights[feature] * residual_x[:, feature] * residual_g / denom
        tau_hat = float(np.mean(influence))
        se = float(np.std(influence, ddof=1) / np.sqrt(influence.size))
        if se == 0.0:
            t_stat = np.inf if tau_hat != 0.0 else 0.0
            p_value = 0.0 if tau_hat != 0.0 else 1.0
        else:
            t_stat = tau_hat / se
            p_value = float(2.0 * stats.t.sf(abs(t_stat), df=influence.size - 1))
        rows.append(
            {
                "feature": feature,
                "screen_score": float(screen_scores[feature]),
                "tau_gender": tau_hat,
                "se": se,
                "t_stat": float(t_stat),
                "p_value": p_value,
                "e_value": float(p_to_e_value(np.array([p_value]), gamma=config.e_gamma)[0]),
                "is_task": bool(dataset.is_task[feature]),
                "is_spurious": bool(dataset.is_spurious[feature]),
                "is_proxy": bool(dataset.is_proxy[feature]),
                "is_noise": bool(
                    (not dataset.is_task[feature])
                    and (not dataset.is_spurious[feature])
                    and (not dataset.is_proxy[feature])
                ),
            }
        )
    return pd.DataFrame(rows)


def residualized_gender_coefficients(x: np.ndarray, y: np.ndarray, g: np.ndarray) -> np.ndarray:
    residual_x, residual_g = residualize_against_label(x, y, g)
    denom = float(np.mean(residual_g**2))
    if denom <= 1e-12:
        raise ValueError("gender residual has near-zero variance; lower alignment probability")
    return np.mean(residual_x * residual_g[:, None], axis=0) / denom


def residualize_against_label(x: np.ndarray, y: np.ndarray, g: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    residual_x = np.empty_like(x, dtype=float)
    residual_g = np.empty_like(g, dtype=float)
    for label in [-1, 1]:
        mask = y == label
        if not np.any(mask):
            raise ValueError(f"missing label {label} in split")
        residual_x[mask] = x[mask] - np.mean(x[mask], axis=0, keepdims=True)
        residual_g[mask] = g[mask] - float(np.mean(g[mask]))
    return residual_x, residual_g


def evaluate_removal_methods(
    dataset: DebiasDataset,
    feature_stats: pd.DataFrame,
    config: DebiasConfig,
    rng: np.random.Generator,
) -> pd.DataFrame:
    p = feature_stats["p_value"].to_numpy(dtype=float)
    e = feature_stats["e_value"].to_numpy(dtype=float)
    n_spurious = int(dataset.is_spurious.sum())
    methods = {
        "none": np.zeros(dataset.n_features, dtype=bool),
        "oracle_spurious": dataset.is_spurious.copy(),
        "e_bh_pcal": e_bh(e, config.q),
        "by_bh": by_bh(p, config.q),
        "bh": bh(p, config.q),
        "p_lt_q": p_threshold(p, config.q),
        "top_score_k_spurious": top_k_mask(feature_stats["screen_score"].to_numpy(dtype=float), n_spurious),
        "random_k_spurious": random_k_mask(dataset.n_features, n_spurious, rng),
    }
    rows = []
    for method, remove in methods.items():
        metrics = evaluate_mask(dataset, remove)
        task_removed = int(np.sum(remove & dataset.is_task))
        spurious_removed = int(np.sum(remove & dataset.is_spurious))
        proxy_removed = int(np.sum(remove & dataset.is_proxy))
        noise_removed = int(np.sum(remove & ~(dataset.is_task | dataset.is_spurious | dataset.is_proxy)))
        rows.append(
            {
                "method": method,
                "removed": int(np.sum(remove)),
                "spurious_removed": spurious_removed,
                "task_removed": task_removed,
                "proxy_removed": proxy_removed,
                "noise_removed": noise_removed,
                "erroneous_removal_rate": (task_removed + proxy_removed + noise_removed) / max(int(np.sum(remove)), 1),
                "spurious_recall": spurious_removed / max(n_spurious, 1),
                **metrics,
            }
        )
    return pd.DataFrame(rows)


def evaluate_mask(dataset: DebiasDataset, remove: np.ndarray) -> dict[str, float]:
    weights = dataset.weights.copy()
    weights[remove] = 0.0
    score = dataset.x_test @ weights
    pred = np.where(score >= 0.0, 1, -1)
    correct = pred == dataset.y_test
    group_values = []
    for y in [-1, 1]:
        for g in [-1, 1]:
            mask = (dataset.y_test == y) & (dataset.g_test == g)
            if np.any(mask):
                group_values.append(float(np.mean(correct[mask])))
    aligned = dataset.y_test == dataset.g_test
    conflict = ~aligned
    return {
        "overall_acc": float(np.mean(correct)),
        "worst_group_acc": float(np.min(group_values)),
        "aligned_acc": float(np.mean(correct[aligned])),
        "conflict_acc": float(np.mean(correct[conflict])),
        "gap_aligned_conflict": float(np.mean(correct[aligned]) - np.mean(correct[conflict])),
        "mean_abs_score": float(np.mean(np.abs(score))),
    }


def top_k_mask(scores: np.ndarray, k: int) -> np.ndarray:
    mask = np.zeros(scores.size, dtype=bool)
    if k <= 0:
        return mask
    order = np.argsort(-np.abs(scores))[:k]
    mask[order] = True
    return mask


def random_k_mask(n: int, k: int, rng: np.random.Generator) -> np.ndarray:
    mask = np.zeros(n, dtype=bool)
    if k <= 0:
        return mask
    mask[rng.choice(n, size=min(k, n), replace=False)] = True
    return mask
