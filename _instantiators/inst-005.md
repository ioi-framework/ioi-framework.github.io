---
inst_id:        INST-005
title:          "Office XML Metadata Instantiator"
artifact:       Office core.xml
parser_tool:    Python zipfile
input_format:   JSON / Office document
output:         JSON-LD
template:       office_xml
script:         office_xml_instantiator.py
contributor:    "@ioi-framework"
date_added:     2025-01-01
status:         Validated
python_version: "3.9+"
dependencies:
  - rdflib>=6.0
notes:          "Supports merged-JSON and direct Office-document input. Emits a dedicated Office XML graph with source-specific metadata properties for IOI-012."
---

## Overview

Generates a CASE/UCO JSON-LD Office metadata graph for IOI-012. The instantiator supports two input modes:

1. **Merged JSON mode** — consumes the Autopsy/ArtifactExporter merged JSON for the `office_xml` artifact.
2. **Manual document mode** — reads a raw Office document (`.docx`, `.xlsx`, `.pptx`, and macro-enabled variants), extracts `docProps/core.xml`, and emits the same Office XML graph.

In both modes, the output contains an `ioi-ext:OfficeXMLFacet` plus an `observable:FileFacet`. Filesystem timestamps are intentionally excluded because IOI-012 compares the Office graph to a separate MFT graph using normalized `observable:filePath`.

## Input

### Merged JSON mode

```json
[
  {
    "filename": "password.docx",
    "filepath": "/Users/ktams/Desktop/Confidential/password.docx",
    "xml_created": "2025-03-04T01:09:00Z",
    "xml_modified": "2025-03-04T01:10:37Z",
    "xml_creator": "ktams",
    "xml_last_modified_by": "ktams"
  }
]
```

### Manual document mode

Provide a raw Office file and, when needed, the original MFT path via `--filepath` so the resulting `observable:filePath` matches the MFT graph used by IOI-012.

## Input fields consumed

| Source | Field | Mapped to |
|---|---|---|
| merged JSON / `core.xml` | `xml_created` | `ioi-ext:dctermsCreated` |
| merged JSON / `core.xml` | `xml_modified` | `ioi-ext:dctermsModified` |
| merged JSON / `core.xml` | `xml_creator` | `ioi-ext:dcCreator` |
| merged JSON / `core.xml` | `xml_last_modified_by` | `ioi-ext:cpLastModifiedBy` |
| merged JSON / manual input | `filename`, `filepath`, `extension`, `size` | `observable:FileFacet` fields |

## Usage

```bash
python3 instantiators/office_xml_instantiator.py office_xml_merged.json output.jsonld
```

```bash
python3 instantiators/office_xml_instantiator.py password.docx output.jsonld --filepath /Users/ktams/Desktop/Confidential/password.docx
```

If `--filepath` is omitted in manual mode, the script prompts for the original file path so the Office graph can still join to the MFT graph.

## Implementation note

AF-012 is evaluated with the Office XML and MFT graphs loaded into separate named graphs and joined at query time via a SPARQL cross-graph join on normalized `observable:filePath`. The current rule uses source-specific Office XML properties: `dctermsCreated`, `dctermsModified`, `dcCreator`, and `cpLastModifiedBy`.
