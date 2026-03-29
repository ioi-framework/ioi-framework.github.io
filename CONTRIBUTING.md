# Contributing to the IoI Framework

Thank you for contributing. This document explains how to add new cases, IoI rules, and Template Instantiators to the repository. All contributions go through a Pull Request and are peer-reviewed before being merged.

---

## Repository structure at a glance

```
_cases/               Case pages (one .md per scenario)
_rules/               IoI rule pages (one .md per rule)
_instantiators/       Template Instantiator pages (one .md per parser)
cases/data/           Artifact datasets (CSV/JSON/JSONLD per case)
rules/sparql/         SPARQL .rq files (one per rule)
instantiators/code/   Python instantiator scripts
templates/            Case-agnostic CASE/UCO JSON-LD templates
ontology/             ioi-ext.ttl namespace definitions
docs/                 Extended documentation
```

---

## What can I contribute?

| Contribution type   | Files to add                                                                 |
|---------------------|------------------------------------------------------------------------------|
| New anti-forensic case | `_cases/af-NNN.md` + `cases/data/AF-NNN/` folder                         |
| New IoI rule        | `_rules/ioi-NNN.md` + `rules/sparql/ioi-NNN.rq`                             |
| New instantiator    | `_instantiators/inst-NNN.md` + `instantiators/code/NNN_instantiator.py`     |
| New CASE/UCO template | `templates/NNN_template.jsonld`                                            |
| ioi-ext property    | Edit `ontology/ioi-ext.ttl` + update documentation                          |
| Documentation fix   | Edit files under `docs/`                                                     |

You can contribute one type in a single PR, or bundle a case + its rule + its instantiator together — that is encouraged.

---

## Case front-matter schema (`_cases/af-NNN.md`)

Every case file **must** include all required fields. Optional fields should be included where applicable.

```yaml
---
# ── Required ──────────────────────────────────────────────
case_id:      AF-NNN           # Sequential ID. Check existing cases first.
title:        "Short descriptive title"
category:     Temporal         # Temporal | Structural | Semantic
status:       Community        # Community | Validated | Deprecated
description:  "One sentence describing the anti-forensic action and contradiction signal."
artifacts:                     # List of artifact types involved (use standard names below)
  - $MFT
  - $UsnJrnl
contributor:  "@github-handle"
date_added:   YYYY-MM-DD

# ── Optional ───────────────────────────────────────────────
rule_link:    /rules/ioi-NNN/  # Link to corresponding IoI rule page
tags:                          # Free-form tags for filtering
  - timestamp-manipulation
os:           Windows 10       # Target OS and version
tools_used:                    # Anti-forensic tools used in scenario
  - timestomper.exe
---
```

**Standard artifact names** (use these exactly for consistent filtering):
`$MFT`, `$UsnJrnl`, `$LogFile`, `Security.evtx`, `System.evtx`, `LNK`, `Prefetch`, `Chrome History`, `Firefox History`, `Registry`, `Office core.xml`, `IndexedDB`, `SQLite DB`

---

## IoI rule front-matter schema (`_rules/ioi-NNN.md`)

```yaml
---
# ── Required ──────────────────────────────────────────────
rule_id:      IOI-NNN
title:        "Short descriptive title"
category:     Temporal         # Temporal | Structural | Semantic
status:       Community        # Community | Validated | Deprecated
description:  "One sentence describing what the rule detects."
artifacts:
  - $MFT
  - LNK
invariant:    "Human-readable statement of the expected invariant φ"
sparql_file:  ioi-NNN.rq       # filename under rules/sparql/
contributor:  "@github-handle"
date_added:   YYYY-MM-DD

# ── Optional ───────────────────────────────────────────────
case_link:    /cases/af-NNN/
version:      "1.0"
tested_on:
  - "Virtuoso 7.2"
  - "Apache Jena Fuseki 4.x"
notes: ""
---
```

---

## Instantiator front-matter schema (`_instantiators/inst-NNN.md`)

```yaml
---
# ── Required ──────────────────────────────────────────────
inst_id:      INST-NNN
title:        "Artifact type — e.g. NTFS $MFT Instantiator"
artifact:     $MFT              # Single artifact type this parser handles
parser_tool:  MFTECmd           # Upstream parser tool
input_format: CSV               # CSV | JSON | JSONL | SQLite | XML
output:       JSON-LD           # Always JSON-LD
template:     mft_template.jsonld  # Template file under templates/
script:       mft_instantiator.py  # Script under instantiators/code/
contributor:  "@github-handle"
date_added:   YYYY-MM-DD

# ── Optional ───────────────────────────────────────────────
status:       Community        # Community | Validated | Deprecated
python_version: "3.9+"
dependencies:
  - rdflib>=6.0
notes: ""
---
```

---

## Step-by-step: submitting a PR

### 1. Fork and branch

```bash
git clone https://github.com/ioi-framework/ioi-framework.git
cd ioi-framework
git checkout -b add/af-NNN-your-scenario-name
```

Use branch naming convention: `add/af-NNN-short-name`, `add/ioi-NNN-short-name`, `fix/...`, `docs/...`

### 2. Pick the next ID

Check the existing files:
```bash
ls _cases/    # → highest existing is af-012, so use af-013
ls _rules/    # → highest existing is ioi-012, so use ioi-013
```

### 3. Add your files

Follow the schemas above. Run the local validation script before pushing:

```bash
python scripts/validate_frontmatter.py
```

This checks all required fields are present and that artifact names match the standard vocabulary.

### 4. If adding a dataset

Place paired files under `cases/data/AF-NNN/`:

```
cases/data/AF-NNN/
├── baseline/               Raw parser output before manipulation
│   ├── mft_baseline.csv
│   └── usn_baseline.csv
├── post-manipulation/      Raw parser output after manipulation
│   ├── mft_post.csv
│   └── usn_post.csv
├── graphs/                 Instantiated JSON-LD knowledge graphs
│   ├── mft_case.jsonld
│   └── usn_case.jsonld
└── ground-truth.md         Invariant + violation specification
```

Datasets over 50 MB should be hosted externally (Zenodo, OSF, institutional repository) and linked from the case page rather than committed to the repository.

### 5. Open the Pull Request

Use the PR template (auto-loaded when you open a PR). Fill out every checkbox. Assign at least one reviewer from the maintainer team.

### 6. Review process

- Automated CI checks run first (schema validation, broken link check)
- A maintainer or community peer reviewer will review within 14 days
- Address any requested changes on the same branch
- Once approved, a maintainer merges and the site deploys automatically

---

## Status lifecycle

| Status      | Meaning                                                             |
|-------------|---------------------------------------------------------------------|
| `Community` | Contributed by a community member, not independently validated      |
| `Validated` | Independently reproduced or reviewed by the core maintainer team    |
| `Deprecated`| Superseded, known-broken, or no longer applicable                   |

To request promotion from `Community` to `Validated`, open a PR adding a `validation_note` field to the front matter and tagging a maintainer.

---

## Code of conduct

Be respectful. Forensic community contributions are expected to be grounded in evidence and reproducible. Do not submit signatures based on theoretical manipulation only — provide a ground-truth specification and, where possible, a paired dataset.
