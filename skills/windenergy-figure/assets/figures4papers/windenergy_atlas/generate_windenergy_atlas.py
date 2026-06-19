#!/usr/bin/env python3
"""Generate the windenergy figure atlas from synthetic demonstration data."""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
ATLAS = ROOT / "chart-atlas"
GALLERY = ROOT / "gallery"
FORMATS = ("png", "svg", "pdf")

BLUE = "#2F6B9A"
TEAL = "#2A9D8F"
ORANGE = "#E76F51"
GOLD = "#E9C46A"
GREY = "#4D4D4D"
LIGHT = "#F3F6F7"


def setup() -> None:
    ATLAS.mkdir(parents=True, exist_ok=True)
    GALLERY.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update(
        {
            "figure.dpi": 140,
            "savefig.dpi": 220,
            "font.family": "serif",
            "font.serif": ["Times New Roman", "DejaVu Serif", "serif"],
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.labelsize": 9,
            "axes.titlesize": 10,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "legend.fontsize": 8,
        }
    )


def save(fig: plt.Figure, slug: str, gallery: bool = False) -> None:
    target = GALLERY if gallery else ATLAS
    for fmt in FORMATS:
        fig.savefig(target / f"{slug}.{fmt}", bbox_inches="tight")
    plt.close(fig)


def wind_rose() -> None:
    rng = np.random.default_rng(7)
    dirs = np.deg2rad(np.arange(0, 360, 15))
    speeds = np.clip(rng.normal(8, 2, len(dirs)) + 2 * np.sin(dirs - 0.5), 2, 15)
    freq = 0.05 + 0.12 * (speeds - speeds.min()) / (speeds.max() - speeds.min())
    fig = plt.figure(figsize=(4.2, 4.2))
    ax = fig.add_subplot(111, polar=True)
    ax.bar(dirs, freq, width=np.deg2rad(12), color=TEAL, edgecolor="white", linewidth=0.6)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_title("Wind direction exposure")
    ax.set_yticklabels([])
    save(fig, "atlas-01-wind-rose")
    fig = plt.figure(figsize=(4.2, 4.2))
    ax = fig.add_subplot(111, polar=True)
    ax.bar(dirs, freq, width=np.deg2rad(12), color=TEAL, edgecolor="white", linewidth=0.6)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_title("Wind direction exposure")
    ax.set_yticklabels([])
    save(fig, "atlas-01-wind-rose", gallery=True)


def power_curve() -> None:
    wind = np.linspace(0, 25, 160)
    rated = 1 / (1 + np.exp(-0.9 * (wind - 9))) * 3.2
    power = np.where(wind < 3, 0, np.where(wind < 12, rated, np.where(wind < 22, 3.2, 0)))
    fig, ax = plt.subplots(figsize=(5.2, 3.4))
    ax.plot(wind, power, color=BLUE, linewidth=2)
    ax.axvspan(0, 3, color=LIGHT)
    ax.axvspan(12, 22, color="#EAF4F2")
    ax.text(1.5, 2.7, "cut-in", ha="center", fontsize=8, color=GREY)
    ax.text(17, 2.7, "rated", ha="center", fontsize=8, color=GREY)
    ax.set_xlabel("Wind speed (m/s)")
    ax.set_ylabel("Power (MW)")
    ax.set_title("Power curve defines operating regimes")
    save(fig, "atlas-02-power-curve")


def forecast_series() -> None:
    t = np.arange(72)
    actual = 1.8 + 0.7 * np.sin(t / 8) + 0.25 * np.sin(t / 2.2)
    forecast = actual + 0.18 * np.sin(t / 5 + 1.2)
    lower = forecast - 0.32 - 0.08 * np.cos(t / 6)
    upper = forecast + 0.32 + 0.08 * np.cos(t / 6)
    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    ax.fill_between(t, lower, upper, color=GOLD, alpha=0.35, label="80% interval")
    ax.plot(t, actual, color=GREY, linewidth=1.8, label="Actual")
    ax.plot(t, forecast, color=ORANGE, linewidth=1.6, label="Forecast")
    ax.set_xlabel("Hour")
    ax.set_ylabel("Power (MW)")
    ax.set_title("Forecast tracks ramp events with interval context")
    ax.legend(frameon=False, ncol=3, loc="upper center")
    save(fig, "atlas-03-forecast-timeseries")


