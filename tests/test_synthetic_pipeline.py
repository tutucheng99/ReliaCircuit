from reliacircuit.pipeline import PipelineConfig, run_replicate
from reliacircuit.synthetic import SyntheticConfig, generate_synthetic_dataset


def test_synthetic_dataset_has_known_active_effects():
    cfg = SyntheticConfig(n_prompts=100, n_features=40, n_active=5, n_blocks=5, seed=7)
    dataset = generate_synthetic_dataset(cfg)
    assert dataset.clean.shape == (100, 40)
    assert dataset.patch.shape == (100, 40)
    assert dataset.is_active.sum() == 5
    assert (dataset.population_tau[dataset.is_active] != 0).all()
    assert (dataset.population_tau[~dataset.is_active] == 0).all()
    assert dataset.finite_tau.shape == (40,)


def test_pipeline_replicate_outputs_tables():
    synth = SyntheticConfig(
        n_prompts=160,
        n_features=60,
        n_active=6,
        n_blocks=6,
        seed=11,
    )
    cfg = PipelineConfig(
        synthetic=synth,
        screen_n=20,
        n_bootstrap=19,
    )
    features, summary, circuit = run_replicate(cfg, replicate=0)
    assert features.shape[0] == 20
    assert {"e_bh_pcal", "by_bh", "bh", "p_lt_q", "top_score_k_active"} == set(summary["method"])
    assert features["ci_covers"].notna().all()
    assert {"e_bh_pcal", "by_bh", "bh", "p_lt_q", "top_score_k_active"} == set(circuit["method"])
    assert circuit["completeness_r2"].notna().all()
