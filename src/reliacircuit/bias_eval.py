from __future__ import annotations

import pandas as pd


def normalize_prediction_cache(
    predictions: pd.DataFrame,
    labels: pd.DataFrame | None = None,
    *,
    example_col: str = "example_id",
    method_col: str = "method",
    prediction_col: str = "predicted_label",
    target_col: str = "target_label",
    protected_col: str = "protected_label",
) -> pd.DataFrame:
    required = {example_col, method_col, prediction_col}
    missing = required - set(predictions.columns)
    if missing:
        raise ValueError(f"prediction cache missing columns: {sorted(missing)}")
    work = predictions.copy()
    if labels is not None:
        available = [c for c in [target_col, protected_col, "group_id", "split"] if c in labels.columns]
        if target_col not in labels.columns or protected_col not in labels.columns:
            raise ValueError(f"labels must contain {target_col!r} and {protected_col!r}")
        merge_cols = [c for c in available if c not in work.columns]
        if merge_cols:
            label_cols = [example_col, *merge_cols]
            work = work.merge(labels.loc[:, label_cols].drop_duplicates(example_col), on=example_col, how="left")
    missing_labels = {target_col, protected_col} - set(work.columns)
    if missing_labels:
        raise ValueError(
            f"prediction cache lacks labels {sorted(missing_labels)}; pass labels/prompts for merging"
        )
    if work[target_col].isna().any() or work[protected_col].isna().any():
        raise ValueError("some predictions could not be matched to target/protected labels")
    if "group_id" not in work.columns:
        work["group_id"] = work[target_col].astype(str) + "::" + work[protected_col].astype(str)
    work["correct"] = work[prediction_col].astype(str) == work[target_col].astype(str)
    return work


def group_metrics(
    normalized: pd.DataFrame,
    *,
    method_col: str = "method",
    target_col: str = "target_label",
    protected_col: str = "protected_label",
) -> pd.DataFrame:
    rows = []
    for keys, group in normalized.groupby([method_col, target_col, protected_col, "group_id"], sort=True):
        method, target, protected, group_id = keys
        rows.append(
            {
                "method": method,
                "target_label": target,
                "protected_label": protected,
                "group_id": group_id,
                "n": int(group.shape[0]),
                "accuracy": float(group["correct"].mean()),
            }
        )
    return pd.DataFrame(rows)


def method_summary(
    normalized: pd.DataFrame,
    groups: pd.DataFrame | None = None,
    *,
    method_col: str = "method",
    baseline_method: str = "clean",
) -> pd.DataFrame:
    if groups is None:
        groups = group_metrics(normalized, method_col=method_col)
    rows = []
    for method, group in normalized.groupby(method_col, sort=True):
        method_groups = groups[groups["method"] == method]
        worst = float(method_groups["accuracy"].min()) if not method_groups.empty else float("nan")
        best = float(method_groups["accuracy"].max()) if not method_groups.empty else float("nan")
        rows.append(
            {
                "method": method,
                "n": int(group.shape[0]),
                "overall_acc": float(group["correct"].mean()),
                "worst_group_acc": worst,
                "best_group_acc": best,
                "group_gap": best - worst,
                "mean_group_acc": float(method_groups["accuracy"].mean()) if not method_groups.empty else float("nan"),
                "n_groups": int(method_groups.shape[0]),
            }
        )
    summary = pd.DataFrame(rows)
    if baseline_method in set(summary["method"]):
        baseline = summary.set_index("method").loc[baseline_method]
        summary["delta_overall_acc_vs_baseline"] = summary["overall_acc"] - float(baseline["overall_acc"])
        summary["delta_worst_group_acc_vs_baseline"] = summary["worst_group_acc"] - float(
            baseline["worst_group_acc"]
        )
    return summary


def attach_removal_metadata(summary: pd.DataFrame, metadata: pd.DataFrame | None) -> pd.DataFrame:
    if metadata is None:
        return summary
    if "method" not in metadata.columns:
        raise ValueError("removal metadata must contain method")
    keep = [c for c in metadata.columns if c != "method"]
    return summary.merge(metadata.loc[:, ["method", *keep]].drop_duplicates("method"), on="method", how="left")