def error_distribution() -> None:
    rng = np.random.default_rng(11)
    horizons = [1, 6, 12, 24]
    data = [rng.normal(0, 0.08 + h / 180, 240) for h in horizons]
    fig, ax = plt.subplots(figsize=(5.2, 3.4))
    parts = ax.violinplot(data, showmeans=True, showextrema=False)
    for body in parts["bodies"]:
        body.set_facecolor(BLUE)
        body.set_edgecolor("white")
        body.set_alpha(0.65)
    parts["cmeans"].set_color(ORANGE)
    ax.axhline(0, color=GREY, linewidth=0.8)
    ax.set_xticks(range(1, len(horizons) + 1), [f"{h}h" for h in horizons])
    ax.set_ylabel("Forecast error (MW)")
    ax.set_title("Error spread increases with horizon")
    save(fig, "atlas-04-error-distribution")


def reliability() -> None:
    nominal = np.array([0.5, 0.6, 0.7, 0.8, 0.9])
    observed = np.array([0.47, 0.58, 0.68, 0.76, 0.86])
    fig, ax = plt.subplots(figsize=(4.2, 3.8))
    ax.plot(nominal, nominal, color=GREY, linewidth=1, linestyle="--", label="Ideal")
    ax.plot(nominal, observed, marker="o", color=TEAL, linewidth=1.8, label="Observed")
    ax.fill_between(nominal, observed - 0.03, observed + 0.03, color=TEAL, alpha=0.18)
    ax.set_xlabel("Nominal coverage")
    ax.set_ylabel("Observed coverage")
    ax.set_title("Prediction intervals are slightly under-covered")
    ax.legend(frameon=False)
    save(fig, "atlas-05-interval-reliability")


def model_comparison() -> None:
    names = ["Persistence", "GBR", "LSTM", "Transformer", "Hybrid"]
    mae = np.array([0.42, 0.34, 0.31, 0.29, 0.27])
    ci = np.array([0.03, 0.025, 0.022, 0.021, 0.018])
    y = np.arange(len(names))
    fig, ax = plt.subplots(figsize=(5.4, 3.6))
    ax.barh(y, mae, xerr=ci, color=[GREY, BLUE, BLUE, TEAL, ORANGE], alpha=0.85)
    ax.set_yticks(y, names)
    ax.invert_yaxis()
    ax.set_xlabel("MAE (MW)")
    ax.set_title("Model comparison reports uncertainty")
    save(fig, "atlas-06-model-comparison-ci")


def ablation_heatmap() -> None:
    rows = ["NWP", "SCADA", "Calendar", "Terrain", "Wake"]
    cols = ["1h", "6h", "12h", "24h"]
    values = np.array(
        [
            [0.08, 0.14, 0.18, 0.22],
            [0.18, 0.15, 0.12, 0.08],
            [0.03, 0.05, 0.07, 0.08],
            [0.02, 0.03, 0.04, 0.05],
            [0.04, 0.05, 0.06, 0.07],
        ]
    )
    fig, ax = plt.subplots(figsize=(4.8, 3.5))
    im = ax.imshow(values, cmap="YlGnBu", aspect="auto")
    ax.set_xticks(range(len(cols)), cols)
    ax.set_yticks(range(len(rows)), rows)
    for i in range(values.shape[0]):
        for j in range(values.shape[1]):
            ax.text(j, i, f"{values[i, j]:.2f}", ha="center", va="center", fontsize=8)
    fig.colorbar(im, ax=ax, shrink=0.78, label="MAE increase")
    ax.set_title("Ablation links feature groups to horizon")
    save(fig, "atlas-07-ablation-heatmap")


