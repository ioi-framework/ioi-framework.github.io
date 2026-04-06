---
layout: default
title: "Artifacts & Datasets"
description: "Download knowledge graphs, ground-truth documents, JSON-LD templates, Template Instantiators, and SPARQL IoI rules."
permalink: /artifacts/
---
<div class="page-wrap">
  <h1 class="page-title">Artifacts &amp; datasets</h1>
  <p class="page-subtitle">
    Ground truth documents, IoI rules, instantiators, and templates available at
    <a href="https://github.com/ioi-framework/ioi-framework" target="_blank" rel="noopener">github.com/ioi-framework/ioi-framework</a>.
  </p>

  <!-- Repository structure -->
  <div class="section-header" style="margin-bottom:1.25rem;">
    <h2>Repository structure</h2>
  </div>

  <pre style="font-size:0.78rem;line-height:1.9;margin-bottom:2rem;"><code>ioi-framework/
├── CASES/                        # Per-scenario datasets
│   ├── AF-002/
│   │   ├── data/                 # Artifact exports (CSV/JSON)
│   │   ├── graphs/               # Instantiated JSON-LD knowledge graphs
│   │   │   ├── mft_case.jsonld
│   │   │   ├── usn_case.jsonld
│   │   │   └── history_case.jsonld
│   │   ├── ground_truth.md       # Invariant + violation specification
│   │   └── README.md
│   ├── AF-004/  ...
│   ├── AF-007/  ...
│   ├── AF-011/  ...
│   └── AF-012/
│       ├── data/
│       ├── graphs/
│       │   ├── office_case.jsonld
│       │   └── mft_case.jsonld
│       └── ground_truth.md
│
├── TEMPLATES/                    # Case-agnostic CASE/UCO templates
│   ├── mft/
│   ├── usn/
│   ├── lnk/
│   ├── evtx/
│   ├── browser_history/
│   └── office_xml/
│
├── instantiators/                # Template Instantiator scripts
│   ├── mft_instantiator.py
│   ├── usn_instantiator.py
│   ├── lnk_instantiator.py
│   ├── evtx_instantiator.py
│   ├── office_xml_instantiator.py
│   └── templates/                # Templates used by instantiators
│
├── RULES/                        # IoI SPARQL signatures (.rq files)
│   ├── semantic/
│   │   └── IOI-002_chrome_history_missing.rq
│   ├── structural/
│   │   └── IOI-004_vss_traces_missing.rq
│   └── temporal/
│       ├── IOI-007_usn_clear_before_event.rq
│       ├── IOI-011_lnk_mft_mismatch.rq
│       └── IOI-012_office_mft_mismatch.rq
│
├── SCRIPTS/
│   └── convert_to_ntriples.py    # JSON-LD → N-Triples conversion
│
└── ontologies/
    └── ioi-ext.ttl               # ioi-ext namespace definitions</code></pre>

  <!-- Artifact types -->
  <div class="section-header" style="margin-bottom:1.25rem;">
    <h2>What each folder contains</h2>
  </div>

  <div class="card-grid" style="grid-template-columns:repeat(auto-fill,minmax(260px,1fr));margin-bottom:2rem;">

    <div class="card">
      <div class="card-tag">CASES/</div>
      <h3>Scenario datasets</h3>
      <p>Artifact exports (CSV/JSON) for all five scenarios, instantiated JSON-LD knowledge graphs ready for loading into Virtuoso, and per-scenario ground truth documents.</p>
    </div>

    <div class="card">
      <div class="card-tag">TEMPLATES/</div>
      <h3>CASE/UCO templates</h3>
      <p>Case-agnostic JSON-LD templates defining the facet structures referenced by IoI rules. Organised by artifact type. Use as the starting point for new Template Instantiators.</p>
    </div>

    <div class="card">
      <div class="card-tag">instantiators/</div>
      <h3>Template Instantiators</h3>
      <p>Python scripts that map artifact-specific parser CSV output to CASE/UCO template structures, producing case-specific JSON-LD graphs for each scenario.</p>
    </div>

    <div class="card">
      <div class="card-tag">RULES/</div>
      <h3>IoI SPARQL rules</h3>
      <p>All five IoI signatures as <code>.rq</code> files, organised by category (semantic, structural, temporal). Substitute named graph IRIs and execute via <code>isql</code> or any SPARQL 1.1 endpoint.</p>
    </div>

    <div class="card">
      <div class="card-tag">CASES/*/ground_truth.md</div>
      <h3>Ground-truth documents</h3>
      <p>Per-scenario specifications describing affected artifacts, expected invariants, and violation predicates as pseudo-query logic — the human-readable counterpart to each IoI rule.</p>
    </div>

    <div class="card">
      <div class="card-tag">ontologies/</div>
      <h3>ioi-ext ontology</h3>
      <p>Turtle definitions for the <code>ioi-ext:</code> namespace, covering artifact-specific properties not expressible in the core CASE/UCO vocabulary (e.g., MFT entry numbers, USN update reasons, LNK target metadata).</p>
    </div>

  </div>

  <!-- Scenario download table -->
  <div class="section-header" style="margin-bottom:1.25rem;">
    <h2>Per-scenario artifact summary</h2>
  </div>

  <div class="prose">
    <table>
      <thead>
        <tr>
          <th>Case</th>
          <th>Artifacts</th>
          <th>Total triples</th>
          <th>JSON-LD graphs</th>
          <th>Ground truth</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><a href="/cases/af-002/">AF-002</a></td>
          <td>$MFT, $UsnJrnl, Chrome History</td>
          <td>24,042,852</td>
          <td>3</td>
          <td><a href="https://github.com/ioi-framework/ioi-framework/blob/main/CASES/AF-002/ground_truth.md" target="_blank" rel="noopener">ground_truth.md ↗</a></td>
        </tr>
        <tr>
          <td><a href="/cases/af-004/">AF-004</a></td>
          <td>$MFT, $UsnJrnl</td>
          <td>21,004,830</td>
          <td>2</td>
          <td><a href="https://github.com/ioi-framework/ioi-framework/blob/main/CASES/AF-004/ground_truth.md" target="_blank" rel="noopener">ground_truth.md ↗</a></td>
        </tr>
        <tr>
          <td><a href="/cases/af-007/">AF-007</a></td>
          <td>Security.evtx, $UsnJrnl</td>
          <td>5,922,784</td>
          <td>2</td>
          <td><a href="https://github.com/ioi-framework/ioi-framework/blob/main/CASES/AF-007/ground_truth.md" target="_blank" rel="noopener">ground_truth.md ↗</a></td>
        </tr>
        <tr>
          <td><a href="/cases/af-011/">AF-011</a></td>
          <td>LNK, $MFT</td>
          <td>18,385,659</td>
          <td>2</td>
          <td><a href="https://github.com/ioi-framework/ioi-framework/blob/main/CASES/AF-011/ground_truth.md" target="_blank" rel="noopener">ground_truth.md ↗</a></td>
        </tr>
        <tr>
          <td><a href="/cases/af-012/">AF-012</a></td>
          <td>Office core.xml, $MFT</td>
          <td>18,383,783</td>
          <td>2</td>
          <td><a href="https://github.com/ioi-framework/ioi-framework/blob/main/CASES/AF-012/ground_truth.md" target="_blank" rel="noopener">ground_truth.md ↗</a></td>
        </tr>
      </tbody>
    </table>
  </div>

  <div style="margin-top:2rem;padding:1.1rem 1.25rem;background:var(--bg-tint);border:1px solid var(--rule);border-radius:4px;font-size:0.85rem;color:var(--ink-mid);">
    <strong style="color:var(--ink);">Repository.</strong>
    Ground truth documents, IoI rules, instantiators, and templates are publicly available at
    <a href="https://github.com/ioi-framework/ioi-framework" target="_blank" rel="noopener">github.com/ioi-framework/ioi-framework</a>.
    See the <a href="/quickstart/">quick start</a> for setup and execution instructions.
  </div>
</div>
