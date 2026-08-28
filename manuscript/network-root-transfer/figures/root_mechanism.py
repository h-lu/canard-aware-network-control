#!/usr/bin/env python3
"""Generate the exact/schematic mechanism figure for Paper A.

Panel (a) is a fold-matching schematic built around the exact singular
parabola.  Panel (b) is a dependency diagram of the proved two-delay source,
nonlinear readout, and dual reconstruction identities.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch


BLUE = "#2369A0"
ORANGE = "#C84E2F"
DARK = "#222222"
MID = "#696969"
LIGHT = "#B7B7B7"
PALE = "#F5F5F3"


def flow_arrow(ax, start, end, color, *, scale=8.5, linewidth=1.35):
    """Arrow in data coordinates, used only for the schematic traces."""
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=scale,
            linewidth=linewidth,
            color=color,
            shrinkA=0,
            shrinkB=0,
            zorder=6,
        )
    )


def diagram_box(
    ax,
    xy,
    text,
    *,
    edge=DARK,
    face="white",
    linewidth=0.85,
    linestyle="solid",
    fontsize=7.0,
    pad=0.30,
    linespacing=1.22,
):
    """Directly labelled rounded box in axes coordinates."""
    ax.text(
        *xy,
        text,
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=fontsize,
        linespacing=linespacing,
        color=DARK,
        bbox={
            "boxstyle": f"round,pad={pad}",
            "facecolor": face,
            "edgecolor": edge,
            "linewidth": linewidth,
            "linestyle": linestyle,
        },
        zorder=4,
    )


def diagram_arrow(
    ax,
    start,
    end,
    *,
    color=DARK,
    style="-|>",
    linewidth=0.9,
    linestyle="solid",
    label=None,
    label_xy=None,
    label_size=6.5,
):
    """Dependency arrow in axes coordinates, with an optional direct label."""
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        xycoords=ax.transAxes,
        textcoords=ax.transAxes,
        arrowprops={
            "arrowstyle": style,
            "color": color,
            "linewidth": linewidth,
            "linestyle": linestyle,
            "shrinkA": 2,
            "shrinkB": 2,
        },
        zorder=2,
    )
    if label is not None and label_xy is not None:
        ax.text(
            *label_xy,
            label,
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=label_size,
            color=color,
            bbox={"facecolor": "white", "edgecolor": "none", "pad": 0.45},
            zorder=3,
        )


def make_figure(output: Path) -> None:
    mpl.rcParams.update(
        {
            "font.family": "serif",
            "font.size": 8.0,
            "axes.linewidth": 0.7,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )

    # The manuscript reduces this 7.15-inch source to a 6.5-inch text block.
    fig = plt.figure(figsize=(7.15, 4.05), constrained_layout=True)
    grid = fig.add_gridspec(1, 2, width_ratios=(0.78, 1.52), wspace=0.14)

    # Panel (a): exact parabola, schematic retained traces and preparation tails.
    ax = fig.add_subplot(grid[0, 0])
    x = np.linspace(-1.66, 1.66, 400)
    singular_y = x**2 - 0.50
    ax.plot(x, singular_y, color=LIGHT, linewidth=1.15, zorder=1)

    xa = np.linspace(1.38, 0.0, 160)
    xr = np.linspace(0.0, -1.38, 160)
    ya = xa**2 - 0.445 + 0.018 * xa
    yr = xr**2 - 0.445 - 0.018 * xr
    ax.plot(xa, ya, color=BLUE, linewidth=2.2, zorder=4)
    ax.plot(xr, yr, color=ORANGE, linewidth=2.2, zorder=4)

    xat = np.linspace(1.63, 1.38, 45)
    xrt = np.linspace(-1.38, -1.63, 45)
    ax.plot(
        xat,
        xat**2 - 0.445 + 0.018 * xat,
        color=MID,
        linewidth=1.6,
        linestyle=(0, (1.0, 2.0)),
        zorder=2,
    )
    ax.plot(
        xrt,
        xrt**2 - 0.445 - 0.018 * xrt,
        color=MID,
        linewidth=1.6,
        linestyle=(0, (1.0, 2.0)),
        zorder=2,
    )

    flow_arrow(
        ax,
        (0.77, 0.77**2 - 0.445 + 0.018 * 0.77),
        (0.49, 0.49**2 - 0.445 + 0.018 * 0.49),
        BLUE,
    )
    flow_arrow(
        ax,
        (-0.49, 0.49**2 - 0.445 + 0.018 * 0.49),
        (-0.77, 0.77**2 - 0.445 + 0.018 * 0.77),
        ORANGE,
    )

    ax.axvline(0.0, color=MID, linewidth=0.75, linestyle=(0, (4, 3)), zorder=0)
    ax.scatter([0.0], [-0.445], s=19, facecolor="white", edgecolor=DARK,
               linewidth=0.9, zorder=7)

    ax.text(
        0.0,
        2.34,
        "exact singular curve; schematic traces",
        color=MID,
        fontsize=6.7,
        ha="center",
    )
    ax.text(
        1.02,
        1.72,
        r"$\gamma_0\subset\{\mathcal{H}_\alpha=0\}$",
        color=MID,
        fontsize=6.8,
        ha="center",
        rotation=20,
    )
    ax.text(0.72, 0.16, r"retained $z^a$", color=BLUE, fontsize=7.0, ha="center")
    ax.text(-0.72, 0.16, r"retained $z^r$", color=ORANGE, fontsize=7.0, ha="center")
    ax.text(
        0.055,
        1.05,
        r"phase section $X=0$",
        color=MID,
        fontsize=6.7,
        rotation=90,
        va="center",
    )
    ax.annotate(
        "selected match",
        xy=(0.0, -0.445),
        xytext=(0.55, -0.69),
        fontsize=6.8,
        color=DARK,
        ha="center",
        arrowprops={"arrowstyle": "-", "color": DARK, "linewidth": 0.65},
    )
    ax.text(
        0.0,
        2.58,
        "dotted: preparation tails",
        color=MID,
        fontsize=6.6,
        ha="center",
    )

    ax.spines[["top", "right"]].set_visible(False)
    ax.set_xlim(-1.78, 1.78)
    ax.set_ylim(-0.78, 2.72)
    ax.set_xlabel(r"$\widehat X=\alpha X$", labelpad=1)
    ax.set_ylabel(r"$\widehat Y=\alpha Y$", labelpad=1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(
        "(a) Complete-history fold match",
        loc="left",
        fontweight="bold",
        fontsize=8.4,
    )

    # Panel (b): exact source/reconstruction identities and proved root readout.
    bx = fig.add_subplot(grid[0, 1])
    bx.set_axis_off()
    bx.set_title(
        "(b) Blind probes and compressed-return recovery",
        loc="left",
        fontweight="bold",
        fontsize=8.2,
    )
    bx.text(
        0.995,
        0.985,
        "equations: proved\nlayout: schematic",
        transform=bx.transAxes,
        ha="right",
        va="top",
        fontsize=6.5,
        color=MID,
    )

    diagram_box(
        bx,
        (0.34, 0.895),
        "projection-blind pure redistributions\n"
        r"$\pi_N^TR_k=0\ (\mathrm{all}\ k),\qquad \sum_kR_k=0$",
        face=PALE,
        linewidth=1.0,
        fontsize=7.0,
    )
    bx.text(
        0.34,
        0.815,
        "exact collective blindness; zeroth delay moment vanishes",
        transform=bx.transAxes,
        ha="center",
        va="center",
        fontsize=6.5,
        color=MID,
    )

    diagram_box(
        bx,
        (0.34, 0.675),
        "two distinct delay locations\n"
        r"$\mathsf{S}_N\mathbf{R}="
        r"\frac{K}{2\alpha}P_{\perp,N}"
        r"(\sum_k\theta_kR_k)\mathbf{1}$"
        "\n"
        r"$\mathsf{S}_N:\mathfrak{T}_N^{\rm red}\to E_N$ is onto",
        linewidth=1.15,
        fontsize=6.65,
    )
    diagram_arrow(
        bx,
        (0.34, 0.795),
        (0.34, 0.755),
        label=r"$\theta_0<\theta_m$",
        label_xy=(0.34, 0.778),
    )

    diagram_box(
        bx,
        (0.79, 0.685),
        "sharp right inverse\n"
        r"$(\mathsf{Q}_Ny)_{0,m}=\mp"
        r"\frac{2\alpha}{K\Delta_\theta}y\pi_N^T$"
        "\n"
        r"$\|\mathsf{S}_N\|=\frac{|K|\Delta_\theta}{4\alpha},\quad"
        r"\|\mathsf{Q}_N\|=\frac{4\alpha}{|K|\Delta_\theta}$",
        edge="#525252",
        fontsize=6.5,
        pad=0.28,
    )
    diagram_arrow(bx, (0.64, 0.685), (0.51, 0.685), style="-|>", color=MID)

    diagram_box(
        bx,
        (0.34, 0.485),
        "stable transverse lift\n"
        r"$h=\mathsf{T}_N\mathbf{R}=A_N^{-1}\mathsf{S}_N\mathbf{R}\in E_N$"
        "\n"
        r"$\mathsf{T}_N\mathsf{Q}_NA_Nz=z$",
        fontsize=6.7,
    )
    diagram_arrow(bx, (0.34, 0.596), (0.34, 0.555))

    diagram_box(
        bx,
        (0.80, 0.485),
        "one merged delay location: no-go\n"
        r"$\sum_k\theta_kR_k=\theta_*\sum_kR_k=0$"
        "\n"
        r"$\Longrightarrow\ \mathsf{S}_N=0$",
        edge=MID,
        face=PALE,
        linestyle=(0, (3, 2)),
        fontsize=6.5,
    )
    # Route the no-go branch around the main chain and the right-inverse box.
    diagram_arrow(
        bx,
        (0.51, 0.895),
        (0.975, 0.895),
        color=MID,
        style="-",
        linestyle=(0, (3, 2)),
        label="one merged delay",
        label_xy=(0.78, 0.875),
        label_size=6.5,
    )
    diagram_arrow(
        bx,
        (0.975, 0.895),
        (0.975, 0.485),
        color=MID,
        style="-",
        linestyle=(0, (3, 2)),
    )
    diagram_arrow(
        bx,
        (0.975, 0.485),
        (0.915, 0.485),
        color=MID,
        linestyle=(0, (3, 2)),
    )

    diagram_box(
        bx,
        (0.34, 0.285),
        "nonlinear selected-root responses\n"
        r"$\frac{\mu_{c,N}(\delta,\zeta)-\mu_{c,N}(\delta,0)}"
        r"{\delta^3\zeta}"
        r"=\Lambda_N(\mathbf{R})+O(\delta+|\zeta|)$",
        linewidth=1.1,
        fontsize=6.55,
    )
    diagram_arrow(bx, (0.34, 0.415), (0.34, 0.365))

    diagram_box(
        bx,
        (0.34, 0.085),
        "dual reconstruction of the compressed return\n"
        r"$\mathfrak{r}_N(z)=\Lambda_N(\mathsf{Q}_NA_Nz),\qquad z\in E_N$"
        "\n"
        r"$\dim E_N=N-1$: use a spanning probe family",
        linewidth=1.35,
        fontsize=6.55,
    )
    diagram_arrow(bx, (0.34, 0.205), (0.34, 0.16))

    diagram_box(
        bx,
        (0.80, 0.205),
        "two separate realization profiles\n"
        r"curvature: $-\alpha^{-1}\pi_N^T(c_N\circ h)$"
        "\n"
        r"recovery: $\pi_N^T[(\varpi_N-c_N/\alpha)\circ h]$",
        edge=MID,
        linestyle=(0, (4, 2)),
        fontsize=6.5,
        pad=0.26,
    )
    # Redundant color cues: the boxes remain intelligible in grayscale.
    bx.plot([0.665, 0.705], [0.195, 0.195], transform=bx.transAxes,
            color=BLUE, linewidth=2.0, solid_capstyle="round", zorder=5)
    bx.plot([0.665, 0.705], [0.163, 0.163], transform=bx.transAxes,
            color=ORANGE, linewidth=2.0, linestyle=(0, (3, 1.5)), zorder=5)
    diagram_arrow(
        bx,
        (0.70, 0.13),
        (0.55, 0.105),
        color=MID,
        style="-|>",
        linestyle=(0, (2, 2)),
        linewidth=0.8,
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, format="pdf", bbox_inches="tight", pad_inches=0.025)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).with_name("root-mechanism.pdf"),
    )
    args = parser.parse_args()
    make_figure(args.output)


if __name__ == "__main__":
    main()
