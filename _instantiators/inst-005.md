---
inst_id:        INST-005
title:          "Office XML Metadata Instantiator"
artifact:       Office core.xml
parser_tool:    7-Zip
input_format:   XML
output:         JSON-LD
template:       office_xml_template.jsonld
script:         office_instantiator.py
contributor:    "@ioi-framework"
date_added:     2025-01-01
status:         Validated
python_version: "3.9+"
dependencies:
  - rdflib>=6.0
notes:          "Extracts docProps/core.xml from .docx/.xlsx/.pptx packages. Uses ioi-ext:OfficeXmlMetadataFacet for dcterms:created and dcterms:modified."
---

## Overview

Extracts `docProps/core.xml` from Office Open XML packages and maps `dcterms:created` and `dcterms:modified` to CASE/UCO-compliant JSON-LD using `ioi-ext:OfficeXmlMetadataFacet`. Used by IoI rule IOI-012.

## Input

The script accepts either a `.docx`/`.xlsx`/`.pptx` file directly (it extracts `docProps/core.xml` internally using Python's `zipfile` module — no dependency on 7-Zip at runtime) or a pre-extracted `core.xml` file.

## Input fields consumed

| XML element | Mapped to | Notes |
|---|---|---|
| `dcterms:created` | `ioi-ext:dctermsCreated` | ISO-8601 |
| `dcterms:modified` | `ioi-ext:dctermsModified` | ISO-8601 |
| `dc:creator` | `observable:creator` | |
| `cp:lastModifiedBy` | `ioi-ext:lastModifiedBy` | Optional |

## Usage

```bash
# From a .docx file directly
python instantiators/code/office_instantiator.py \
  --input  path/to/document.docx \
  --output cases/data/AF-NNN/graphs/office_case.jsonld \
  --graph-iri http://ioi/office_caseN

# From a pre-extracted core.xml
python instantiators/code/office_instantiator.py \
  --input  path/to/core.xml \
  --xml-only \
  --output cases/data/AF-NNN/graphs/office_case.jsonld \
  --graph-iri http://ioi/office_caseN
```

## Implementation note

AF-012 was evaluated with the Office XML and MFT graphs loaded into separate named graphs and joined at query time. An alternative is to materialize MFT properties into the Office graph during instantiation — this trades query complexity for instantiation complexity and is supported by passing `--mft-csv` to the script.
