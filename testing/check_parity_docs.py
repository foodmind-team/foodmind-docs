"""Fail documentation CI when client parity claims drift from the public API."""

from __future__ import annotations

import os
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
FORBIDDEN = (
    "backend has no recipe crud",
    "backend openapi has no /recipes",
    "account-scoped local recipe drafts",
    "stores recipe drafts locally",
    "android is blocked by compilation",
)


def operation_count(contract: str) -> int:
    methods = {"get", "post", "put", "patch", "delete", "head", "options"}
    path: str | None = None
    operations: set[tuple[str, str]] = set()
    for line in contract.splitlines():
        path_match = re.fullmatch(r"  (/[^:]+):\s*", line)
        if path_match:
            path = path_match.group(1)
            continue
        method_match = re.fullmatch(r"    ([a-z]+):\s*", line)
        if path and method_match and method_match.group(1) in methods:
            operations.add((method_match.group(1), path))
    return len(operations)


def main() -> None:
    markdown = list(ROOT.rglob("*.md"))
    current_guides = [path for path in markdown if "testing" not in path.relative_to(ROOT).parts]
    combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in current_guides)
    stale = [phrase for phrase in FORBIDDEN if phrase in combined]
    if stale:
        raise SystemExit(f"Stale parity statements found: {stale}")

    configured = os.environ.get("FOODMIND_BACKEND_OPENAPI")
    contract_path = Path(configured) if configured else WORKSPACE / "foodmind-backend/src/main/resources/openapi/openapi.yaml"
    if contract_path.is_file():
        count = operation_count(contract_path.read_text(encoding="utf-8"))
        if count != 84:
            raise SystemExit(f"Expected 84 backend operations, found {count}")

    parity_documents = [path for path in markdown if "parity" in path.name.lower() or "end-to-end" in path.name.lower()]
    if not any("84" in path.read_text(encoding="utf-8") for path in parity_documents):
        raise SystemExit("Parity documentation does not record the 84-operation contract total")
    print(f"Parity documentation check passed ({len(markdown)} Markdown files).")


if __name__ == "__main__":
    main()
