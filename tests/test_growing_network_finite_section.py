"""Regression checks for the growing-network finite-section diagnostic."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pytest

from canard_control.growing_network_finite_section import (
    GrowingNetworkParameters,
    exact_fold_rhs,
    growing_direction,
    network_objects,
    network_size_row,
    projected_rhs_difference,
)


REPOSITORY = Path(__file__).resolve().parents[1]
ARCHIVE = (
    REPOSITORY
    / "experiments"
    / "results"
    / "growing_network_finite_section_diagnostic.json"
)
NODE_COUNTS = (3, 5, 9, 17, 33)


@pytest.mark.parametrize("node_count", NODE_COUNTS)
def test_growing_family_has_exact_uniform_identities(node_count: int) -> None:
    parameters = GrowingNetworkParameters(node_count=node_count, delta=0.02)
    direction = growing_direction(node_count)
    _, curvature, graph_coefficient = network_objects(parameters)

    assert np.mean(direction) == pytest.approx(0.0, abs=2.0e-15)
    assert np.mean(direction**2) == pytest.approx(1.0, abs=2.0e-15)
    assert np.all(np.diff(direction) > 0.0)
    assert np.min(curvature) > 0.0
    assert np.mean(curvature) == pytest.approx(1.0, abs=2.0e-15)
    assert np.mean(graph_coefficient) == pytest.approx(0.0, abs=2.0e-15)
    assert parameters.dobrushin_coefficient == 0.0
    assert parameters.predicted_coefficient == pytest.approx(-0.5)
    assert parameters.singular_center == pytest.approx(-0.1875)


def test_projection_invisibility_uses_two_distinct_delayed_histories() -> None:
    parameters = GrowingNetworkParameters(node_count=5, delta=0.02)
    direction = growing_direction(parameters.node_count)
    current = np.concatenate(([0.2, -0.3], 0.03 * direction))
    delayed_0 = np.concatenate(([-0.1, 0.2], -0.02 * direction))
    delayed_1 = np.concatenate(([-0.25, 0.35], 0.01 * direction))

    residual = projected_rhs_difference(
        current,
        (delayed_0, delayed_1),
        parameters=parameters,
        zeta=0.04,
        nu=parameters.singular_center,
    )
    assert residual < 2.0e-14


def test_structured_rhs_agrees_with_dense_matrix_formula() -> None:
    parameters = GrowingNetworkParameters(
        node_count=7,
        delta=0.03,
        rho=0.6,
        sigma=0.4,
        diffusion=1.3,
        coupling_gain=1.7,
    )
    rng = np.random.default_rng(42)
    current = rng.normal(size=parameters.node_count + 2)
    delayed_states = (
        rng.normal(size=parameters.node_count + 2),
        rng.normal(size=parameters.node_count + 2),
    )
    zeta = 0.027
    nu = -0.11

    direction, curvature, graph_coefficient = network_objects(parameters)
    node_count = parameters.node_count
    stationary = np.ones(node_count) / node_count
    collective = np.ones((node_count, node_count)) / node_count
    markov = (1.0 - parameters.rho) * np.eye(node_count) + (
        parameters.rho * collective
    )
    transverse_projection = np.eye(node_count) - collective
    transverse_generator = parameters.diffusion * (markov - np.eye(node_count))
    chart_x, chart_y = current[:2]
    transverse = current[2:]
    graph_state = graph_coefficient * chart_x**2 + transverse
    delayed_collective = np.zeros(node_count)
    delayed_graph = np.zeros(node_count)
    for sign, delayed in zip((1.0, -1.0), delayed_states, strict=True):
        layer = 0.5 * markov + sign * zeta * np.outer(
            direction, stationary
        )
        delayed_x = delayed[0]
        delayed_graph_state = (
            graph_coefficient * delayed_x**2 + delayed[2:]
        )
        delayed_collective += (
            layer @ np.ones(node_count) * (chart_x - delayed_x)
        )
        delayed_graph += layer @ (graph_state - delayed_graph_state)

    delta = parameters.delta
    beta = parameters.beta
    coupling_gain = parameters.coupling_gain
    chart_x_prime = (
        chart_y
        - chart_x**2
        + delta
        * (
            -2.0 * chart_x * (stationary @ (curvature * graph_state))
            - beta * chart_x**3 / 3.0
            + coupling_gain * (stationary @ delayed_collective)
        )
        + delta**2
        * (
            -(stationary @ (curvature * graph_state**2))
            + coupling_gain * (stationary @ delayed_graph)
        )
        - delta**3 * beta * chart_x * (stationary @ graph_state**2)
        - delta**4 * beta * (stationary @ graph_state**3) / 3.0
    )
    chart_y_prime = -chart_x + delta * nu
    transverse_prime = (
        transverse_generator @ transverse
        + delta
        * (
            transverse_projection
            @ (
                -2.0 * chart_x * curvature * graph_state
                + coupling_gain * delayed_collective
            )
            - 2.0 * graph_coefficient * chart_x * chart_x_prime
        )
        + delta**2
        * (
            transverse_projection
            @ (
                -curvature * graph_state**2
                - beta * chart_x**2 * graph_state
                + coupling_gain * delayed_graph
            )
        )
        - delta**3
        * beta
        * chart_x
        * (transverse_projection @ graph_state**2)
        - delta**4
        * beta
        * (transverse_projection @ graph_state**3)
        / 3.0
    ) / delta
    dense_result = np.concatenate(
        ([chart_x_prime, chart_y_prime], transverse_prime)
    )

    structured_result = exact_fold_rhs(
        current,
        delayed_states,
        parameters=parameters,
        zeta=zeta,
        nu=nu,
    )
    np.testing.assert_allclose(structured_result, dense_result, atol=2.0e-14)


def test_small_growing_network_run_has_predicted_sign_and_scale() -> None:
    row = network_size_row(
        node_count=3,
        delta=0.02,
        section_half_width=3.5,
        zeta_step=0.04,
        rtol=2.0e-7,
        atol=2.0e-9,
        max_step=0.12,
        root_xtol=2.0e-7,
        root_rtol=2.0e-7,
    )
    assert -0.51 < row.quotient < -0.49
    assert row.root_residual_max < 2.0e-6
    assert row.transverse_mean_max < 1.0e-9


def test_archived_values_preserve_scope_uniformity_and_provenance() -> None:
    payload = json.loads(ARCHIVE.read_text(encoding="utf-8"))

    assert payload["status"] == "numerical diagnostic; not used in any proof"
    assert payload["parameters"]["node_counts"] == list(NODE_COUNTS)
    assert payload["parameters"]["theta_0"] == 1.0
    assert payload["parameters"]["theta_1"] == 2.0
    assert payload["parameters"]["predicted_coefficient"] == pytest.approx(-0.5)
    assert "D_N^fin" in payload["definition"]["not_computed"]
    assert "heteroclinic connection" in payload["definition"]["not_computed"]

    rows = payload["network_size_rows"]
    assert [row["node_count"] for row in rows] == list(NODE_COUNTS)
    assert all(row["predicted_coefficient"] == pytest.approx(-0.5) for row in rows)
    assert all(abs(row["quotient"] + 0.5) < 0.01 for row in rows)
    assert payload["checks"]["quotient_spread"] < 2.0e-4
    assert payload["checks"]["maximum_root_residual"] < 2.0e-8
    assert payload["checks"]["maximum_projection_rhs_residual"] < 2.0e-14
    assert payload["checks"]["maximum_transverse_mean"] < 2.0e-12

    for relative, expected in payload["source_sha256"].items():
        digest = hashlib.sha256((REPOSITORY / relative).read_bytes()).hexdigest()
        assert digest == expected
