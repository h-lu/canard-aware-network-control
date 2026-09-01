#!/usr/bin/env python3
"""Generate the flagship mechanism figure for Paper A.

The artifact is deliberately mixed rather than numerical evidence:

* panel (a) is a schematic history-space channel populated by invariant
  objects proved in the paper;
* panel (b) places proved identities and estimates in a schematic dependency
  diagram;
* panel (c) schematically realizes the proved modelwise centering and conormal
  limit.

Reproduce from ``manuscript/network-root-transfer`` with ``make figure``.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, PathPatch
from matplotlib.path import Path as MplPath


BLUE = "#2369A0"
VERMILION = "#C84E2F"
PURPLE = "#6A4C93"
DARK = "#202020"
MID = "#666666"
LIGHT = "#B8B8B8"
PALE = "#F3F3F0"
PALE_BLUE = "#EAF2F8"
PALE_ORANGE = "#FAEEE9"
PDF_TIMESTAMP = datetime(2026, 8, 31, tzinfo=timezone.utc)
PDF_METADATA = {
    "Title": "Projection-blind delay redistribution and anchored canard response",
    "Author": "Haibo Lu",
    "Subject": "Schematic of the proved mechanism",
    "Creator": "root_mechanism.py",
    "Producer": "Matplotlib",
    "CreationDate": PDF_TIMESTAMP,
    "ModDate": PDF_TIMESTAMP,
}


def axes_arrow(ax, start, end, *, color=DARK, lw=1.0, style="-|>", zorder=5):
    """Draw an arrow whose coordinates are fractions of an axes."""
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            transform=ax.transAxes,
            arrowstyle=style,
            mutation_scale=8.5,
            linewidth=lw,
            color=color,
            shrinkA=0,
            shrinkB=0,
            zorder=zorder,
        )
    )


def labelled_box(
    ax,
    center,
    width,
    height,
    text,
    *,
    face="white",
    edge=DARK,
    linestyle="solid",
    fontsize=6.65,
    linewidth=0.9,
):
    """Draw a rounded dependency box in axes coordinates."""
    x, y = center
    patch = FancyBboxPatch(
        (x - width / 2, y - height / 2),
        width,
        height,
        transform=ax.transAxes,
        boxstyle="round,pad=0.014,rounding_size=0.018",
        facecolor=face,
        edgecolor=edge,
        linewidth=linewidth,
        linestyle=linestyle,
        zorder=2,
    )
    ax.add_patch(patch)
    ax.text(
        x,
        y,
        text,
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=fontsize,
        linespacing=1.20,
        color=DARK,
        zorder=3,
    )


def curve_patch(ax, vertices, codes, *, color, lw, linestyle="solid", zorder=4):
    """Draw a Bezier curve in axes coordinates."""
    patch = PathPatch(
        MplPath(vertices, codes),
        transform=ax.transAxes,
        facecolor="none",
        edgecolor=color,
        linewidth=lw,
        linestyle=linestyle,
        capstyle="round",
        zorder=zorder,
    )
    ax.add_patch(patch)
    return patch


def panel_history_channel(ax) -> None:
    """Panel (a): one fixed anchored RFDE and its complete connection."""
    ax.set_axis_off()
    ax.set_title(
        "(a) One fixed anchored RFDE",
        loc="left",
        fontweight="bold",
        fontsize=8.2,
        pad=4,
    )

    # Regions are schematic.  The central rectangle means literal equality of
    # the anchored and unanchored vector fields on the retained history tube.
    ax.add_patch(
        FancyBboxPatch(
            (0.34, 0.20),
            0.32,
            0.64,
            transform=ax.transAxes,
            boxstyle="round,pad=0.012,rounding_size=0.02",
            facecolor=PALE,
            edgecolor=LIGHT,
            linewidth=0.75,
            zorder=0,
        )
    )
    ax.text(
        0.50,
        0.78,
        r"retained fold-history tube",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=6.6,
        color=MID,
    )
    ax.text(
        0.50,
        0.70,
        r"$g_{\rm anc}=1$: exact original law",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=6.5,
        color=MID,
    )
    ax.text(
        0.14,
        0.82,
        "anchor-modified\nouter law",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=6.3,
        color=MID,
    )
    ax.text(
        0.86,
        0.82,
        "anchor-modified\nouter law",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=6.3,
        color=MID,
    )

    # A single schematic orbit, split only to identify the attracting,
    # central, and repelling tracking portions.
    codes = [MplPath.MOVETO, MplPath.CURVE4, MplPath.CURVE4, MplPath.CURVE4]
    incoming = [(0.10, 0.54), (0.20, 0.57), (0.31, 0.47), (0.47, 0.42)]
    central = [(0.47, 0.42), (0.50, 0.40), (0.53, 0.40), (0.56, 0.43)]
    outgoing = [(0.56, 0.43), (0.68, 0.50), (0.78, 0.61), (0.90, 0.55)]
    curve_patch(ax, incoming, codes, color=BLUE, lw=2.35)
    curve_patch(ax, central, codes, color=DARK, lw=2.35)
    curve_patch(
        ax,
        outgoing,
        codes,
        color=VERMILION,
        lw=2.35,
        linestyle=(0, (5, 1.6, 1.2, 1.6)),
    )

    # Forward-time arrows, one on each slow tracking segment.
    axes_arrow(ax, (0.25, 0.535), (0.31, 0.485), color=BLUE, lw=1.25)
    axes_arrow(ax, (0.70, 0.525), (0.76, 0.585), color=VERMILION, lw=1.25)

    # Exact equilibria are represented by labelled markers; their positions
    # and distances in this schematic have no metric meaning.
    ax.scatter(
        [0.085, 0.915],
        [0.54, 0.55],
        transform=ax.transAxes,
        s=34,
        facecolors=["white", "white"],
        edgecolors=[BLUE, VERMILION],
        linewidths=1.35,
        zorder=7,
    )
    ax.text(
        0.115,
        0.43,
        r"$E_N^+$" "\n" r"$\dim W^u=1$",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=6.5,
        color=BLUE,
    )
    ax.text(
        0.925,
        0.43,
        r"$E_N^-$" "\n" r"$\operatorname{codim}W^s=1$",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=6.5,
        color=VERMILION,
    )

    # A projected cue for the codimension-one stable history sheet.  It is
    # not drawn as a basin boundary and is explicitly labelled schematic.
    sheet_codes = [MplPath.MOVETO, MplPath.CURVE4, MplPath.CURVE4, MplPath.CURVE4]
    curve_patch(
        ax,
        [(0.83, 0.23), (0.88, 0.34), (0.88, 0.73), (0.84, 0.86)],
        sheet_codes,
        color=VERMILION,
        lw=1.05,
        linestyle=(0, (4, 2)),
        zorder=2,
    )
    ax.text(
        0.80,
        0.67,
        r"intrinsic $W^s(E_N^-)$" "\n" "history sheet",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=6.35,
        color=VERMILION,
    )
    ax.text(
        0.22,
        0.25,
        "attracting slow-history tracking",
        transform=ax.transAxes,
        ha="center",
        fontsize=6.05,
        color=BLUE,
    )
    ax.text(
        0.76,
        0.25,
        "repelling slow-history tracking",
        transform=ax.transAxes,
        ha="center",
        fontsize=6.05,
        color=VERMILION,
    )
    ax.text(
        0.515,
        0.345,
        "fold",
        transform=ax.transAxes,
        ha="center",
        fontsize=6.2,
        color=DARK,
    )
    axes_arrow(ax, (0.10, 0.10), (0.90, 0.10), color=MID, lw=0.75)
    ax.text(
        0.50,
        0.045,
        r"forward time; collective coordinate $r:+r_A\ \longrightarrow\ -r_A$",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=6.3,
        color=MID,
    )
    ax.text(
        0.99,
        0.96,
        "schematic history-space projection",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=6.0,
        color=MID,
    )


def panel_mechanism(ax) -> None:
    """Panel (b): exact algebra and estimates in a dependency layout."""
    ax.set_axis_off()
    ax.set_title(
        "(b) Blind source and returned root response",
        loc="left",
        fontweight="bold",
        fontsize=8.2,
        pad=4,
    )
    ax.text(
        0.99,
        0.97,
        "identities: exact/proved\nlayout: schematic",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=5.9,
        color=MID,
    )

    labelled_box(
        ax,
        (0.35, 0.86),
        0.61,
        0.145,
        "same-full-history blindness\n"
        r"$\Pi_N\mathcal{F}_{\eta}(\Phi)=\Pi_N\mathcal{F}_0(\Phi)$",
        face=PALE,
        fontsize=6.6,
    )
    labelled_box(
        ax,
        (0.35, 0.635),
        0.61,
        0.17,
        "two distinct delays\n"
        r"$\mathsf{S}_N:\mathfrak{T}_N^{\rm red}\twoheadrightarrow E_N$"
        r" with sharp $\mathsf{Q}_N$",
        face=PALE_BLUE,
        edge=BLUE,
        fontsize=6.45,
        linewidth=1.0,
    )
    labelled_box(
        ax,
        (0.35, 0.405),
        0.61,
        0.17,
        "transverse lift and return\n"
        r"$h=\mathsf{T}_N\eta=A_N^{-1}\mathsf{S}_N\eta,$"
        "  "
        r"$\Lambda_N=\mathfrak{r}_N\mathsf{T}_N$",
        fontsize=6.4,
    )
    labelled_box(
        ax,
        (0.35, 0.17),
        0.64,
        0.18,
        "fixed anchored-model heteroclinic root\n"
        r"$D_\eta\mu_{c,N}^{\rm phys}="
        r"\delta^3\Lambda_N+O(\delta^4+\delta^3\|\eta\|)$",
        face=PALE_ORANGE,
        edge=VERMILION,
        fontsize=6.35,
        linewidth=1.05,
    )
    for y0, y1 in [(0.775, 0.72), (0.55, 0.49), (0.32, 0.26)]:
        axes_arrow(ax, (0.35, y0), (0.35, y1), color=DARK, lw=0.9)

    labelled_box(
        ax,
        (0.81, 0.635),
        0.31,
        0.17,
        "one merged delay\n"
        r"$\mathsf{S}_N=0$"
        "\n(leading no-go)",
        face=PALE,
        edge=MID,
        linestyle=(0, (4, 2)),
        fontsize=6.25,
    )
    axes_arrow(ax, (0.66, 0.86), (0.81, 0.72), color=MID, lw=0.8, style="-|>")
    ax.text(
        0.80,
        0.82,
        "one delay",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=5.9,
        color=MID,
    )

    labelled_box(
        ax,
        (0.835, 0.30),
        0.30,
        0.20,
        "compressed dual recovery\n"
        r"$\mathfrak{r}_N(z)="
        r"\Lambda_N(\mathsf{Q}_NA_Nz)$"
        "\n(not the full network)",
        face="white",
        edge=MID,
        fontsize=6.2,
    )
    axes_arrow(ax, (0.66, 0.405), (0.65, 0.34), color=MID, lw=0.8)


def draw_small_axes(ax, origin, xend, yend, *, xlabel, ylabel):
    axes_arrow(ax, origin, xend, color=MID, lw=0.75)
    axes_arrow(ax, origin, yend, color=MID, lw=0.75)
    ax.text(
        xend[0],
        xend[1] - 0.055,
        xlabel,
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=6.2,
        color=MID,
    )
    ax.text(
        yend[0] - 0.012,
        yend[1],
        ylabel,
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=6.2,
        color=MID,
    )


def panel_anchor_centering(ax) -> None:
    """Panel (c): exact baselines may differ; centered conormals agree."""
    ax.set_axis_off()
    ax.set_title(
        "(c) What is and is not universal across global anchors",
        loc="left",
        fontweight="bold",
        fontsize=8.2,
        pad=4,
    )

    # Left mini-panel: absolute roots for two different global RFDEs.
    draw_small_axes(
        ax,
        (0.055, 0.17),
        (0.445, 0.17),
        (0.055, 0.88),
        xlabel=r"$\zeta$ in $\eta=\zeta R$",
        ylabel=r"$\mu_c$",
    )
    x = np.linspace(-1.0, 1.0, 160)
    x_plot = 0.25 + 0.17 * x
    y_a = 0.48 + 0.16 * x + 0.025 * x**2
    y_b = 0.67 + 0.145 * x - 0.020 * x**2
    ax.plot(x_plot, y_a, transform=ax.transAxes, color=DARK, linewidth=1.45)
    ax.plot(
        x_plot,
        y_b,
        transform=ax.transAxes,
        color=MID,
        linewidth=1.35,
        linestyle=(0, (5, 2)),
    )
    ax.scatter(
        [0.25, 0.25],
        [0.48, 0.67],
        transform=ax.transAxes,
        s=14,
        facecolor="white",
        edgecolor=[DARK, MID],
        linewidth=0.9,
        zorder=5,
    )
    ax.text(
        0.405,
        0.73,
        "anchor B (dashed)",
        transform=ax.transAxes,
        ha="right",
        fontsize=6.1,
        color=MID,
    )
    ax.text(
        0.405,
        0.42,
        "anchor A (solid)",
        transform=ax.transAxes,
        ha="right",
        fontsize=6.1,
        color=DARK,
    )
    ax.text(
        0.25,
        0.94,
        "different autonomous RFDEs: exact baselines may differ",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=6.45,
        color=DARK,
    )

    # Centering arrow between mini-panels.
    axes_arrow(ax, (0.465, 0.52), (0.535, 0.52), color=PURPLE, lw=1.1)
    ax.text(
        0.50,
        0.61,
        "center each\n" r"model at $\zeta=0$",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=6.0,
        color=PURPLE,
    )

    # Right mini-panel: centered weighted graphs and limiting tangent/conormal.
    draw_small_axes(
        ax,
        (0.74, 0.50),
        (0.965, 0.50),
        (0.74, 0.91),
        xlabel=r"$\zeta$",
        ylabel=r"$\xi=\delta^{-3}[\mu_c(\zeta R)-\mu_c(0)]$",
    )
    xr = np.linspace(-1.0, 1.0, 160)
    xp = 0.74 + 0.19 * xr
    limit = 0.50 + 0.25 * xr
    ca = 0.50 + 0.27 * xr + 0.020 * xr**2
    cb = 0.50 + 0.23 * xr - 0.018 * xr**2
    ax.plot(
        xp,
        limit,
        transform=ax.transAxes,
        color=PURPLE,
        linewidth=1.15,
        linestyle=(0, (1.2, 2.0)),
        zorder=1,
    )
    ax.plot(xp, ca, transform=ax.transAxes, color=DARK, linewidth=1.45, zorder=3)
    ax.plot(
        xp,
        cb,
        transform=ax.transAxes,
        color=MID,
        linewidth=1.35,
        linestyle=(0, (5, 2)),
        zorder=3,
    )
    ax.scatter(
        [0.74],
        [0.50],
        transform=ax.transAxes,
        s=15,
        facecolor="white",
        edgecolor=DARK,
        linewidth=0.9,
        zorder=5,
    )
    # A normal cue to the limiting tangent, labelled as a covector rather than
    # a metric vector equality.
    axes_arrow(ax, (0.74, 0.50), (0.68, 0.68), color=PURPLE, lw=1.15)
    ax.text(
        0.655,
        0.74,
        "limiting conormal\n"
        r"$\mathrm{d}\xi-\Lambda_N(R)\,\mathrm{d}\zeta$",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=6.15,
        color=PURPLE,
    )
    ax.text(
        0.84,
        0.94,
        r"both slopes $=\Lambda_N(R)+O(\delta)$",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=6.4,
        color=DARK,
    )
    ax.text(
        0.99,
        0.06,
        "curves and distances schematic; tangent and error statement proved",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=5.9,
        color=MID,
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
    fig = plt.figure(figsize=(7.15, 5.25), constrained_layout=True)
    grid = fig.add_gridspec(
        2,
        2,
        width_ratios=(1.02, 1.18),
        height_ratios=(1.20, 0.80),
        hspace=0.10,
        wspace=0.08,
    )
    panel_history_channel(fig.add_subplot(grid[0, 0]))
    panel_mechanism(fig.add_subplot(grid[0, 1]))
    panel_anchor_centering(fig.add_subplot(grid[1, :]))
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        output,
        format="pdf",
        bbox_inches="tight",
        pad_inches=0.035,
        metadata=PDF_METADATA,
    )
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
