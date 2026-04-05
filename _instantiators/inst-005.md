---
inst_id:        INST-005
title:          "Office XML Metadata Instantiator"
artifact:       Office core.xml
parser_tool:    Python zipfile
input_format:   DOCX/XML
output:         JSON-LD
template:       office_xml
script:         office_xml_instantiator.py
contributor:    "@ioi-framework"
date_added:     2025-01-01
status:         Validated
python_version: "3.9+"
dependencies:
  - rdflib>=6.0
notes:          "Accepts .docx/.xlsx/.pptx files directly (extracts core.xml via Python zipfile) or pre-extracted folders. Joins MFT timestamps with core.xml metadata by filename for IOI-012 timestomping detection."
---

## Overview

Combines MFT timestamps with embedded Office XML metadata (`docProps/core.xml`) into a single CASE/UCO JSON-LD graph. Accepts `.docx`/`.xlsx`/`.pptx` files directly — extracts `core.xml` internally via Python's `zipfile` module, no external tools needed. Matches each document to its MFT record by filename, enabling the cross-source timestamp comparison used by IoI rule IOI-012.

## Input

Requires an MFT CSV (from MFTECmd) and a folder containing the Office documents. The folder can hold raw `.docx`/`.xlsx`/`.pptx` files — the script extracts `core.xml` internally. Pre-extracted subdirectory layout is also supported as a fallback.

```
office_folder/
  secret.docx        ← script reads core.xml directly from the zip
  report.xlsx
```

The script matches each document to its MFT record by filename, then combines both into one JSON-LD graph.

## Input fields consumed

| Source | Field | Mapped to |
|---|---|---|
| MFT CSV | `Created0x10` / `LastModified0x10` | `ioi-ext:created0x10` / `ioi-ext:lastModified0x10` |
| MFT CSV | `Created0x30` / `LastModified0x30` | `ioi-ext:created0x30` / `ioi-ext:lastModified0x30` |
| core.xml | `dcterms:created` | `ioi-ext:dctermsCreated` |
| core.xml | `dcterms:modified` | `ioi-ext:dctermsModified` |
| core.xml | `dc:creator` | `observable:creator` |

## Usage

```bash
python instantiators/office_xml_instantiator.py \
  cases/data/AF-012/mft_post.csv \
  cases/data/AF-012/office_docs/ \
  cases/data/AF-012/graphs/office_case.jsonld
```

Place the `.docx`/`.xlsx`/`.pptx` files in `office_docs/` — no extraction step needed.

## Implementation note

AF-012 was evaluated with the Office XML and MFT graphs loaded into separate named graphs and joined at query time via a SPARQL cross-graph join on `observable:filePath`.
