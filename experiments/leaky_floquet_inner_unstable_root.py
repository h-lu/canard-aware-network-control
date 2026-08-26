"""Generate the local inner leaky Floquet root certificate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from canard_control.leaky_floquet_inner_unstable_root import (
    RESULT_RELATIVE_PATH,
    build_leaky_inner_unstable_root_result,
    validate_leaky_inner_unstable_root_result,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=None)
    arguments = parser.parse_args()
    repository = Path(__file__).resolve().parents[1]
    payload = build_leaky_inner_unstable_root_result(repository)
    validate_leaky_inner_unstable_root_result(payload, repository)
    path = arguments.output or repository / RESULT_RELATIVE_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(path)


if __name__ == "__main__":
    main()
