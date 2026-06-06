from __future__ import annotations

from pathlib import Path
import shutil

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "figure_drafts"
PAPER_FIG = ROOT / "paper" / "figures"

# Shared semantic palette across final figures.
EBH = "#0072B2"       # RELIACIRCUIT / e-BH
BASE = "#D55E00"      # score, p-value, BH/BY baselines
PVAL = "#CC79A7"      # uncorrected p-value baseline when shown beside scores
NEUTRAL = "#6B7280"   # boundary / negative / notes
LIGHT = "#F4F6F8"
DARK = "#111827"
BORDER = "#9CA3AF"


def setup_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "Times", "Nimbus Roman", "DejaVu Serif"],
            "mathtext.fontset": "stix",
            "font.size": 8.0,
            "axes.titlesize": 8.4,
            "axes.labelsize": 8.0,
            "xtick.labelsize": 7.4,
            "ytick.labelsize": 7.4,
            "legend.fontsize": 7.1,
            "figure.titlesize": 9.4,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "axes.linewidth": 0.65,
        }
    )


def save_outputs(fig: plt.Figure, stem: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    PAPER_FIG.mkdir(parents=True, exist_ok=True)
    pdf = OUT / f"{stem}.pdf"
    fig.savefig(pdf, bbox_inches="tight", pad_inches=0.018)
    fig.savefig(OUT / f"{stem}.svg", bbox_inches="tight", pad_inches=0.018)
    fig.savefig(OUT / f"{stem}.png", bbox_inches="tight", pad_inches=0.018, dpi=320)
    shutil.copyfile(pdf, PAPER_FIG / f"{stem}.pdf")


def clean_axis(ax: plt.Axes, grid_axis: str | None = "x") -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#D1D5DB")
    ax.spines["bottom"].set_color("#D1D5DB")
    ax.tick_params(colors="#374151", width=0.55, length=2.4)
    if grid_axis:
        ax.grid(axis=grid_axis, color="#E5E7EB", linewidth=0.55)
        ax.set_axisbelow(True)


def panel_label(ax: plt.Axes, label: str) -> None:
    ax.text(
        -0.08,
        1.05,
        label,
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=9.0,
        fontweight="bold",
        color=DARK,
    )


def high_score_decoy_rows() -> pd.DataFrame:
    tab18 = pd.read_csv(ROOT / "results" / "paper_assets" / "table_18_second_round_decoy_bh_by.csv")
    return tab18[tab18["decoy_scheme"] == "high_score_signflip"].copy()


def draw_contract_panel(ax: plt.Axes) -> None:
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    rows = [
        ("Stopping rule", "manual $k$", "$q$ controls\ncount"),
        ("Error contract", "none", "FDR target"),
        ("Effect report", "score only", "$\\hat\\tau$ + CI"),
    ]
    ax.text(0.03, 0.93, "score threshold", color=BASE, fontweight="bold", fontsize=6.8)
    ax.text(0.52, 0.93, "RELIACIRCUIT", color=EBH, fontweight="bold", fontsize=6.8)
    for idx, (name, old, new) in enumerate(rows):
        y = 0.74 - idx * 0.22
        face = "white" if idx % 2 == 0 else "#F8FAFC"
        ax.add_patch(Rectangle((0.00, y - 0.105), 1.00, 0.155, facecolor=face, edgecolor="#DDE3EA", linewidth=0.55))
        ax.text(0.02, y + 0.017, name, ha="left", va="center", fontweight="bold", fontsize=6.7, color=DARK)
        ax.text(0.05, y - 0.047, old, ha="left", va="center", fontsize=6.6, color="#374151")
        ax.text(0.47, y - 0.047, r"$\rightarrow$", ha="center", va="center", fontsize=6.8, color=NEUTRAL)
        ax.text(0.55, y - 0.047, new, ha="left", va="center", fontsize=6.45, color=DARK, linespacing=0.86)


def draw_fig1() -> None:
    decoy18 = high_score_decoy_rows()
    old_decoy = pd.read_csv(ROOT / "results" / "real_subject_verb_reliability" / "decoy_reliability_summary.csv")
    layer = pd.read_csv(ROOT / "results" / "real_subject_verb_reliability" / "layer_scan_summary.csv")

    def row(method: str) -> pd.Series:
        return decoy18[(decoy18["layer"] == "L16") & (decoy18["method"] == method)].iloc[0]

    ebh = row("e_bh_pcal")
    top = row("top_score_matched_e_bh_pcal")
    pval = row("p_lt_q")
    fixed = old_decoy[(old_decoy["layer"] == "L16") & (old_decoy["method"] == "top_score_fixed_k_256")].iloc[0]

    panel_a = [
        ("e-BH\n(auto $q=0.1$)", ebh["known_null_fdp_mean"], f"0/{ebh['discoveries_mean']:.0f} decoys"),
        ("score-matched\ntop-$k$", top["known_null_fdp_mean"], f"{top['known_null_decoys_selected_mean']:.0f}/{top['discoveries_mean']:.0f} decoys"),
        ("uncorrected\n$p<q$", pval["known_null_fdp_mean"], f"FDP {pval['known_null_fdp_mean']:.3f}"),
        ("fixed\ntop-256", fixed["known_null_fdp_mean"], "256/256 decoys"),
    ]

    l16 = layer[(layer["layer"] == "L16") & (layer["method"].isin(["e_bh_pcal", "top_score_k_e_bh_pcal"]))].set_index("method")
    fig = plt.figure(figsize=(7.16, 2.72))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.42, 1.18, 1.02], wspace=0.38)
    fig.subplots_adjust(top=0.87, bottom=0.13)

    ax_a = fig.add_subplot(gs[0, 0])
    labels = [x[0] for x in panel_a]
    vals = [float(x[1]) for x in panel_a]
    texts = [x[2] for x in panel_a]
    y = np.arange(len(labels))
    colors = [EBH, BASE, BASE, NEUTRAL]
    bars = ax_a.barh(y, vals, color=colors, height=0.52, edgecolor="white", linewidth=0.8)
    for idx, bar in enumerate(bars):
        if idx in (1, 2):
            bar.set_hatch("//" if idx == 1 else "\\\\")
    ax_a.set_yticks(y, labels)
    ax_a.invert_yaxis()
    ax_a.set_xlim(0, 1.24)
    ax_a.set_xticks([0.00, 0.25, 0.50, 0.75, 1.00])
    ax_a.set_xlabel("decoy-FDP")
    ax_a.set_title("L16 high-score null-decoy stress", loc="left", pad=6)
    panel_label(ax_a, "A")
    clean_axis(ax_a, "x")
    ax_a.axvline(0.1, color=DARK, linestyle=(0, (3, 2)), linewidth=0.7)
    ax_a.set_ylim(len(labels) - 0.5, -0.82)
    ax_a.text(
        0.10,
        -0.62,
        "$q=0.1$",
        ha="center",
        va="bottom",
        fontsize=7.2,
        color=DARK,
        bbox=dict(facecolor="white", edgecolor="none", pad=0.6),
        clip_on=False,
    )
    for i, (v, text) in enumerate(zip(vals, texts)):
        if v == 0:
            x_text = 0.185
        elif v >= 0.90:
            x_text = 1.035
        else:
            x_text = v + 0.055
        ax_a.text(
            x_text,
            i,
            text,
            va="center",
            ha="left",
            fontsize=6.75,
            color=DARK,
            bbox=dict(facecolor="white", edgecolor="none", pad=0.45),
            clip_on=False,
        )

    ax_b = fig.add_subplot(gs[0, 1])
    ax_b.set_title("What changes", loc="left", pad=6)
    panel_label(ax_b, "B")
    draw_contract_panel(ax_b)

    ax_c = fig.add_subplot(gs[0, 2])
    metrics = ["Completeness\n(unc.)", "Sel./full\ncorr."]
    ebh_vals = [
        float(l16.loc["e_bh_pcal", "completeness_r2"]),
        float(l16.loc["e_bh_pcal", "selected_full_corr"]),
    ]
    top_vals = [
        float(l16.loc["top_score_k_e_bh_pcal", "completeness_r2"]),
        float(l16.loc["top_score_k_e_bh_pcal", "selected_full_corr"]),
    ]
    x = np.arange(2)
    w = 0.32
    ax_c.bar(x - w / 2, ebh_vals, w, color=EBH, label="e-BH")
    ax_c.bar(x + w / 2, top_vals, w, color=BASE, hatch="//", label="top-$k$")
    ax_c.set_title("Reconstruction is comparable", loc="left", pad=6)
    panel_label(ax_c, "C")
    ax_c.set_xticks(x, metrics)
    ax_c.set_ylim(0.70, 1.08)
    ax_c.set_ylabel("value")
    clean_axis(ax_c, None)
    ax_c.legend(frameon=False, loc="upper left", bbox_to_anchor=(-0.03, 1.02), ncol=2, handlelength=1.0, columnspacing=0.8)
    for xi, val in zip(x - w / 2, ebh_vals):
        ax_c.text(xi, val + 0.009, f"{val:.3f}", ha="center", va="bottom", fontsize=6.8)
    for xi, val in zip(x + w / 2, top_vals):
        ax_c.text(xi, val + 0.009, f"{val:.3f}", ha="center", va="bottom", fontsize=6.8)
    save_outputs(fig, "fig1_old_vs_reliacircuit_final")
    plt.close(fig)


