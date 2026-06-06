from reliacircuit.debias import DebiasConfig, generate_debias_dataset, run_debias_replicate


def test_debias_dataset_feature_roles_are_disjoint():
    cfg = DebiasConfig(n_train=100, n_test=100, n_features=64, n_task=8, n_spurious=8, n_proxy=8, seed=13)
    dataset = generate_debias_dataset(cfg)
    assert dataset.x_train.shape == (100, 64)
    assert dataset.is_task.sum() == 8
    assert dataset.is_spurious.sum() == 8
    assert dataset.is_proxy.sum() == 8
    assert not (dataset.is_task & dataset.is_spurious).any()
    assert not (dataset.is_task & dataset.is_proxy).any()
    assert not (dataset.is_spurious & dataset.is_proxy).any()


def test_debias_replicate_outputs_evaluation_rows():
    cfg = DebiasConfig(n_train=200, n_test=200, n_features=80, n_task=8, n_spurious=8, n_proxy=8, seed=17)
    features, evaluation = run_debias_replicate(cfg, replicate=0)
    assert features.shape[0] == 80
    assert {"e_bh_pcal", "oracle_spurious", "none"}.issubset(set(evaluation["method"]))
    assert evaluation["worst_group_acc"].between(0, 1).all()
