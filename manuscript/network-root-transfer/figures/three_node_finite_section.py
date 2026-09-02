#!/usr/bin/env python3
"""Plot the three-node prescribed-history finite-section diagnostic."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


plt.rcParams.update(
    {
        "font.size": 8.3,
        "axes.labelsize": 8.7,
        "axes.titlesize": 9.1,
        "legend.fontsize": 7.6,
        "xtick.labelsize": 7.7,
        "ytick.labelsize": 7.7,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)


REPOSITORY = Path(__file__).resolve().parents[3]
DEFAULT_DATA = (
    REPOSITORY
    / "experiments"
    / "results"
    / "three_node_finite_section_diagnostic.json"
)

INK = "#202124"
BLUE = "#2F6F9F"
ORANGE = "#C65D2E"
GREEN = "#557A46"
GRAY = "#74787C"
LIGHT_GRAY = "#D2D4D5"


def load_payload(path: Path) -> dict[str, object]:
    """Load and minimally validate the archived diagnostic data."""

    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("status") != "numerical diagnostic; not used in any proof":
        raise ValueError("unexpected status in numerical data")
    return payload


def plot_exit_gap(ax: plt.Axes, payload: dict[str, object]) -> None:
    """Plot the movement of the finite-section zero."""

    panel = payload["left_panel"]
    parameters = payload["parameters"]
    assert isinstance(panel, dict) and isinstance(parameters, dict)
    nu = np.asarray(panel["nu_values"], dtype=float)
    curves = panel["exit_gap_curves"]
    roots = panel["roots"]
    assert isinstance(curves, dict) and isinstance(roots, dict)
    center = float(roots["zero"])
    scaled_nu = 1.0e3 * (nu - center)
    zeta_step = float(parameters["zeta_step"])

    styles = (
        ("minus", -zeta_step, BLUE, (0, (5, 2)), "o"),
        ("zero", 0.0, INK, "-", "s"),
        ("plus", zeta_step, ORANGE, (0, (2, 1.5)), "^"),
    )
    for key, zeta, color, line_style, marker in styles:
        zeta_label = r"$\zeta=0$" if zeta == 0.0 else rf"$\zeta={zeta:+.2f}$"
        ax.plot(
            scaled_nu,
            np.asarray(curves[key], dtype=float),
            color=color,
            linewidth=1.55,
            linestyle=line_style,
            label=zeta_label,
        )
        root_x = 1.0e3 * (float(roots[key]) - center)
        ax.plot(
            root_x,
            0.0,
            marker=marker,
            markersize=5.0,
            markerfacecolor="white",
            markeredgewidth=1.15,
            markeredgecolor=color,
            linestyle="none",
            zorder=5,
        )

    ax.axhline(0.0, color=GRAY, linewidth=0.75, zorder=0)
    ax.set_xlabel(r"$10^3[\nu-\widehat\nu_{\rm sec}(\delta,0;S)]$")
    ax.set_ylabel(r"outgoing gap $\widehat E_S$")
    ax.set_title(r"(a)  Finite-section zero", loc="left", fontweight="bold")
    ax.legend(loc="upper left", frameon=False, handlelength=2.5)
    ax.text(
        0.97,
        0.05,
        r"$\Pi_3\mathcal{F}_{\zeta R}=\Pi_3\mathcal{F}_0$"
        "\n(at the same history)",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        color=GRAY,
        fontsize=7.35,
    )
    ax.grid(axis="y", color=LIGHT_GRAY, linewidth=0.55, alpha=0.65)


def plot_response(ax: plt.Axes, payload: dict[str, object]) -> None:
    """Plot the normalized quotient and the coincident-delay control."""

    rows = payload["convergence_rows"]
    parameters = payload["parameters"]
    control = payload["coincident_delay_control"]
    assert isinstance(rows, list)
    assert isinstance(parameters, dict) and isinstance(control, dict)
    ordered = sorted(rows, key=lambda row: float(row["delta"]))
    delta = np.asarray([row["delta"] for row in ordered], dtype=float)
    quotient = np.asarray([row["quotient"] for row in ordered], dtype=float)
    predicted = float(parameters["predicted_coefficient"])
    control_value = float(control["quotient"])

    ax.plot(
        delta,
        quotient,
        color=BLUE,
        linewidth=1.65,
        marker="o",
        markersize=4.5,
        markerfacecolor="white",
        markeredgewidth=1.05,
        label=r"two distinct delays",
    )
    ax.axhline(
        predicted,
        color=INK,
        linewidth=1.15,
        linestyle=(0, (5, 2)),
        label=r"$\Lambda_3=-1/3$",
    )
    ax.plot(
        delta,
        np.full_like(delta, control_value),
        color=GREEN,
        linewidth=1.3,
        linestyle=(0, (2, 1.5)),
        marker="^",
        markersize=4.3,
        markerfacecolor="white",
        markeredgewidth=1.0,
        label=r"coincident-delay control",
    )
    ax.set_xlabel(r"$\delta$")
    ax.set_ylabel(r"$\widehat q_{\delta}$")
    ax.set_title(
        r"(b)  Normalized zero displacement", loc="left", fontweight="bold"
    )
    ax.set_xlim(0.0, 0.128)
    ax.set_ylim(-0.365, 0.035)
    ax.set_xticks([0.0, 0.02, 0.05, 0.08, 0.12])
    ax.legend(loc="center right", frameon=False, handlelength=2.5)
    ax.grid(axis="y", color=LIGHT_GRAY, linewidth=0.55, alpha=0.65)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    payload = load_payload(arguments.data)

    figure, axes = plt.subplots(1, 2, figsize=(7.05, 3.12))
    plot_exit_gap(axes[0], payload)
    plot_response(axes[1], payload)
    figure.subplots_adjust(left=0.085, right=0.985, bottom=0.18, top=0.92, wspace=0.31)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(arguments.output, bbox_inches="tight", pad_inches=0.02)
    plt.close(figure)


if __name__ == "__main__":
    main()