def draw_fig3() -> None:
    decoy = high_score_decoy_rows()
    layers = ["L8", "L12", "L16", "L20"]
    methods = [
        ("e_bh_pcal", "e-BH", EBH, ""),
        ("top_score_matched_e_bh_pcal", "score-matched top-$k$", BASE, "//"),
        ("p_lt_q", "$p<q$", PVAL, "xx"),
    ]
    fig, ax = plt.subplots(figsize=(3.48, 2.90))
    fig.subplots_adjust(left=0.16, right=0.98, bottom=0.15, top=0.70)
    x = np.arange(len(layers))
    width = 0.23
    for j, (method, label, color, hatch) in enumerate(methods):
        vals = [
            float(decoy[(decoy["layer"] == layer) & (decoy["method"] == method)]["known_null_decoys_selected_mean"].iloc[0])
            for layer in layers
        ]
        bars = ax.bar(x + (j - 1) * width, vals, width, color=color, label=label, hatch=hatch, edgecolor="white", linewidth=0.65)
        if method == "e_bh_pcal":
            for i, bar in enumerate(bars):
                ax.text(bar.get_x() + bar.get_width() / 2, 0.62, "0", ha="center", va="bottom", fontsize=7.0, color=EBH)
    ax.set_xticks(x, layers)
    ax.set_ylabel("known-null decoys selected")
    ax.set_ylim(0, 34)
    fig.text(0.16, 0.985, "Screen-attractive null decoys across layers", ha="left", va="top", fontsize=8.4, color=DARK)
    clean_axis(ax, None)
    handles, legend_labels = ax.get_legend_handles_labels()
    fig.legend(
        handles,
        legend_labels,
        frameon=False,
        loc="upper left",
        bbox_to_anchor=(0.16, 0.925),
        ncol=2,
        handlelength=1.1,
        columnspacing=0.9,
        labelspacing=0.45,
        borderaxespad=0.0,
    )
    save_outputs(fig, "fig3_decoy_layers_final")
    plt.close(fig)


def main() -> None:
    setup_style()
    draw_fig1()
    draw_fig3()
    print("wrote final matplotlib figures to results/figure_drafts and paper/figures")


if __name__ == "__main__":
    main()