def wake_layout() -> None:
    x = np.array([0, 1.8, 3.6, 0.4, 2.2, 4.0])
    y = np.array([0, 0.3, 0.1, 1.6, 1.8, 1.5])
    fig, ax = plt.subplots(figsize=(5.4, 3.6))
    for xi, yi in zip(x, y):
        ax.add_patch(plt.Circle((xi, yi), 0.12, color=BLUE))
        ax.arrow(xi + 0.12, yi, 0.9, 0.08, width=0.015, head_width=0.08, color=GOLD, alpha=0.55)
    ax.scatter(x, y, s=90, color=BLUE, edgecolor="white", linewidth=0.8, zorder=3)
    for idx, (xi, yi) in enumerate(zip(x, y), start=1):
        ax.text(xi, yi + 0.22, f"T{idx}", ha="center", fontsize=8)
    ax.set_xlim(-0.4, 5.2)
    ax.set_ylim(-0.4, 2.4)
    ax.set_aspect("equal")
    ax.set_xlabel("Downwind distance (km)")
    ax.set_ylabel("Crosswind distance (km)")
    ax.set_title("Wake schematic exposes layout dependency")
    save(fig, "atlas-08-wake-layout")


def storage_market() -> None:
    t = np.arange(24)
    price = 45 + 18 * np.sin((t - 7) / 24 * 2 * math.pi) + 9 * np.sin(t / 24 * 4 * math.pi)
    dispatch = np.clip((price - price.mean()) / 18, -1, 1)
    soc = 50 + np.cumsum(-dispatch) * 2.2
    fig, ax1 = plt.subplots(figsize=(6.0, 3.3))
    ax1.bar(t, dispatch, color=np.where(dispatch >= 0, TEAL, ORANGE), alpha=0.75, label="Dispatch")
    ax1.set_ylabel("Battery dispatch")
    ax1.set_xlabel("Hour")
    ax2 = ax1.twinx()
    ax2.plot(t, price, color=GREY, linewidth=1.5, label="Price")
    ax2.plot(t, soc, color=BLUE, linewidth=1.5, label="State of charge")
    ax2.set_ylabel("Price or state")
    lines, labels = [], []
    for ax in [ax1, ax2]:
        h, l = ax.get_legend_handles_labels()
        lines += h
        labels += l
    ax1.legend(lines, labels, frameon=False, ncol=3, loc="upper center")
    ax1.set_title("Storage dispatch follows market signal")
    save(fig, "atlas-09-storage-market")


def mechanism_flow() -> None:
    fig, ax = plt.subplots(figsize=(6.3, 3.2))
    ax.axis("off")
    boxes = [
        (0.08, 0.55, "SCADA and NWP"),
        (0.31, 0.55, "Quality filters"),
        (0.54, 0.55, "Forecast model"),
        (0.77, 0.55, "Grid decision"),
        (0.31, 0.18, "Leakage audit"),
        (0.54, 0.18, "Uncertainty check"),
    ]
    for x, y, label in boxes:
        rect = plt.Rectangle((x, y), 0.16, 0.16, transform=ax.transAxes, facecolor=LIGHT, edgecolor=BLUE, linewidth=1.1)
        ax.add_patch(rect)
        ax.text(x + 0.08, y + 0.08, label, ha="center", va="center", transform=ax.transAxes, fontsize=8)
    arrows = [((0.24, 0.63), (0.31, 0.63)), ((0.47, 0.63), (0.54, 0.63)), ((0.70, 0.63), (0.77, 0.63)), ((0.39, 0.55), (0.39, 0.34)), ((0.62, 0.55), (0.62, 0.34))]
    for start, end in arrows:
        ax.annotate("", xy=end, xytext=start, xycoords=ax.transAxes, arrowprops={"arrowstyle": "-|>", "color": GREY, "lw": 1})
    ax.set_title("Mechanism figure separates data, model, and decision")
    save(fig, "atlas-10-mechanism-flow")


def write_qa() -> None:
    text = """# Windenergy atlas QA

Data status: synthetic demonstration data.

Generated formats: PNG, SVG, and PDF for every atlas figure.

Use rule: replace synthetic data with user-provided evidence before manuscript use.

Visual checks:

- All charts use a restrained, colorblind-aware palette.
- Text sizes are intended for manuscript inspection.
- Dual-axis use appears only in the storage-market example and must be justified in a real manuscript.
- Low-support claims require sample counts or uncertainty before strong wording.
"""
    (ROOT / "figures4papers" / "windenergy_atlas" / "atlas_qa.md").write_text(text, encoding="utf-8")


def main() -> None:
    setup()
    wind_rose()
    power_curve()
    forecast_series()
    error_distribution()
    reliability()
    model_comparison()
    ablation_heatmap()
    wake_layout()
    storage_market()
    mechanism_flow()
    write_qa()


if __name__ == "__main__":
    main()
