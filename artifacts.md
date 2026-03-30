---
layout: default
title: "Artifacts & Datasets"
description: "Download knowledge graphs, ground-truth documents, JSON-LD templates, Template Instantiators, and SPARQL IoI rules."
---
<div class="page-wrap">
  <h1 class="page-title">Artifacts &amp; datasets</h1>
  <p class="page-subtitle">
    All datasets, templates, and code will be released publicly following paper acceptance,
    in accordance with double-blind review requirements. The structure below reflects what
    will be available in the repository.
  </p>

  <!-- Repository structure -->
  <div class="section-header" style="margin-bottom:1.25rem;">
    <h2>Repository structure</h2>
  </div>

  <pre style="font-size:0.78rem;line-height:1.9;margin-bottom:2rem;"><code>ioi-framework/
├── cases/                        # Per-scenario datasets
│   ├── AF-002/
│   │   ├── baseline/             # Baseline artifact exports (CSV/JSON)
│   │   ├── post-manipulation/    # Post-manipulation artifact exports
│   │   ├── graphs/               # Instantiated JSON-LD knowledge graphs
│   │   │   ├── mft_case.jsonld
│   │   │   ├── usn_case.jsonld
│   │   │   └── history_case.jsonld
│   │   └── ground-truth.md       # Invariant + violation specification
│   ├── AF-004/  ...
│   ├── AF-007/  ...
│   ├── AF-011/  ...
│   └── AF-012/
│       ├── graphs/
│       │   ├── office_case.jsonld
│       │   └── mft_case.jsonld
│       └── ground-truth.md
│
├── templates/                    # Case-agnostic CASE/UCO templates
│   ├── mft_template.jsonld
│   ├── usn_template.jsonld
│   ├── lnk_template.jsonld
│   ├── evtx_template.jsonld
│   ├── history_template.jsonld
│   └── office_xml_template.jsonld
│
├── instantiators/                # Template Instantiator scripts
│   ├── mft_instantiator.py
│   ├── usn_instantiator.py
│   ├── lnk_instantiator.py
│   ├── evtx_instantiator.py
│   └── office_instantiator.py
│
├── rules/
│   └── sparql/                   # IoI SPARQL signatures (.rq files)
│       ├── ioi-002.rq
│       ├── ioi-004.rq
│       ├── ioi-007.rq
│       ├── ioi-011.rq
│       ├── ioi-011-permissive.rq
│       └── ioi-012.rq
│
├── scripts/
│   ├── jsonld_to_ntriples.py     # JSON-LD → N-Triples conversion
│   └── docker-compose.yml        # Virtuoso stack
│
└── ontology/
    └── ioi-ext.ttl               # ioi-ext namespace definitions</code></pre>

  <!-- Artifact types -->
  <div class="section-header" style="margin-bottom:1.25rem;">
    <h2>What each folder contains</h2>
  </div>

  <div class="card-grid" style="grid-template-columns:repeat(auto-fill,minmax(260px,1fr));margin-bottom:2rem;">

    <div class="card">
      <div class="card-tag">cases/</div>
      <h3>Scenario datasets</h3>
      <p>Paired baseline and post-manipulation artifact exports (CSV/JSON) for all five scenarios, plus instantiated JSON-LD knowledge graphs ready for loading into Virtuoso.</p>
    </div>

    <div class="card">
      <div class="card-tag">templates/</div>
      <h3>CASE/UCO templates</h3>
      <p>Case-agnostic JSON-LD templates defining the facet structures referenced by IoI rules. Use these as the starting point for building Template Instantiators for new artifact types.</p>
    </div>

    <div class="card">
      <div class="card-tag">instantiators/</div>
      <h3>Template Instantiators</h3>
      <p>Python scripts that map artifact-specific parser CSV output to CASE/UCO template structures, producing case-specific JSON-LD graphs for each scenario.</p>
    </div>

    <div class="card">
      <div class="card-tag">rules/sparql/</div>
      <h3>IoI SPARQL rules</h3>
      <p>All five IoI signatures as <code>.rq</code> files. Substitute named graph IRIs and execute directly via <code>isql</code> or any SPARQL 1.1 endpoint.</p>
    </div>

    <div class="card">
      <div class="card-tag">cases/*/ground-truth.md</div>
      <h3>Ground-truth documents</h3>
      <p>Per-scenario specifications describing affected artifacts, expected invariants, and violation predicates as pseudo-query logic — the human-readable counterpart to each IoI rule.</p>
    </div>

    <div class="card">
      <div class="card-tag">ontology/</div>
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
          <td><a href="https://github.com/ioi-framework/ioi-framework/blob/main/cases/AF-002/ground-truth.md" target="_blank" rel="noopener">ground-truth.md ↗</a></td>
        </tr>
        <tr>
          <td><a href="/cases/af-004/">AF-004</a></td>
          <td>$MFT, $UsnJrnl</td>
          <td>21,004,830</td>
          <td>2</td>
          <td><a href="https://github.com/ioi-framework/ioi-framework/blob/main/cases/AF-004/ground-truth.md" target="_blank" rel="noopener">ground-truth.md ↗</a></td>
        </tr>
        <tr>
          <td><a href="/cases/af-007/">AF-007</a></td>
          <td>Security.evtx, $UsnJrnl</td>
          <td>5,922,784</td>
          <td>2</td>
          <td><a href="https://github.com/ioi-framework/ioi-framework/blob/main/cases/AF-007/ground-truth.md" target="_blank" rel="noopener">ground-truth.md ↗</a></td>
        </tr>
        <tr>
          <td><a href="/cases/af-011/">AF-011</a></td>
          <td>LNK, $MFT</td>
          <td>18,385,659</td>
          <td>2</td>
          <td><a href="https://github.com/ioi-framework/ioi-framework/blob/main/cases/AF-011/ground-truth.md" target="_blank" rel="noopener">ground-truth.md ↗</a></td>
        </tr>
        <tr>
          <td><a href="/cases/af-012/">AF-012</a></td>
          <td>Office core.xml, $MFT</td>
          <td>18,383,783</td>
          <td>2</td>
          <td><a href="https://github.com/ioi-framework/ioi-framework/blob/main/cases/AF-012/ground-truth.md" target="_blank" rel="noopener">ground-truth.md ↗</a></td>
        </tr>
      </tbody>
    </table>
  </div>

  <div style="margin-top:2rem;padding:1.1rem 1.25rem;background:var(--bg-tint);border:1px solid var(--rule);border-radius:4px;font-size:0.85rem;color:var(--ink-mid);">
    <strong style="color:var(--ink);">Dataset availability.</strong>
    All datasets, templates, instantiators, and IoI rules will be released in the public GitHub repository
    at <a href="https://github.com/ioi-framework/ioi-framework" target="_blank" rel="noopener">github.com/ioi-framework/ioi-framework</a>
    following paper acceptance. During double-blind review, this page reflects the planned release structure.
  </div>
</div>
