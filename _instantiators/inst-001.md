---
inst_id:        INST-001
title:          "NTFS $MFT Instantiator"
artifact:       $MFT
parser_tool:    MFTECmd
input_format:   CSV
output:         JSON-LD
template:       mft
script:         mft_instantiator.py
contributor:    "@ioi-framework"
date_added:     2025-01-01
status:         Validated
python_version: "3.9+"
dependencies:
  - rdflib>=6.0
  - pandas>=1.3
notes:          "Handles both $MFT record-level fields ($SI and $FN timestamps, entry number, parent path) and extended attributes used by IoI rules IOI-011 and IOI-012."
---

## Overview

Maps MFTECmd CSV output to CASE/UCO-compliant JSON-LD graphs using `ioi-ext:MftFacet` for filesystem-specific properties not covered by the core CASE/UCO vocabulary.

## Input fields consumed

| CSV field (MFTECmd) | Mapped to | Notes |
|---|---|---|
| `EntryNumber` | `ioi-ext:entryNumber` | Used for LNK cross-reference |
| `ParentPath` | `ioi-ext:parentPath` | Used for VSS and IndexedDB path checks |
| `FileName` | `observable:fileName` | |
| `FilePath` | `observable:filePath` | |
| `Created0x10` | `ioi-ext:created0x10` | $SI creation timestamp |
| `Created0x30` | `ioi-ext:created0x30` | $FN creation timestamp |
| `LastModified0x10` | `ioi-ext:lastModified0x10` | |
| `LastModified0x30` | `ioi-ext:lastModified0x30` | |

## Usage

```bash
python instantiators/mft_instantiator.py \
  --input  cases/data/AF-NNN/post-manipulation/mft_post.csv \
  --output cases/data/AF-NNN/graphs/mft_case.jsonld \
  --graph-iri http://ioi/mft_caseN
```

For large $MFT exports use `--chunk-size N` (e.g. `--chunk-size 5000`) to split output into multiple JSON-LD files.

## Output structure

Produces one `observable:File` node per MFT record, each with an `observable:FileFacet` and an `ioi-ext:MftFacet`. Records are serialized as a JSON-LD `@graph` array.
