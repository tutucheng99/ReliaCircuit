"""Public release note for layer-scan GPU planning.

The internal pod-specific execution planner was removed from this anonymous
release. The fixed layer protocol is preserved in
``configs/subject_verb_layer_scan_protocol.json`` and the generic GPU cache
recipe is documented in ``docs/gpu_cache_generation.md``.
"""

from __future__ import annotations


def main() -> None:
    raise SystemExit("Use docs/gpu_cache_generation.md for the public GPU-stage recipe.")


if __name__ == "__main__":
    main()
