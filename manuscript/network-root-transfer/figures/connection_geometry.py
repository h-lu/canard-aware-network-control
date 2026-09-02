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
PALE_GRAY = "#EFEFEA"


def arrow_on_curve(ax, x, y, idx, color):
    """Place a forward-time arrow without changing the curve geometry."""
    ax.add_patch(
        FancyArrowPatch(
            (x[idx - 5], y[idx - 5]),
            (x[idx + 5], y[idx + 5]),
            arrowstyle="-|>",
            mutation_scale=12,
            linewidth=0,
            color=color,
            shrinkA=0,
            shrinkB=0,
            zorder=5,
        )
    )


def draw_projection_panel(ax) -> None:
    """Draw the schematic global projection in the coordinates (-r,w)."""
    ax.set_xlim(0, 6)
    ax.set_ylim(-1.15, 1.35)
    ax.axis("off")

    ax.text(
        0.02,
        0.98,
        r"(a)  Projection at $G=0$",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=9.2,
        fontweight="bold",
    )

    # Coordinate arrows.  The horizontal coordinate is exactly the one used
    # in the manuscript; forward fold time points from left to right.
    ax.annotate(
        "",
        xy=(5.82, -1.02),
        xytext=(0.28, -1.02),
        arrowprops=dict(arrowstyle="->", linewidth=0.8, color=INK),
    )
    ax.annotate(
        "",
        xy=(0.28, 0.92),
        xytext=(0.28, -1.02),
        arrowprops=dict(arrowstyle="->", linewidth=0.8, color=INK),
    )
    ax.text(5.90, -1.02, r"$-r$", ha="left", va="center", fontsize=8.5)
    ax.text(0.16, 0.90, r"$w$", ha="center", va="bottom", fontsize=8.5)

    # The exact agreement condition is |r| <= r_loc.  The affine horizontal
    # placement is schematic, but the region is therefore drawn as a strip.
    ax.add_patch(
        Rectangle(
            (2.18, -0.91),
            1.64,
            1.93,
            facecolor=PALE_GRAY,
            edgecolor="#B3B3AA",
            linewidth=0.8,
            zorder=0,
        )
    )
    ax.text(
        3.0,
        0.88,
        "agreement strip",
        ha="center",
        va="bottom",
        fontsize=7.7,
        color=GRAY,
    )
    ax.text(
        3.0,
        0.71,
        r"$|r|\leq r_{\rm loc}$",
        ha="center",
        va="bottom",
        fontsize=7.7,
        color=GRAY,
    )

    # In (-r,w), both the frozen critical curve and the distinguished fold
    # orbit have a local maximum.  The critical curve is dashed; the solid
    # curve is the specified conditional orbit at a zero of G.
    x = np.linspace(0.68, 5.32, 401)
    half_width = (5.32 - 0.68) / 2
    critical = 0.43 - 0.16 * (x - 3.0) ** 2
    profile = np.maximum(0.0, 1.0 - ((x - 3.0) / half_width) ** 2) ** 2
    bump = 0.19 * profile
    skew = 0.035 * (x - 3.0) * profile
    orbit = critical + bump + skew

    ax.plot(
        x,
        critical,
        color=GREEN,
        linewidth=1.35,
        linestyle=(0, (5, 3)),
        zorder=2,
    )
    ax.plot(x, orbit, color=BLUE, linewidth=2.45, solid_capstyle="round", zorder=4)
    arrow_on_curve(ax, x, orbit, 112, INK)
    arrow_on_curve(ax, x, orbit, 292, INK)

    ax.text(
        1.25,
        0.47,
        "attracting branch",
        color=GREEN,
        fontsize=7.55,
        ha="center",
        va="bottom",
    )
    ax.text(
        4.76,
        0.47,
        "repelling branch",
        color=GREEN,
        fontsize=7.55,
        ha="center",
        va="bottom",
    )
    # Outer equilibria.  Equal schematic heights avoid claiming an ordering
    # that is not fixed by the stated hypotheses.
    y_left = orbit[0]
    y_right = orbit[-1]
    ax.plot(
        [x[0], x[-1]],
        [y_left, y_right],
        linestyle="none",
        marker="o",
        markersize=6.2,
        markerfacecolor="white",
        markeredgewidth=1.45,
        markeredgecolor=BLUE,
        zorder=6,
    )
    ax.text(x[0], y_left - 0.24, r"$Z_N^+$", ha="center", fontsize=8.8)
    ax.text(x[-1], y_right - 0.24, r"$Z_N^-$", ha="center", fontsize=8.8)

    # The common phase section and the distinct fold and orbit points on it.
    section_x = 3.0
    fold_y = 0.43
    incoming_y = 0.62
    ax.plot(
        [section_x, section_x],
        [-0.68, incoming_y],
        color=INK,
        linewidth=0.85,
        linestyle=(0, (2, 2)),
        zorder=1,
    )
    ax.plot(
        [section_x],
        [fold_y],
        marker="D",
        markersize=4.0,
        markerfacecolor="white",
        markeredgewidth=1.0,
        markeredgecolor=GREEN,
        zorder=6,
    )
    ax.plot(
        [section_x],
        [incoming_y],
        marker="o",
        markersize=4.8,
        markerfacecolor=BLUE,
        markeredgewidth=0,
        zorder=7,
    )
    ax.text(section_x, -0.83, r"$\Sigma_0=\{X=0\}$", ha="center", fontsize=7.65)
    ax.text(
        section_x + 0.45,
        incoming_y + 0.04,
        r"$A^0$",
        ha="left",
        va="bottom",
        fontsize=7.8,
    )
    ax.text(section_x + 0.11, fold_y - 0.27, "fold", ha="left", fontsize=7.55, color=GREEN)


