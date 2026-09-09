"""Check the active Paper A source closure, without freezing editorial prose.

These checks detect broken source dependencies and references. Mathematical
identities and numerical regression are tested separately; none is a proof
of the RFDE theorems.
"""

from pathlib import Path
import re


REPOSITORY = Path(__file__).resolve().parents[1]
PAPER = REPOSITORY / "manuscript/network-root-transfer"


def without_comments(text: str) -> str:
    return re.sub(r"(?<!\\)%[^\n]*", "", text)


def active_sources() -> dict[Path, str]:
    pending = [PAPER / "main.tex"]
    seen = {}
    while pending:
        path = pending.pop()
        if path in seen:
            continue
        assert path.is_file(), f"Missing TeX input: {path}"
        text = without_comments(path.read_text())
        seen[path] = text
        for name in re.findall(r"\\input\{([^}]+)\}", text):
            child = PAPER / name
            pending.append(child if child.suffix else child.with_suffix(".tex"))
    return seen


def test_active_inputs_are_self_contained() -> None:
    for path in active_sources():
        assert path.is_relative_to(PAPER), f"External manuscript input: {path}"


def test_active_labels_are_unique_and_references_resolve() -> None:
    labels = {}
    sources = active_sources()
    for path, text in sources.items():
        for label in re.findall(r"\\label(?:\[[^]]*\])?\{([^}]+)\}", text):
            assert label not in labels, f"Duplicate {label}: {path}, {labels.get(label)}"
            labels[label] = path
    for path, text in sources.items():
        for group in re.findall(r"\\(?:[Cc]ref|[Ee]qref|ref|pageref)\*?\{([^}]+)\}", text):
            for label in group.split(","):
                assert label.strip() in labels, f"Unresolved {label.strip()} in {path}"


def test_citations_have_bibliography_entries() -> None:
    bibliography = (REPOSITORY / "references/references.bib").read_text()
    keys = set(re.findall(r"@\w+\s*\{\s*([^,\s]+)", bibliography))
    for path, text in active_sources().items():
        for group in re.findall(r"\\cite\w*\*?(?:\[[^]]*\])*\{([^}]+)\}", text):
            for key in group.split(","):
                assert key.strip() in keys, f"Missing citation {key.strip()} in {path}"


def test_active_graphics_are_supplied() -> None:
    for path, text in active_sources().items():
        for name in re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", text):
            assert (PAPER / name).is_file(), f"Missing figure {name} in {path}"
