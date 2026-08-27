#!/usr/bin/env python3
"""Generate the mixed exact/schematic mechanism figure for Paper A."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch


BLUE = "#2369A0"
ORANGE = "#C84E2F"
GRAY = "#777777"
DARK = "#222222"


def arrow_along(ax, start, end, color, mutation_scale=9):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=mutation_scale,
            linewidth=1.45,
            color=color,
            shrinkA=0,
            shrinkB=0,
            zorder=5,
        )
    )


def box(ax, xy, text, *, edge=DARK, linewidth=0.8):
    ax.text(
        *xy,
        text,
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=7.2,
        linespacing=1.25,
        bbox={
            "boxstyle": "round,pad=0.32",
            "facecolor": "white",
            "edgecolor": edge,
            "linewidth": linewidth,
        },
        zorder=3,
    )


def dependency_arrow(ax, start, end, *, color=DARK, style="-|>"):
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        xycoords=ax.transAxes,
        textcoords=ax.transAxes,
        arrowprops={
            "arrowstyle": style,
            "color": color,
            "linewidth": 0.9,
            "shrinkA": 2,
            "shrinkB": 2,
        },
        zorder=2,
    )


def make_figure(output: Path) -> None:
    mpl.rcParams.update(
        {
            "font.family": "serif",
            "font.size": 8,
            "axes.linewidth": 0.7,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )

    fig = plt.figure(figsize=(7.15, 3.55), constrained_layout=True)
    grid = fig.add_gridspec(1, 2, width_ratios=(1.03, 1.18), wspace=0.18)

    # Panel (a): exact parabola plus schematic finite-delta selected traces.
    ax = fig.add_subplot(grid[0, 0])
    x = np.linspace(-1.72, 1.72, 400)
    ax.plot(x, x**2 - 0.5, color="#AAAAAA", linewidth=1.0, zorder=1)

    xa = np.linspace(1.47, 0.0, 150)
    ya = xa**2 - 0.46 + 0.02 * xa
    xr = np.linspace(0.0, -1.47, 150)
    yr = xr**2 - 0.46 - 0.02 * xr
    ax.plot(xa, ya, color=BLUE, linewidth=2.2, zorder=4)
    ax.plot(xr, yr, color=ORANGE, linewidth=2.2, zorder=4)

    xat = np.linspace(1.70, 1.47, 50)
    xrt = np.linspace(-1.47, -1.70, 50)
    ax.plot(
        xat,
        xat**2 - 0.46 + 0.02 * xat,
        color=GRAY,
        linewidth=1.8,
        linestyle=(0, (1.2, 2.0)),
    )
    ax.plot(
        xrt,
        xrt**2 - 0.46 - 0.02 * xrt,
        color=GRAY,
        linewidth=1.8,
        linestyle=(0, (1.2, 2.0)),
    )

    arrow_along(
        ax,
        (0.82, 0.82**2 - 0.46 + 0.02 * 0.82),
        (0.56, 0.56**2 - 0.46 + 0.02 * 0.56),
        BLUE,
    )
    arrow_along(
        ax,
        (-0.56, 0.56**2 - 0.46 + 0.02 * 0.56),
        (-0.82, 0.82**2 - 0.46 + 0.02 * 0.82),
        ORANGE,
    )

    ax.axvline(0.0, color="#999999", linewidth=0.8, linestyle=(0, (4, 3)))
    ax.scatter([0.0], [-0.46], s=16, color=DARK, zorder=6)
    ax.scatter([1.47], [ya[0]], s=10, color=BLUE, zorder=6)
    ax.scatter([-1.47], [yr[-1]], s=10, color=ORANGE, zorder=6)

    ax.text(
        1.12,
        2.24,
        r"$\gamma_0\subset\{\mathscr{H}_\alpha=0\}$",
        color="#666666",
        fontsize=7.2,
        ha="center",
    )
    ax.text(0.76, 0.34, r"retained $z^a$", color=BLUE, fontsize=7.2)
    ax.text(-0.76, 0.34, r"retained $z^r$", color=ORANGE, fontsize=7.2, ha="right")
    ax.text(
        0.04,
        1.33,
        r"phase section $X=0$",
        color="#666666",
        fontsize=7,
        rotation=90,
        va="center",
    )
    ax.text(0.0, -0.64, "history root", fontsize=7.1, ha="center", va="top")
    ax.text(
        0.0,
        2.57,
        "dotted outer pieces: prepared selection tails",
        color="#666666",
        fontsize=6.9,
        ha="center",
    )

    ax.spines[["top", "right"]].set_visible(False)
    ax.set_xlim(-1.85, 1.85)
    ax.set_ylim(-0.75, 2.75)
    ax.set_xlabel(r"$\widehat X=\alpha X$", labelpad=1)
    ax.set_ylabel(r"$\widehat Y=\alpha Y$", labelpad=1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("(a) Complete-history matching", loc="left", fontweight="bold")

    # Panel (b): exact dependencies in the response coefficient.
    bx = fig.add_subplot(grid[0, 1])
    bx.set_axis_off()
    bx.set_title("(b) Structural response mechanism", loc="left", fontweight="bold")

    box(
        bx,
        (0.35, 0.88),
        "row-neutral delay redistribution\n" r"$\{R_{k,N}\}_{k=0}^m$",
    )
    box(bx, (0.35, 0.69), "delay moment\n" r"$\dot M_{1,N}\mathbf{1}$")
    box(
        bx,
        (0.35, 0.49),
        "transverse resolvent\n"
        r"$h_{*,N}=\frac{K}{2\alpha}"
        r"A_N^{-1}P_{\perp,N}\dot M_{1,N}\mathbf{1}$",
    )
    box(
        bx,
        (0.35, 0.285),
        "heterogeneous-curvature return\n"
        r"$r_N=\pi_N^T\operatorname{diag}(c_N)h_{*,N}$",
    )
    box(
        bx,
        (0.35, 0.085),
        "root response\n"
        r"$\partial_\zeta\mu_{c,N}"
        r"=-\delta^3r_N/\alpha+O(\delta^4)$",
        linewidth=1.35,
    )

    dependency_arrow(bx, (0.35, 0.81), (0.35, 0.755))
    dependency_arrow(bx, (0.35, 0.625), (0.35, 0.565))
    dependency_arrow(bx, (0.35, 0.405), (0.35, 0.36))
    dependency_arrow(bx, (0.35, 0.205), (0.35, 0.16))

    box(
        bx,
        (0.80, 0.65),
        r"$\pi_N^TR_{k,N}=0$" "\ndirect collective\nterm cancels",
        edge="#888888",
    )
    dependency_arrow(bx, (0.56, 0.86), (0.73, 0.72), color="#888888")
    dependency_arrow(
        bx,
        (0.80, 0.565),
        (0.80, 0.46),
        color="#888888",
        style="-[",
    )
    bx.text(
        0.80,
        0.42,
        "indirect path\nsurvives",
        transform=bx.transAxes,
        ha="center",
        va="top",
        fontsize=7,
        color="#666666",
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, format="pdf", bbox_inches="tight", pad_inches=0.03)
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
