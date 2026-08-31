"""Static release-contract tests for the Paper A submission architecture.

These tests prevent editorial regressions in what the manuscript claims and
where the complete-history argument lives.  They are not substitutes for the
mathematical proofs referenced below.
"""

from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]
PAPER = REPOSITORY / "manuscript" / "network-root-transfer"


def source(relative: str) -> str:
    return (REPOSITORY / relative).read_text(encoding="utf-8")


def compact(text: str) -> str:
    return " ".join(text.split())


def test_submission_split_keeps_one_flagship_model_in_main() -> None:
    main = source("manuscript/network-root-transfer/main.tex")
    supplement = source("manuscript/network-root-transfer/supplement.tex")

    assert "Projection-Blind Delay Redistribution" in main
    assert r"\input{sections/02d-anchored-physical-connection}" in main
    assert r"\input{sections/02b-sensed-recovery}" not in main
    assert r"\input{sections/02b-sensed-recovery}" not in supplement
    assert r"\input{sections/03c-anchor-local-toolkit}" in supplement
    assert r"\input{sections/03d-anchored-lean-proofs}" in supplement
    assert r"\input{sections/02c-unprepared-outer-skeleton}" not in supplement
    assert r"\input{sections/03c-outer-skeleton-and-nonselection}" not in supplement
    assert r"\input{sections/03d-anchored-physical-connection-proofs}" not in supplement
    assert r"\input{sections/03e-broken-lin-gluing}" not in supplement


def test_flagship_front_matter_states_the_fixed_model_root_and_boundary() -> None:
    main = source("manuscript/network-root-transfer/main.tex")
    introduction = source(
        "manuscript/network-root-transfer/sections/01-introduction.tex"
    )

    assert "exact complete-history heteroclinic canard" in main
    assert r"D_\eta\mu_c(\delta,\eta)" in main
    flat_main = compact(main)
    assert "Exact roots may differ between admissible global anchors" in flat_main
    assert "No maximal-canard claim is made for the unanchored" in flat_main
    assert r"\label[theorem]{thm:flagship-synthesis}" in introduction
    assert "same-full-history projection blindness" in introduction
    assert "Why the global anchor is not a preparation" in introduction


def test_anchored_statement_has_exact_membership_root_and_full_dual_jet() -> None:
    anchored = source(
        "manuscript/network-root-transfer/sections/02d-anchored-physical-connection.tex"
    )

    required = {
        r"\label[theorem]{thm:anchor-indices-manifolds}",
        r"\label[theorem]{thm:anchor-annulus-flat-forgetting}",
        r"\label[proposition]{prop:anchor-gap-comparison}",
        r"\label[theorem]{thm:anchored-physical-root-conormal}",
        r"\label[proposition]{prop:anchor-physical-naturality-composition}",
        r"\lim_{t\to-\infty}Z^{\rm het}_t=E_N^+",
        r"\lim_{t\to+\infty}Z^{\rm het}_t=E_N^-",
        "The derivative estimate holds in the full dual operator norm",
    }
    for item in required:
        assert item in anchored
    assert "exact finite-\\(\\delta\\) baselines may differ" in compact(anchored)


def test_lean_halfline_proof_keeps_the_non_circularity_contract() -> None:
    proof = source(
        "manuscript/network-root-transfer/sections/03d-anchored-lean-proofs.tex"
    )

    required = {
        r"\label[lemma]{lem:lean-anchor-history-objects}",
        r"\label[lemma]{lem:lean-anchor-generated-cut-sheets}",
        r"\label[lemma]{lem:lean-anchor-action-intersection}",
        r"\label[lemma]{lem:lean-anchor-gap-comparison}",
        r"\mathbb X_{bL}=\mathscr D_{bL}^{0;2}",
        r"\frac{\delta}{s_b^\#}E_b",
        "The finite graph is used only for comparison",
        "No history holonomy is inverted",
    }
    for item in required:
        assert item in proof

    toolkit = source(
        "manuscript/network-root-transfer/sections/03c-anchor-local-toolkit.tex"
    )
    assert "No small-curvature claim is made" in compact(proof)
    # The restored typed residual and two half-line ledgers fit in one
    # sub-1000-line proof spine; this guards against a return to the old ledger.
    assert len(proof.splitlines()) < 1000
    assert len(toolkit.splitlines()) < 900
    assert "No flat bound on the second derivative" in toolkit


def test_figure_and_notation_disclose_the_scope_boundary() -> None:
    caption = source("manuscript/network-root-transfer/figures/root-mechanism.tex")
    notation = source(
        "manuscript/network-root-transfer/sections/01a-notation-and-status.tex"
    )
    contract = source("docs/paper-a-flagship-figure-contract.md")

    assert "positions are not" in compact(caption)
    assert "No root for the unanchored law" in compact(caption)
    assert "equality across anchors" in compact(caption)
    assert "Exact roots for different anchors need not agree" in notation
    assert "The figure must not imply" in contract
