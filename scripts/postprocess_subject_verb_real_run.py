"""Public release note for real-run postprocessing.

The public repository ships the canonical cached CSVs and analysis scripts.
Run ``scripts/analyze_ablation_cache.py``, ``scripts/analyze_circuit_cache.py``,
and ``scripts/analyze_real_subject_verb_reliability.py`` directly on those
caches. Internal returned-output staging code is not included.
"""

from __future__ import annotations


def main() -> None:
    raise SystemExit("Use the public analysis scripts on the checked-in caches.")


if __name__ == "__main__":
    main()
