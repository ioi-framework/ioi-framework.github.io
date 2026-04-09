---
inst_id:        INST-003
title:          "Windows LNK Instantiator"
artifact:       LNK
parser_tool:    LECmd
input_format:   CSV
output:         JSON-LD
template:       lnk
script:         lnk_instantiator.py
contributor:    "@ioi-framework"
date_added:     2025-01-01
status:         Validated
python_version: "3.9+"
dependencies:
  - rdflib>=6.0
  - pandas>=1.3
notes:          "Extracts targetMftEntryNumber for cross-reference with $MFT entry numbers in IOI-011."
---

## Overview

Maps LECmd CSV output to CASE/UCO-compliant JSON-LD using `ioi-ext:WindowsLnkFacet` for LNK-specific properties. The critical field is `targetMftEntryNumber`, which enables cross-graph matching with the $MFT instantiator output by entry number.

## Input fields consumed

| CSV field (LECmd) | Mapped to | Notes |
|---|---|---|
| `SourceFile` | `observable:fileName` | LNK filename |
| `SourceCreated` | `observable:observableCreatedTime` | Shortcut creation time |
| `TargetCreated` | `ioi-ext:targetCreatedTime` | Target file creation as recorded in LNK |
| `TargetMFTEntryNumber` | `ioi-ext:targetMftEntryNumber` | Cross-reference key with $MFT |
| `LocalPath` | `ioi-ext:targetFilePath` | |

## Usage

```bash
python3 instantiators/lnk_instantiator.py cases/data/AF-NNN/post-manipulation/lnk_post.csv cases/data/AF-NNN/graphs/lnk_case.jsonld
```
