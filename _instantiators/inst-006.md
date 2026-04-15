---
inst_id:        INST-006
title:          "Chrome Browser History Instantiator"
artifact:       Chrome History
parser_tool:    SQLite export / Autopsy plugin
input_format:   JSON
output:         JSON-LD
template:       browser_history
script:         history_instantiator.py
contributor:    "@ioi-framework"
date_added:     2026-04-15
status:         Validated
python_version: "3.9+"
dependencies:
  - rdflib>=6.0
notes:          "Consumes the same urls/visits JSON contract produced internally by the Autopsy plugin. Manual users can create that JSON from a copied Chrome History SQLite database with SCRIPTS/export_chrome_history.py."
---

## Overview

Maps Chrome History URL and visit records to CASE/UCO-compliant JSON-LD using the browser-history template snippets under `instantiators/templates/browser_history/`. This instantiator is used by IOI-002 to represent Chrome History evidence separately from IndexedDB filesystem evidence and USN modification evidence.

The Autopsy plugin performs the SQLite-to-JSON export internally before invoking this instantiator. Manual users can run the same flow explicitly with `SCRIPTS/export_chrome_history.py`.

## Input contract

The instantiator expects a JSON object with `urls` and `visits` arrays:

```json
{
  "urls": [
    {
      "id": 1,
      "url": "https://example.com",
      "title": "Example",
      "visit_count": 3,
      "typed_count": 1,
      "last_visit_datetime": "2026-04-15 10:00:00"
    }
  ],
  "visits": [
    {
      "id": 10,
      "url": 1,
      "visit_datetime": "2026-04-15 10:00:00",
      "visit_duration": 2000000,
      "transition": 1,
      "from_visit": 0
    }
  ]
}
```

## Input fields consumed

| JSON field | Mapped to | Notes |
|---|---|---|
| `urls[].url` | `observable:fullValue` | URL resource value used by IOI-002 domain matching |
| `urls[].title` | browser-history entry title | Preserved as page title metadata |
| `urls[].visit_count` | visit count | Stored as integer metadata |
| `urls[].typed_count` | typed count | Stored as integer metadata |
| `urls[].last_visit_datetime` | last visit timestamp | Accepts Chrome WebKit timestamps or string timestamps |
| `visits[].visit_datetime` | visit timestamp | Serialized as a visit facet timestamp |
| `visits[].visit_duration` | visit duration | Converted from microseconds to seconds |
| `visits[].transition` | transition type | Normalized from Chrome transition integer to label |
| `visits[].from_visit` | referring visit | Optional link to prior visit |

## Usage

Autopsy path:

```bash
# The Autopsy plugin exports Chrome History SQLite to this JSON shape internally.
python3 instantiators/history_instantiator.py history.json outputs/history_filled.jsonld
```

Manual path:

```bash
python3 SCRIPTS/export_chrome_history.py "/path/to/History" outputs/history.json
python3 instantiators/history_instantiator.py outputs/history.json outputs/history_filled.jsonld
python3 SCRIPTS/convert_to_ntriples.py outputs/history_filled.jsonld outputs/history_case.nt
```

## Output structure

Produces URL resource nodes, browser history entry nodes, and visit nodes in a JSON-LD `@graph`. The output is loaded into a browser-history named graph and joined by IOI-002 with MFT-derived IndexedDB paths and USN History-file modification records.
