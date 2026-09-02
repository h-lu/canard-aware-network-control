"""Editorial and scope contract for the rewritten Paper A manuscript.

These checks guard the public claim architecture.  They do not replace any
analytic proof in the paper.
"""

from pathlib import Path
import re


REPOSITORY = Path(__file__).resolve().parents[1]
PAPER = REPOSITORY / "manuscript" / "network-root-transfer"


def source(relative: str) -> str:
    return (REPOSITORY / relative).read_text(encoding="utf-8")


def compact(text: str) -> str:
    return " ".join(text.split())


def visible_prose(text: str) -> str:
    """Drop labels and comments before checking reader-facing terminology."""
    lines = []
    for line in text.splitlines():
        if r"\label" in line:
            line = re.sub(r"\\label(?:\[[^]]*\])?\{[^}]*\}", "", line)
        line = line.split("%", 1)[0]
        lines.append(line)
    return compact("\n".join(lines)).lower()


def test_active_submission_uses_only_the_rewrite_sources() -> None:
    main = source("manuscript/network-root-transfer/main.tex")

    for name in (
        "01-introduction",
        "02-model-results",
        "03-fredholm-sensitivity",
        "04-fold-passage",
        "05-heteroclinic-connection",
        "06-scope-and-transfer",
    ):
        assert rf"\input{{rewrite-sections/{name}}}" in main
    assert r"\input{sections/" not in main
    assert r"\appendix" in main
    assert r"\input{appendices/01-fold-details}" in main
    assert r"\input{appendices/02-connection-details}" in main
    assert not (PAPER / "supplement.tex").exists()
    makefile = source("manuscript/network-root-transfer/Makefile")
    assert "supplement.tex" not in makefile


def test_front_matter_states_the_model_change_and_scope_boundary() -> None:
    main = compact(source("manuscript/network-root-transfer/main.tex"))

    assert "Sensitivity of Heteroclinic Connections" in main
    assert "fixed smooth modification outside the fold neighborhood" in main
    assert "global invariant-manifold and comparison properties are hypotheses" in main
    assert "does not prove a heteroclinic connection for the unmodified recovery equation" in main
    assert "does not by itself force the first variation of the collective solvability condition to vanish" in main
    assert "The theorem statements are analytic and do not rely on numerical data" in main
    assert "is not used in any proof" in main
    assert "research draft" not in main.lower()


def test_reusable_theorem_requires_an_exact_connection_defining_function() -> None:
    abstract_section = source(
        "manuscript/network-root-transfer/rewrite-sections/03-fredholm-sensitivity.tex"
    )
    scope = source(
        "manuscript/network-root-transfer/rewrite-sections/06-scope-and-transfer.tex"
    )
    abstract_compact = compact(abstract_section)

    required = {
        r"\label{thm:fredholm-reduction}",
        r"\label{thm:fredholm-heteroclinic-sensitivity}",
        r"G_N(\delta,\nu,\eta)=0",
        "heteroclinic orbit of the prescribed branch",
        "does not assert that a general RFDE automatically possesses",
    }
    for item in required:
        assert item in abstract_compact
    assert "additional hypothesis" in scope.lower()


def test_first_moment_and_fredholm_statements_have_separate_interfaces() -> None:
    introduction = compact(
        source("manuscript/network-root-transfer/rewrite-sections/01-introduction.tex")
    )
    model = compact(
        source("manuscript/network-root-transfer/rewrite-sections/02-model-results.tex")
    )
    scope = compact(
        source("manuscript/network-root-transfer/rewrite-sections/06-scope-and-transfer.tex")
    )

    assert r"\label{thm:rw-first-moment-map}" in model
    assert "Surjectivity and a sharp right inverse for the first delay moment" in model
    assert r"\label[corollary]{cor:rw-fold-fredholm-coefficient}" in model
    assert "Dimension-uniform Fredholm sensitivity functional for the" in model
    assert r"\label{eq:intro-full-factorization}" in introduction
    assert r"\ell_N\mathcal B_NA_N^{-1}\mathsf S_N" in introduction
    assert r"defining function \(G_{N,\delta}^{g}\) for the stable-manifold section" in scope
    assert r"finite-interval approximation \(D_N^{\rm fin}\)" not in scope


def test_model_connection_statement_is_explicitly_conditional() -> None:
    model = source(
        "manuscript/network-root-transfer/rewrite-sections/02-model-results.tex"
    )
    proof = source(
        "manuscript/network-root-transfer/rewrite-sections/05-heteroclinic-connection.tex"
    )
    model_compact = compact(model)

    required = {
        r"\label[corollary]{cor:rw-conditional-connection}",
        "Conditional heteroclinic connection for the modified RFDE",
        r"\dim W^u(Z_N^+)=1",
        r"\operatorname{codim}W^s(Z_N^-)=1",
        r"\norm{G_{N,\delta}^{g}-D_N^{\rm fin}}",
        r"D_\eta\mu_{c,N}^{g}",
        "No heteroclinic connection for the unmodified recovery equation",
        "does not establish the uniform global",
    }
    for item in required:
        assert item in model_compact
    assert r"G_{N,\delta}^{g}(\nu,\eta)=0" in proof
    assert r"W_{\rm in}^u(Z_N^+)\subset W^s(Z_N^-)" in proof
    assert "is not proved here" in proof


def test_active_reader_facing_sources_avoid_project_vocabulary() -> None:
    paths = [PAPER / "main.tex"]
    paths.extend(sorted((PAPER / "rewrite-sections").glob("*.tex")))
    paths.extend(sorted((PAPER / "appendices").glob("*.tex")))
    paths.append(PAPER / "figures" / "connection-geometry.tex")
    paths.append(PAPER / "figures" / "three-node-finite-section.tex")
    prose = " ".join(visible_prose(path.read_text(encoding="utf-8")) for path in paths)

    banned = (
        "flagship",
        "projection-blind",
        "hidden return",
        "hidden-return",
        "physical root",
        "physical gap",
        "response germ",
        "preparation template",
        "construction ledger",
        "proof ledger",
        "anchored rfde",
        "shared-resource",
        "exact connection",
        "exact root",
        "zero-fiber",
        "structural perturbation",
        "first-moment source",
        "returned forcing",
        "finite-endpoint rows",
        "root map",
    )
    for phrase in banned:
        assert phrase not in prose


def test_figure_discloses_projected_and_schematic_content() -> None:
    connection = compact(source("manuscript/network-root-transfer/figures/connection-geometry.tex"))
    connection_contract = source(
        "manuscript/network-root-transfer/figures/connection-geometry-contract.md"
    )

    assert "figure does not prove existence" in connection
    assert "collective coordinates" in connection.lower()
    assert "positions and distances are not quantitative" in connection.lower()
    assert "Status: `SCHEMATIC`" in connection_contract


def test_numerical_figure_is_scoped_as_a_finite_section_diagnostic() -> None:
    figure = compact(
        source("manuscript/network-root-transfer/figures/three-node-finite-section.tex")
    )
    contract = source(
        "manuscript/network-root-transfer/figures/three-node-finite-section-contract.md"
    )

    assert r"\widehat E_S=Y(S)-X(S)^2+1/2" in figure
    assert r"is not \(D_3^{\rm fin}\)" in figure
    assert "does not compute a heteroclinic connection or a maximal canard" in figure
    assert "Status: `MIXED`" in contract
