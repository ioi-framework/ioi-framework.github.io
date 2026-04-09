---
inst_id:        INST-005
title:          "Office XML Metadata Instantiator"
artifact:       Office core.xml
parser_tool:    Python zipfile
input_format:   JSON
output:         JSON-LD
template:       office_xml
script:         office_xml_instantiator.py
contributor:    "@ioi-framework"
date_added:     2025-01-01
status:         Validated
python_version: "3.9+"
dependencies:
  - rdflib>=6.0
notes:          "Consumes merged JSON from ArtifactExporter and emits a single CASE/UCO graph combining filesystem timestamps with embedded Office metadata for IOI-012."
---

## Overview

Consumes the merged JSON produced by ArtifactExporter for the `office_xml` artifact. Each record already contains filesystem timestamps from Autopsy together with embedded `docProps/core.xml` metadata, allowing IOI-012 to compare the tampered filesystem view with the authentic Office metadata in a single JSON-LD graph.

## Input

Requires a single merged JSON file produced by ArtifactExporter. Each record contains both filesystem timestamps and extracted Office XML metadata for one Office document.

```json
[
  {
    "filename": "report.docx",
    "filepath": "C:/Users/.../report.docx",
    "fs_created": "2025-03-04T10:15:43Z",
    "xml_created": "2025-03-04T01:10:37Z"
  }
]
```

## Input fields consumed

| Source | Field | Mapped to |
|---|---|---|
| merged JSON | `fs_created` / `fs_modified` / `fs_accessed` / `fs_changed` | `observable:observableCreatedTime` / `observable:modifiedTime` / `observable:accessedTime` / `observable:metadataChangeTime` |
| merged JSON | `xml_created` | `ioi-ext:created` |
| merged JSON | `xml_modified` | `ioi-ext:modified` |
| merged JSON | `xml_creator` | `ioi-ext:creator` |
| merged JSON | `xml_last_modified_by` | `ioi-ext:lastModifiedBy` |

## Usage

```bash
python3 instantiators/office_xml_instantiator.py cases/data/AF-012/office_xml_merged.json cases/data/AF-012/graphs/office_case.jsonld
```

The merged JSON is produced upstream by ArtifactExporter using the `office_xml` export strategy.

## Implementation note

AF-012 was evaluated with the Office XML and MFT graphs loaded into separate named graphs and joined at query time via a SPARQL cross-graph join on `observable:filePath`.
