#!/usr/bin/env python3
"""Generate the conditional heteroclinic-connection schematic."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Rectangle


plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42


INK = "#202124"
BLUE = "#2F6F9F"
ORANGE = "#C65D2E"
GRAY = "#74787C"
GREEN = "#6E8B5B"


def arrow_on_curve(ax, x, y, idx, color):
    ax.add_patch(
        FancyArrowPatch(
            (x[idx - 1], y[idx - 1]),
            (x[idx + 1], y[idx + 1]),
            arrowstyle="-|>",
            mutation_scale=10,
            linewidth=0,
            color=color,
        )
    )


def draw(output: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.35, 2.9))
    ax.set_xlim(0, 10)
    ax.set_ylim(-1.35, 1.45)
    ax.axis("off")

    # Coordinate arrows identify the two-dimensional projection; no metric is
    # implied by the drawing.
    ax.annotate(
        "",
        xy=(9.65, -1.22),
        xytext=(0.32, -1.22),
        arrowprops=dict(arrowstyle="->", linewidth=0.8, color=INK),
    )
    ax.annotate(
        "",
        xy=(0.32, 1.28),
        xytext=(0.32, -1.22),
        arrowprops=dict(arrowstyle="->", linewidth=0.8, color=INK),
    )
    ax.text(9.74, -1.22, r"$-r$", ha="left", va="center", fontsize=8.5)
    ax.text(0.32, 1.34, r"$w$", ha="center", va="bottom", fontsize=8.5)

    # The central rectangle is only the projected image of the fold chart.
    ax.add_patch(
        Rectangle(
            (2.95, -1.0),
            4.15,
            2.05,
            facecolor="#EFEFEA",
            edgecolor="#B3B3AA",
            linewidth=0.9,
            zorder=0,
        )
    )
    ax.text(
        5.025,
        1.15,
        "fold neighborhood (the equations agree)",
        ha="center",
        va="bottom",
        fontsize=8.2,
        color=GRAY,
    )

    # Representative attracting and repelling slow branches.
    xa = np.linspace(1.2, 4.8, 160)
    ya = 0.42 - 0.11 * (xa - 1.2) - 0.13 * np.exp(-((xa - 4.7) / 0.55) ** 2)
    xr = np.linspace(5.15, 8.55, 160)
    yr = -0.13 + 0.18 * (xr - 5.15) / 3.4
    ax.plot(xa, ya, color=GREEN, linewidth=1.2, linestyle=(0, (5, 3)), zorder=1)
    ax.plot(xr, yr, color=GREEN, linewidth=1.2, linestyle=(0, (2, 2)), zorder=1)
    ax.text(2.45, 0.82, "attracting slow branch", color=GREEN, fontsize=8.1, ha="center")
    ax.text(7.15, 0.31, "repelling slow branch", color=GREEN, fontsize=8.1, ha="center")

    # One continuous heteroclinic orbit, colored by the two slow regimes.
    x1 = np.linspace(0.75, 5.0, 240)
    y1 = 0.35 - 0.12 * (x1 - 1.2) - 0.35 / (1 + np.exp(-4.5 * (x1 - 4.5)))
    x2 = np.linspace(5.0, 9.1, 220)
    y2 = y1[-1] + 0.55 * (1 - np.exp(-0.9 * (x2 - 5.0)))
    ax.plot(x1, y1, color=BLUE, linewidth=2.6, solid_capstyle="round", zorder=3)
    ax.plot(x2, y2, color=ORANGE, linewidth=2.6, solid_capstyle="round", zorder=3)
    arrow_on_curve(ax, x1, y1, 95, BLUE)
    arrow_on_curve(ax, x2, y2, 120, ORANGE)

    # Equilibria and fold.
    ax.plot([0.72], [y1[0]], marker="o", markersize=6.5, markerfacecolor="white", markeredgewidth=1.5, markeredgecolor=BLUE)
    ax.text(0.72, y1[0] + 0.27, r"$Z_N^+$", ha="center", fontsize=9)
    ax.text(1.08, y1[0] - 0.38, r"inward branch of $W^u(Z_N^+)$", ha="left", fontsize=7.9, color=BLUE)

    fold_idx = np.argmin(y1)
    ax.plot([x1[fold_idx]], [y1[fold_idx]], marker="o", markersize=4.5, color=INK, zorder=4)
    ax.text(x1[fold_idx], y1[fold_idx] - 0.27, "fold passage", ha="center", fontsize=8.2)

    ax.plot([9.15], [y2[-1]], marker="o", markersize=6.5, markerfacecolor="white", markeredgewidth=1.5, markeredgecolor=ORANGE)
    ax.text(9.15, y2[-1] + 0.27, r"$Z_N^-$", ha="center", fontsize=9)

    # Codimension-one stable manifold shown as a band at a section.
    ax.add_patch(
        Rectangle(
            (8.45, -0.55),
            0.32,
            1.45,
            facecolor="#F8D8CA",
            edgecolor=ORANGE,
            linewidth=1.0,
            alpha=0.75,
            zorder=2,
        )
    )
    ax.text(8.61, -0.78, r"projected section of $W^s(Z_N^-)$", ha="center", fontsize=7.9, color=ORANGE)

    ax.annotate(
        "connection if $G=0$",
        xy=(6.05, y2[np.searchsorted(x2, 6.05)]),
        xytext=(5.85, -1.13),
        ha="center",
        fontsize=8.3,
        arrowprops=dict(arrowstyle="->", linewidth=0.9, color=INK),
    )
    fig.savefig(output, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    draw(args.output)


if __name__ == "__main__":
    main()
