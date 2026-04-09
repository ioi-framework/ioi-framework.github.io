---
inst_id:        INST-004
title:          "Windows Event Log (EVTX) Instantiator"
artifact:       Security.evtx
parser_tool:    EvtxECmd
input_format:   CSV
output:         JSON-LD
template:       evtx
script:         evtx_instantiator.py
contributor:    "@ioi-framework"
date_added:     2025-01-01
status:         Validated
python_version: "3.9+"
dependencies:
  - rdflib>=6.0
  - pandas>=1.3
notes:          "Designed for Security.evtx but the template generalises to any EVTX channel by changing the ioi-ext:channel value."
---

## Overview

Maps EvtxECmd CSV output to CASE/UCO-compliant JSON-LD using `observable:EventRecordFacet` for standard event fields and `ioi-ext:EventLogFacet` for channel metadata. Used by IoI rule IOI-007.

## Input fields consumed

| CSV field (EvtxECmd) | Mapped to | Notes |
|---|---|---|
| `EventId` | `observable:eventID` | Stored as string for SPARQL string-match |
| `TimeCreated` | `observable:startTime` | ISO-8601 |
| `Payload` | `observable:eventRecordText` | |
| `Channel` | `ioi-ext:channel` | e.g. `Security` |
| `Computer` | `ioi-ext:computer` | Optional |

## Usage

```bash
python3 instantiators/evtx_instantiator.py cases/data/AF-NNN/post-manipulation/security_post.jsonl cases/data/AF-NNN/graphs/security_case.jsonld
```
