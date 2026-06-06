from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class SyntheticConfig:
    n_prompts: int = 1200
    n_features: int = 512
    n_active: int = 24
    n_blocks: int = 32
    within_block_corr: float = 0.35
    active_mean_shift: float = 1.25
    null_mean_shift_sd: float = 0.15
    effect_size: float = 0.55
    nuisance_effect_sd: float = 0.25
    metric_noise_sd: float = 0.4
    cluster_size: int = 8
    seed: int = 0


@dataclass
class SyntheticDataset:
    clean: np.ndarray
    patch: np.ndarray
    beta: np.ndarray
    clean_mean: np.ndarray
    patch_mean: np.ndarray
    active_features: np.ndarray
    cluster_ids: np.ndarray
    observed_metric: np.ndarray
    local_effects: np.ndarray

    @property
    def n_prompts(self) -> int:
        return int(self.clean.shape[0])

    @property
    def n_features(self) -> int:
        return int(self.clean.shape[1])

    @property
    def population_tau(self) -> np.ndarray:
        return self.beta * (self.clean_mean - self.patch_mean)

    @property
    def finite_tau(self) -> np.ndarray:
        patch_mean = np.mean(self.patch, axis=0)
        clean_delta = self.clean - patch_mean
        return np.mean((self.beta[None, :] + self.local_effects) * clean_delta, axis=0)

    @property
    def true_tau(self) -> np.ndarray:
        return self.finite_tau

    @property
    def is_active(self) -> np.ndarray:
        mask = np.zeros(self.n_features, dtype=bool)
        mask[self.active_features] = True
        return mask

    def forward(self, features: np.ndarray) -> np.ndarray:
        return features @ self.beta

    def ablation_differences(
        self,
        feature: int,
        prompt_indices: np.ndarray,
        rng: np.random.Generator,
    ) -> np.ndarray:
        """Clean metric minus metric after resample-ablation of one feature."""
        idx = np.asarray(prompt_indices, dtype=int)
        patch_rows = rng.integers(0, self.patch.shape[0], size=idx.size)
        delta = self.clean[idx, feature] - self.patch[patch_rows, feature]
        prompt_local_effect = self.local_effects[idx, feature]
        return (self.beta[feature] + prompt_local_effect) * delta

    def paired_behavior_difference(
        self,
        prompt_indices: np.ndarray,
        features: np.ndarray | None = None,
        include_local_effects: bool = True,
    ) -> np.ndarray:
        """Clean minus patch behavior difference on paired held-out prompts."""
        idx = np.asarray(prompt_indices, dtype=int)
        if features is None:
            feat = np.arange(self.n_features)
        else:
            feat = np.asarray(features, dtype=int)
        if feat.size == 0:
            return np.zeros(idx.size, dtype=float)
        delta = self.clean[np.ix_(idx, feat)] - self.patch[np.ix_(idx, feat)]
        effects = self.beta[feat][None, :]
        if include_local_effects:
            effects = effects + self.local_effects[np.ix_(idx, feat)]
        return np.sum(effects * delta, axis=1)


def generate_synthetic_dataset(config: SyntheticConfig) -> SyntheticDataset:
    rng = np.random.default_rng(config.seed)
    if config.n_active >= config.n_features:
        raise ValueError("n_active must be smaller than n_features")
    if not 0.0 <= config.within_block_corr < 1.0:
        raise ValueError("within_block_corr must be in [0, 1)")

    active = np.sort(rng.choice(config.n_features, size=config.n_active, replace=False))
    clean_mean = rng.normal(0.0, config.null_mean_shift_sd, size=config.n_features)
    patch_mean = rng.normal(0.0, config.null_mean_shift_sd, size=config.n_features)
    signs = rng.choice([-1.0, 1.0], size=config.n_active)
    clean_mean[active] = 0.5 * config.active_mean_shift
    patch_mean[active] = -0.5 * config.active_mean_shift

    beta = np.zeros(config.n_features, dtype=float)
    beta[active] = signs * config.effect_size * rng.uniform(0.8, 1.2, size=config.n_active)

    clean = _block_correlated_normal(
        rng,
        n_rows=config.n_prompts,
        n_features=config.n_features,
        n_blocks=config.n_blocks,
        corr=config.within_block_corr,
        mean=clean_mean,
    )
    patch = _block_correlated_normal(
        rng,
        n_rows=config.n_prompts,
        n_features=config.n_features,
        n_blocks=config.n_blocks,
        corr=config.within_block_corr,
        mean=patch_mean,
    )
    metric_noise = rng.normal(0.0, config.metric_noise_sd, size=config.n_prompts)
    observed_metric = clean @ beta + metric_noise
    local_effects = rng.normal(
        0.0,
        config.nuisance_effect_sd,
        size=(config.n_prompts, config.n_features),
    )
    cluster_ids = np.arange(config.n_prompts) // max(1, config.cluster_size)

    return SyntheticDataset(
        clean=clean,
        patch=patch,
        beta=beta,
        clean_mean=clean_mean,
        patch_mean=patch_mean,
        active_features=active,
        cluster_ids=cluster_ids,
        observed_metric=observed_metric,
        local_effects=local_effects,
    )


def _block_correlated_normal(
    rng: np.random.Generator,
    n_rows: int,
    n_features: int,
    n_blocks: int,
    corr: float,
    mean: np.ndarray,
) -> np.ndarray:
    x = np.empty((n_rows, n_features), dtype=float)
    block_edges = np.linspace(0, n_features, num=n_blocks + 1, dtype=int)
    shared_scale = np.sqrt(corr)
    private_scale = np.sqrt(1.0 - corr)
    for start, end in zip(block_edges[:-1], block_edges[1:]):
        if start == end:
            continue
        shared = rng.normal(0.0, 1.0, size=(n_rows, 1))
        private = rng.normal(0.0, 1.0, size=(n_rows, end - start))
        x[:, start:end] = shared_scale * shared + private_scale * private
    return x + mean
