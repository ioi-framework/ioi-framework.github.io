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
├── CASES/
│   ├── AF-002/
│   │   ├── snippets/             # JSON-LD test graphs + sample data
│   │   ├── ground_truth.md
│   │   ├── mapping.md
│   │   └── README.md
│   └── AF-012/  ...
│
├── instantiators/
│   ├── mft_instantiator.py
│   ├── usn_instantiator.py
│   ├── lnk_instantiator.py
│   ├── evtx_instantiator.py
│   ├── history_instantiator.py
│   ├── office_xml_instantiator.py
│   └── templates/
│       ├── mft/  usn/  lnk/  evtx/  browser_history/  office_xml/
│
├── RULES/
│   ├── semantic/  structural/  temporal/
│
├── registry.json                 # Single source of truth for artifact metadata
├── SCRIPTS/
│   ├── convert_to_ntriples.py
│   └── export_chrome_history.py  # Manual Chrome History SQLite → framework JSON
├── scripts/
│   ├── validate_registry.py
│   ├── validate_sparql.py
│   └── validate_jsonld.py
├── playground/
└── ontologies/
    └── ioi-ext.ttl</code></pre>

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
      <div class="card-tag">instantiators/templates/</div>
      <h3>CASE/UCO templates</h3>
      <p>Case-agnostic JSON-LD templates defining the facet structures referenced by IoI rules. They now live under `instantiators/templates/` and serve as the starting point for new instantiators and artifact types.</p>
    </div>

    <div class="card">
      <div class="card-tag">instantiators/</div>
      <h3>Template Instantiators</h3>
      <p>Python scripts that map artifact-specific parser output to CASE/UCO template structures, producing case-specific JSON-LD graphs for each scenario. This now includes the browser-history flow plus a manual Chrome History SQLite exporter under <code>SCRIPTS/</code>.</p>
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
    {% assign sorted_cases = site.cases | sort: "case_id" %}
    <table>
      <thead>
        <tr>
          <th>Case</th>
          <th>Artifacts</th>
          <th>Total triples</th>
          <th>JSON-LD graphs</th>
          <th>Ground truth</th>
          <th>Reproducibility bundle</th>
        </tr>
      </thead>
      <tbody>
        {% for case in sorted_cases %}
        {% assign ground_truth_url = "https://github.com/ioi-framework/ioi-framework/blob/main/CASES/" | append: case.case_id | append: "/ground_truth.md" %}
        <tr>
          <td><a href="{{ case.url | relative_url }}">{{ case.case_id }}</a></td>
          <td>{{ case.artifact_summary }}</td>
          <td>{{ case.total_triples }}</td>
          <td>{{ case.jsonld_graphs }}</td>
          <td><a href="{{ ground_truth_url }}" target="_blank" rel="noopener">ground_truth.md ↗</a></td>
          <td>
            {% assign repro_url = case.repro_bundle_url | default: "" | strip %}
            {% if repro_url != "" %}
            {% assign repro_label = case.repro_bundle_label | default: "" | strip %}
            {% if repro_label == "" %}
              {% assign repro_label = "Zenodo DOI ↗" %}
            {% endif %}
            <a href="{{ repro_url }}" target="_blank" rel="noopener">{{ repro_label }}</a>
            {% endif %}
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>

  <div style="margin-top:2rem;padding:1.1rem 1.25rem;background:var(--bg-tint);border:1px solid var(--rule);border-radius:4px;font-size:0.85rem;color:var(--ink-mid);">
    <strong style="color:var(--ink);">Repository.</strong>
    Ground truth documents, IoI rules, instantiators, and templates are publicly available at
    <a href="https://github.com/ioi-framework/ioi-framework" target="_blank" rel="noopener">github.com/ioi-framework/ioi-framework</a>.
    See the <a href="/executerules/">Executing Rules</a> page for setup and execution instructions, including the manual Chrome History SQLite export path. Published per-case reproducibility bundles will appear in the table above as they become available.
  </div>
</div>
