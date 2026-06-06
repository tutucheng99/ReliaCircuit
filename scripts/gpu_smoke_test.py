from __future__ import annotations

import argparse
import importlib
import importlib.metadata
import json
import os
import platform
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    args = parse_args()
    report: dict[str, Any] = {
        "timestamp_unix": time.time(),
        "platform": platform.platform(),
        "python": sys.version,
        "packages": package_versions(
            [
                "torch",
                "transformers",
                "accelerate",
                "safetensors",
                "huggingface-hub",
                "sae-lens",
                "transformer-lens",
            ]
        ),
        "args": jsonable_args(args),
    }

    torch = import_optional("torch")
    if torch is None:
        report["torch_error"] = "torch is not importable"
        write_report(args.output, report)
        raise SystemExit("torch is not importable")

    report["cuda"] = cuda_report(torch)
    device = choose_device(torch, args.device)
    report["chosen_device"] = str(device)

    if not args.skip_model_load:
        report["model"] = load_model_smoke(args, torch, device)
    else:
        report["model"] = {"skipped": True}

    if not args.skip_sae:
        report["sae"] = load_sae_smoke(args, device)
    else:
        report["sae"] = {"skipped": True}

    write_report(args.output, report)
    print(json.dumps(report, indent=2))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="RunPod/Gemma/SAELens smoke test.")
    parser.add_argument("--model-id", default="google/gemma-2-2b")
    parser.add_argument("--prompt", default="The key to the cabinets")
    parser.add_argument("--max-new-tokens", type=int, default=1)
    parser.add_argument("--dtype", choices=["auto", "bfloat16", "float16", "float32"], default="auto")
    parser.add_argument("--device", choices=["auto", "cuda", "cpu"], default="auto")
    parser.add_argument("--cache-dir", type=Path, default=None)
    parser.add_argument("--skip-model-load", action="store_true")
    parser.add_argument("--skip-sae", action="store_true")
    parser.add_argument("--sae-release", default="gemma-scope-2b-pt-res-canonical")
    parser.add_argument("--sae-id", default="layer_20/width_16k/canonical")
    parser.add_argument("--output", type=Path, default=ROOT / "results" / "gpu_smoke" / "smoke_report.json")
    return parser.parse_args()


def import_optional(module: str):
    try:
        return importlib.import_module(module)
    except Exception:
        return None


def package_versions(names: list[str]) -> dict[str, str | None]:
    versions: dict[str, str | None] = {}
    for name in names:
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            versions[name] = None
    return versions


def cuda_report(torch) -> dict[str, Any]:
    available = bool(torch.cuda.is_available())
    info: dict[str, Any] = {
        "available": available,
        "device_count": int(torch.cuda.device_count()) if available else 0,
    }
    if available:
        devices = []
        for i in range(torch.cuda.device_count()):
            props = torch.cuda.get_device_properties(i)
            devices.append(
                {
                    "index": i,
                    "name": torch.cuda.get_device_name(i),
                    "total_memory_gb": round(props.total_memory / (1024**3), 2),
                    "capability": list(torch.cuda.get_device_capability(i)),
                }
            )
        info["devices"] = devices
        info["torch_cuda_version"] = torch.version.cuda
    return info


def choose_device(torch, requested: str):
    if requested == "cpu":
        return torch.device("cpu")
    if requested == "cuda":
        if not torch.cuda.is_available():
            raise SystemExit("--device cuda requested but CUDA is not available")
        return torch.device("cuda")
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def dtype_from_arg(torch, dtype: str, device) -> Any:
    if dtype == "float32" or str(device) == "cpu":
        return torch.float32
    if dtype == "float16":
        return torch.float16
    if dtype == "bfloat16":
        return torch.bfloat16
    return torch.bfloat16 if torch.cuda.is_available() else torch.float32


def load_model_smoke(args: argparse.Namespace, torch, device) -> dict[str, Any]:
    transformers = import_optional("transformers")
    if transformers is None:
        return {"ok": False, "error": "transformers is not importable"}

    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
    kwargs = {}
    if args.cache_dir is not None:
        kwargs["cache_dir"] = str(args.cache_dir)
    if token:
        kwargs["token"] = token

    started = time.time()
    tokenizer = transformers.AutoTokenizer.from_pretrained(args.model_id, **kwargs)
    dtype = dtype_from_arg(torch, args.dtype, device)
    model_kwargs = dict(kwargs)
    model_kwargs["torch_dtype"] = dtype
    if str(device) == "cuda":
        model_kwargs["device_map"] = "auto"
    model = transformers.AutoModelForCausalLM.from_pretrained(args.model_id, **model_kwargs)
    if str(device) == "cpu":
        model.to(device)
    model.eval()

    inputs = tokenizer(args.prompt, return_tensors="pt")
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=args.max_new_tokens)
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return {
        "ok": True,
        "model_id": args.model_id,
        "device": str(model.device),
        "dtype": str(dtype),
        "elapsed_sec": round(time.time() - started, 3),
        "input_tokens": int(inputs["input_ids"].shape[-1]),
        "decoded_preview": text[:200],
    }


def load_sae_smoke(args: argparse.Namespace, device) -> dict[str, Any]:
    started = time.time()
    try:
        from sae_lens import SAE
    except Exception as exc:
        return {"ok": False, "error": f"sae_lens import failed: {exc}"}

    try:
        loaded = SAE.from_pretrained(
            release=args.sae_release,
            sae_id=args.sae_id,
            device=str(device),
        )
    except Exception as exc:
        return {
            "ok": False,
            "release": args.sae_release,
            "sae_id": args.sae_id,
            "error": repr(exc),
        }

    sae = loaded[0] if isinstance(loaded, tuple) else loaded
    cfg = loaded[1] if isinstance(loaded, tuple) and len(loaded) > 1 else getattr(sae, "cfg", None)
    return {
        "ok": True,
        "release": args.sae_release,
        "sae_id": args.sae_id,
        "elapsed_sec": round(time.time() - started, 3),
        "sae_class": sae.__class__.__name__,
        "cfg": cfg_to_report(cfg),
    }


def cfg_to_report(cfg: Any) -> dict[str, Any]:
    if cfg is None:
        return {}
    keys = ["d_in", "d_sae", "hook_name", "hook_layer", "model_name", "architecture"]
    out = {}
    for key in keys:
        if isinstance(cfg, dict) and key in cfg:
            out[key] = cfg[key]
        elif hasattr(cfg, key):
            value = getattr(cfg, key)
            if isinstance(value, (str, int, float, bool, type(None))):
                out[key] = value
            else:
                out[key] = str(value)
    return out


def write_report(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")


def jsonable_args(args: argparse.Namespace) -> dict[str, Any]:
    out = {}
    for key, value in vars(args).items():
        out[key] = str(value) if isinstance(value, Path) else value
    return out


if __name__ == "__main__":
    main()