def draw_section_panel(ax) -> None:
    """Draw a two-dimensional slice of the chart on the phase section."""
    ax.set_xlim(0, 4.15)
    ax.set_ylim(-1.15, 1.35)
    ax.axis("off")

    ax.text(
        0.02,
        0.98,
        r"(b)  Defining function on $\mathcal{M}_{\Sigma_0}^2$",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=9.2,
        fontweight="bold",
    )
    ax.text(
        0.50,
        0.88,
        r"schematic slice, shown for $G\ne0$",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=7.45,
        color=GRAY,
    )

    ax.annotate(
        "",
        xy=(3.98, -1.02),
        xytext=(0.38, -1.02),
        arrowprops=dict(arrowstyle="->", linewidth=0.8, color=INK),
    )
    ax.annotate(
        "",
        xy=(0.38, 0.91),
        xytext=(0.38, -1.02),
        arrowprops=dict(arrowstyle="->", linewidth=0.8, color=INK),
    )
    ax.text(4.05, -1.02, r"$\psi$", ha="left", va="center", fontsize=8.5)
    ax.text(0.22, 0.89, r"$u$", ha="center", va="bottom", fontsize=8.5)

    psi = np.linspace(0.72, 3.78, 250)
    stable = -0.33 + 0.12 * (psi - 2.15) + 0.105 * (psi - 2.15) ** 2
    ax.plot(psi, stable, color=ORANGE, linewidth=2.1, zorder=3)
    ax.text(
        2.35,
        -0.50,
        r"stable section: $u=F^-(\psi)$",
        ha="center",
        va="top",
        fontsize=7.45,
        color=ORANGE,
    )

    psi_a = 2.58
    stable_a = -0.33 + 0.12 * (psi_a - 2.15) + 0.105 * (psi_a - 2.15) ** 2
    u_a = stable_a + 0.68
    ax.plot(
        [psi_a],
        [stable_a],
        marker="s",
        markersize=4.0,
        markerfacecolor="white",
        markeredgewidth=1.1,
        markeredgecolor=ORANGE,
        zorder=5,
    )
    ax.plot(
        [psi_a],
        [u_a],
        marker="o",
        markersize=5.2,
        markerfacecolor=BLUE,
        markeredgewidth=0,
        zorder=6,
    )
    ax.text(
        psi_a + 0.13,
        u_a + 0.04,
        r"$A^0=(\psi_A,u_A)$",
        ha="left",
        va="bottom",
        fontsize=7.7,
        color=BLUE,
    )
    ax.plot(
        [psi_a, psi_a],
        [stable_a, u_a],
        color=INK,
        linewidth=0.8,
        linestyle=(0, (2, 2)),
        zorder=2,
    )
    ax.add_patch(
        FancyArrowPatch(
            (psi_a + 0.10, stable_a + 0.025),
            (psi_a + 0.10, u_a - 0.025),
            arrowstyle="<->",
            mutation_scale=8,
            linewidth=0.9,
            color=INK,
            zorder=4,
        )
    )
    ax.text(
        1.48,
        0.25,
        r"$G=u_A-F^-(\psi_A)$",
        ha="center",
        va="center",
        fontsize=7.55,
    )

    ax.text(
        2.15,
        -0.80,
        r"$G=0\ \Longleftrightarrow\ A^0\in W^s(Z_N^-)\cap\mathcal{M}_{\Sigma_0}^2$",
        ha="center",
        va="center",
        fontsize=6.65,
    )


def draw(output: Path) -> None:
    fig = plt.figure(figsize=(7.35, 3.05))
    grid = fig.add_gridspec(1, 2, width_ratios=(1.55, 1.0), wspace=0.08)
    draw_projection_panel(fig.add_subplot(grid[0, 0]))
    draw_section_panel(fig.add_subplot(grid[0, 1]))
    fig.savefig(output, bbox_inches="tight", pad_inches=0.025)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    draw(args.output)


if __name__ == "__main__":
    main()
