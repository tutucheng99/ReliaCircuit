import numpy as np

from reliacircuit.fdr import bh, by_bh, e_bh, p_to_e_value


def test_bh_rejects_prefix_of_sorted_p_values():
    p = np.array([0.001, 0.02, 0.03, 0.6])
    reject = bh(p, q=0.05)
    assert reject.tolist() == [True, True, True, False]


def test_by_is_no_less_conservative_than_bh():
    p = np.array([0.001, 0.02, 0.03, 0.6])
    assert np.sum(by_bh(p, q=0.05)) <= np.sum(bh(p, q=0.05))


def test_p_to_e_and_e_bh_can_reject_strong_signal():
    p = np.array([1e-12, 0.2, 0.7])
    e = p_to_e_value(p, gamma=0.5)
    reject = e_bh(e, q=0.1)
    assert reject.tolist() == [True, False, False]
