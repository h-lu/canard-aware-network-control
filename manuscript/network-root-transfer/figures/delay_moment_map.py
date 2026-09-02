#!/usr/bin/env python3
"""Generate the delay-moment/Fredholm diagram as a vector PDF."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42


INK = "#202124"
BLUE = "#2F6F9F"
BLUE_FILL = "#EAF2F8"
ORANGE = "#B65C2A"
ORANGE_FILL = "#FCEFE7"
GRAY = "#6B7075"


def box(ax, xy, wh, text, *, edge=INK, face="white", dashed=False, fontsize=8.5):
    x, y = xy
    w, h = wh
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.018,rounding_size=0.025",
        linewidth=1.15,
        edgecolor=edge,
        facecolor=face,
        linestyle=(0, (4, 2)) if dashed else "solid",
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize)
    return patch


def arrow(ax, start, end, *, color=INK, dashed=False):
    arr = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=10,
        linewidth=1.15,
        color=color,
        linestyle=(0, (4, 2)) if dashed else "solid",
        shrinkA=3,
        shrinkB=3,
    )
    ax.add_patch(arr)


def draw(output: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.35, 3.15))
    ax.set_xlim(-0.025, 1.025)
    ax.set_ylim(0, 1)
    ax.axis("off")

    box(
        ax,
        (0.015, 0.36),
        (0.205, 0.30),
        r"perturbation $E=(E_k)$"
        "\n"
        r"of delayed coupling"
        "\n"
        r"$\pi_N^TE_k=0$, $\sum_kE_k=0$",
        fontsize=7.5,
    )
    box(
        ax,
        (0.275, 0.36),
        (0.205, 0.30),
        r"first moment"
        "\n"
        r"$\mathsf{S}_NE=\frac{K}{2\alpha}P_{\perp,N}$"
        "\n"
        r"$\left(\sum_k\theta_kE_k\right)\mathbf{1}$",
        edge=BLUE,
        face=BLUE_FILL,
        fontsize=7.6,
    )
    box(
        ax,
        (0.535, 0.36),
        (0.185, 0.30),
        r"transverse variation"
        "\n"
        r"$h_E=A_N^{-1}\mathsf{S}_NE$",
        edge=BLUE,
        face=BLUE_FILL,
    )
    box(
        ax,
        (0.775, 0.36),
        (0.205, 0.30),
        r"if a heteroclinic defining"
        "\n"
        r"function $G$ is available"
        "\n"
        r"$D_E\mu_{c,N}=\delta^3\Lambda_N(E)+O(\delta^4)$",
        edge=ORANGE,
        face=ORANGE_FILL,
        fontsize=7.3,
    )

    arrow(ax, (0.22, 0.51), (0.275, 0.51))
    arrow(ax, (0.48, 0.51), (0.535, 0.51), color=BLUE)
    arrow(ax, (0.72, 0.51), (0.775, 0.51), color=ORANGE)

    ax.text(
        0.747,
        0.735,
        r"$\Lambda_N(E)=-\alpha^{-1}\pi_N^T\mathrm{diag}(c_N)h_E$",
        ha="center",
        va="center",
        fontsize=7.4,
        color=INK,
    )

    box(
        ax,
        (0.015, 0.76),
        (0.35, 0.18),
        r"exact identity: $D_E(\Pi_N\mathcal{F}_N)(\Phi)=0$"
        "\n"
        r"for every history $\Phi$",
        edge=GRAY,
        face="#F5F5F5",
        fontsize=7.8,
    )
    arrow(ax, (0.118, 0.66), (0.118, 0.76), color=GRAY)

    box(
        ax,
        (0.276, 0.075),
        (0.205, 0.14),
        r"one merged delay"
        "\n"
        r"$\mathsf{S}_NE=0$",
        edge=GRAY,
        face="white",
        dashed=True,
        fontsize=8.2,
    )
    arrow(ax, (0.378, 0.36), (0.378, 0.215), color=GRAY, dashed=True)

    ax.text(
        0.995,
        0.015,
        "linear maps exact; final equality conditional and asymptotic",
        ha="right",
        va="bottom",
        fontsize=6.8,
        color=GRAY,
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
