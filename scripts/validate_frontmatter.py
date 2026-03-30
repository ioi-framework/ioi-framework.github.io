#!/usr/bin/env python3
"""
validate_frontmatter.py
Validates Jekyll front matter for all _cases/, _rules/, and _instantiators/ files.
Run locally before pushing: python scripts/validate_frontmatter.py
Also runs in CI on every PR.
"""

import os
import sys
import yaml
from datetime import datetime
from pathlib import Path

# ── Schema definitions ─────────────────────────────────────────────────────

STANDARD_ARTIFACTS = {
    "$MFT", "$UsnJrnl", "$LogFile", "Security.evtx", "System.evtx",
    "LNK", "Prefetch", "Chrome History", "Firefox History",
    "Registry", "Office core.xml", "IndexedDB", "SQLite DB",
}

VALID_CATEGORIES = {"Temporal", "Structural", "Semantic"}
VALID_STATUSES   = {"Community", "Validated", "Deprecated"}

CASE_REQUIRED = [
    "case_id", "title", "category", "status",
    "description", "artifacts", "contributor", "date_added",
]

RULE_REQUIRED = [
    "rule_id", "title", "category", "status",
    "description", "artifacts", "invariant",
    "sparql_file", "contributor", "date_added",
]

INST_REQUIRED = [
    "inst_id", "title", "artifact", "parser_tool",
    "input_format", "output", "template", "script",
    "contributor", "date_added",
]

COLLECTION_SCHEMA = {
    "_cases":         (CASE_REQUIRED, "case_id"),
    "_rules":         (RULE_REQUIRED, "rule_id"),
    "_instantiators": (INST_REQUIRED, "inst_id"),
}

# ── Helpers ────────────────────────────────────────────────────────────────

def parse_frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        return yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        return {"__parse_error__": str(e)}

def check_id_format(fm, id_field, path):
    """Case IDs: AF-NNN, Rule IDs: IOI-NNN, Inst IDs: INST-NNN"""
    val = str(fm.get(id_field, ""))
    prefixes = {"case_id": "AF-", "rule_id": "IOI-", "inst_id": "INST-"}
    prefix = prefixes.get(id_field, "")
    if not val.startswith(prefix):
        return [f"  {id_field} '{val}' must start with '{prefix}'"]
    return []

def check_date(fm, path):
    d = fm.get("date_added", "")
    try:
        datetime.strptime(str(d), "%Y-%m-%d")
        return []
    except Exception:
        return [f"  date_added '{d}' must be YYYY-MM-DD"]

def check_artifacts(fm, path):
    arts = fm.get("artifacts", [])
    if not isinstance(arts, list):
        return ["  artifacts must be a list"]
    unknown = [a for a in arts if a not in STANDARD_ARTIFACTS]
    if unknown:
        return [
            f"  Non-standard artifact name(s): {unknown}",
            f"  Allowed: {sorted(STANDARD_ARTIFACTS)}",
        ]
    return []

def check_sparql_file(fm, root, path):
    sf = fm.get("sparql_file")
    if not sf:
        return []
    sparql_path = root / "rules" / "sparql" / sf
    if not sparql_path.exists():
        return [f"  sparql_file '{sf}' not found at {sparql_path}"]
    return []

def check_script(fm, root, path):
    sc = fm.get("script")
    if not sc:
        return []
    script_path = root / "instantiators" / "code" / sc
    if not script_path.exists():
        return [f"  script '{sc}' not found at {script_path}"]
    return []

# ── Main validation ────────────────────────────────────────────────────────

def validate_collection(collection_dir: Path, required_fields, id_field, root: Path):
    errors = {}
    ids_seen = {}

    for md_file in sorted(collection_dir.glob("*.md")):
        fm = parse_frontmatter(md_file)
        file_errors = []

        if fm is None:
            file_errors.append("  No front matter found (file must start with ---)")
            errors[str(md_file)] = file_errors
            continue

        if "__parse_error__" in fm:
            file_errors.append(f"  YAML parse error: {fm['__parse_error__']}")
            errors[str(md_file)] = file_errors
            continue

        # Required fields
        for field in required_fields:
            if field not in fm or fm[field] in (None, ""):
                file_errors.append(f"  Missing required field: '{field}'")

        # Category
        cat = fm.get("category")
        if cat and cat not in VALID_CATEGORIES:
            file_errors.append(f"  category '{cat}' must be one of {VALID_CATEGORIES}")

        # Status
        status = fm.get("status")
        if status and status not in VALID_STATUSES:
            file_errors.append(f"  status '{status}' must be one of {VALID_STATUSES}")

        # ID format
        file_errors += check_id_format(fm, id_field, md_file)

        # Duplicate ID check
        id_val = fm.get(id_field)
        if id_val:
            if id_val in ids_seen:
                file_errors.append(
                    f"  Duplicate {id_field} '{id_val}' — also in {ids_seen[id_val]}"
                )
            ids_seen[id_val] = str(md_file)

        # Date format
        file_errors += check_date(fm, md_file)

        # Artifact name check (cases and rules)
        if "artifacts" in fm:
            file_errors += check_artifacts(fm, md_file)

        # Linked file existence
        file_errors += check_sparql_file(fm, root, md_file)
        file_errors += check_script(fm, root, md_file)

        if file_errors:
            errors[str(md_file)] = file_errors

    return errors

def main():
    root = Path(__file__).parent.parent
    total_errors = {}

    for folder, (required, id_field) in COLLECTION_SCHEMA.items():
        col_dir = root / folder
        if not col_dir.exists():
            print(f"[SKIP] {folder}/ not found — skipping")
            continue
        errs = validate_collection(col_dir, required, id_field, root)
        total_errors.update(errs)

    if not total_errors:
        files_checked = sum(
            len(list((root / f).glob("*.md")))
            for f in COLLECTION_SCHEMA
            if (root / f).exists()
        )
        print(f"✓ All {files_checked} front-matter file(s) valid.")
        sys.exit(0)
    else:
        print(f"✗ Front-matter validation failed ({len(total_errors)} file(s)):\n")
        for filepath, errs in total_errors.items():
            print(f"{filepath}")
            for e in errs:
                print(e)
            print()
        sys.exit(1)

if __name__ == "__main__":
    main()
