---
inst_id:        INST-002
title:          "NTFS $UsnJrnl Instantiator"
artifact:       $UsnJrnl
parser_tool:    MFTECmd
input_format:   CSV
output:         JSON-LD
template:       usn
script:         usn_instantiator.py
contributor:    "@ioi-framework"
date_added:     2025-01-01
status:         Validated
python_version: "3.9+"
dependencies:
  - rdflib>=6.0
  - pandas>=1.3
notes:          "Parses $UsnJrnl:$J CSV output from MFTECmd. updateReasons field is a semicolon-delimited string; the instantiator preserves the full string for SPARQL CONTAINS() filtering."
---

## Overview

Maps MFTECmd `$UsnJrnl:$J` CSV output to CASE/UCO-compliant JSON-LD using `ioi-ext:UsnFacet` for USN-specific fields. Used by IoI rules IOI-002, IOI-004, and IOI-007.

## Input fields consumed

| CSV field (MFTECmd) | Mapped to | Notes |
|---|---|---|
| `FileName` | `observable:fileName` | |
| `UpdateReasons` | `ioi-ext:updateReasons` | Preserved as semicolon-delimited string |
| `UpdateTimestamp` | `ioi-ext:updateTimestamp` | ISO-8601 |
| `ParentPath` | `ioi-ext:parentPath` | |
| `EntryNumber` | `ioi-ext:entryNumber` | |

## Usage

```bash
python3 instantiators/usn_instantiator.py cases/data/AF-NNN/post-manipulation/usn_post.csv cases/data/AF-NNN/graphs/usn_case.jsonld

# For large USN exports
python3 instantiators/usn_instantiator.py cases/data/AF-NNN/post-manipulation/usn_post.csv cases/data/AF-NNN/graphs/usn_case.jsonld --chunk-size 5000
```

## Output structure

Produces one `observable:File` node per USN record with an `observable:FileFacet` and an `ioi-ext:UsnFacet`. Large $UsnJrnl exports can be split into chunks using `--chunk-size N` (e.g. `--chunk-size 5000`).
