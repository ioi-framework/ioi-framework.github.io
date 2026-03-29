---
layout: default
title: "Paper"
description: "Indicator of Inconsistency (IoI): A SPARQL-Based Framework for Cross-Artifact Contradiction Detection in Digital Forensics."
---
<div class="page-wrap">

  <div style="margin-bottom:2rem;padding-bottom:1.5rem;border-bottom:1px solid var(--rule);">
    <div style="font-family:var(--mono);font-size:0.7rem;letter-spacing:0.1em;text-transform:uppercase;color:var(--accent-mid);margin-bottom:0.6rem;">
      Forensic Science International: Digital Investigation · Under review
    </div>
    <h1 class="page-title" style="font-size:1.5rem;line-height:1.3;max-width:680px;">
      Indicator of Inconsistency (IoI): A SPARQL-Based Framework for
      Cross-Artifact Contradiction Detection in Digital Forensics
    </h1>
  </div>

  <!-- Abstract -->
  <div style="margin-bottom:2.5rem;">
    <h2 style="font-family:var(--serif);font-weight:600;font-size:1rem;margin-bottom:0.75rem;color:var(--ink);">Abstract</h2>
    <p style="font-size:0.92rem;color:var(--ink-mid);line-height:1.85;max-width:720px;">
      Identifying complex events and their reconstruction have been an exhaustive task through digital forensic investigations and analyses. In this paper, we propose an Indicator of Inconsistency (IoI) framework that assists investigators in defining inconsistent digital artifacts, which in turn helps highlight events of probative value, such as anti-forensics attempts. IoIs are defined as schema-consistent SPARQL queries that detect contradictions among temporally, structurally, and semantically related artifacts. The framework leverages CASE/UCO ontology graphs and the SPARQL language, along with the corresponding reasoning framework. A proof-of-concept implementation was developed to generate reusable, machine-readable, and interoperable ontology-based knowledge graphs of digital artifacts along with corresponding signatures in SPARQL to detect contradicting artifacts and/or attributes across five curated anti-forensic scenarios. We found that, when supported by the community, such a framework can facilitate detection of complex events that would otherwise be difficult to detect due to investigators' expertise limitations or the volume of artifacts.
    </p>
  </div>

  <!-- Contributions -->
  <div style="margin-bottom:2.5rem;">
    <h2 style="font-family:var(--serif);font-weight:600;font-size:1rem;margin-bottom:0.75rem;color:var(--ink);">Contributions</h2>
    <div class="steps" style="gap:0;">
      <div class="step">
        <div class="step-num">1</div>
        <div class="step-content">
          <h3>Formal categorization of cross-artifact inconsistencies</h3>
          <p>Temporal, structural, and semantic invariant classes defined over CASE/UCO-compliant knowledge graphs.</p>
        </div>
      </div>
      <div class="step">
        <div class="step-num">2</div>
        <div class="step-content">
          <h3>Case-agnostic IoI signatures</h3>
          <p>Reusable SPARQL constraints expressing violation predicates over ontology classes and properties rather than case-specific identifiers.</p>
        </div>
      </div>
      <div class="step">
        <div class="step-num">3</div>
        <div class="step-content">
          <h3>Ontology-driven implementation</h3>
          <p>End-to-end pipeline from artifact parsing through CASE/UCO knowledge graph construction to SPARQL evaluation in OpenLink Virtuoso.</p>
        </div>
      </div>
      <div class="step">
        <div class="step-num">4</div>
        <div class="step-content">
          <h3>Empirical evaluation</h3>
          <p>Five curated anti-forensic scenarios executed in controlled Windows 10 VMs, validated with zero false positives across all primary rules.</p>
        </div>
      </div>
      <div class="step">
        <div class="step-num">5</div>
        <div class="step-content">
          <h3>Distributed crowd-sourced architecture</h3>
          <p>A community-driven model decoupling IoI signature development from operational execution, enabling cross-investigator reuse.</p>
        </div>
      </div>
    </div>
  </div>

  <!-- Research questions -->
  <div style="margin-bottom:2.5rem;">
    <h2 style="font-family:var(--serif);font-weight:600;font-size:1rem;margin-bottom:0.75rem;color:var(--ink);">Research questions</h2>
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:0.75rem;">
      <div style="border:1px solid var(--rule);border-radius:4px;padding:1rem 1.1rem;">
        <div style="font-family:var(--mono);font-size:0.65rem;color:var(--accent-mid);margin-bottom:0.3rem;">RQ1</div>
        <p style="font-size:0.85rem;color:var(--ink-mid);margin:0;">How can inconsistencies between dependent digital artifacts be formally defined and categorized?</p>
      </div>
      <div style="border:1px solid var(--rule);border-radius:4px;padding:1rem 1.1rem;">
        <div style="font-family:var(--mono);font-size:0.65rem;color:var(--accent-mid);margin-bottom:0.3rem;">RQ2</div>
        <p style="font-size:0.85rem;color:var(--ink-mid);margin:0;">How can such inconsistencies be operationalized using CASE/UCO graphs and SPARQL constraints?</p>
      </div>
      <div style="border:1px solid var(--rule);border-radius:4px;padding:1rem 1.1rem;">
        <div style="font-family:var(--mono);font-size:0.65rem;color:var(--accent-mid);margin-bottom:0.3rem;">RQ3</div>
        <p style="font-size:0.85rem;color:var(--ink-mid);margin:0;">How can IoI signatures be represented as interoperable and reusable artifacts for sharing across investigators and tools?</p>
      </div>
      <div style="border:1px solid var(--rule);border-radius:4px;padding:1rem 1.1rem;">
        <div style="font-family:var(--mono);font-size:0.65rem;color:var(--accent-mid);margin-bottom:0.3rem;">RQ4</div>
        <p style="font-size:0.85rem;color:var(--ink-mid);margin:0;">What architectural components are required to support a distributed IoI development and execution framework?</p>
      </div>
    </div>
  </div>

  <!-- Citation -->
  <div style="margin-bottom:2rem;">
    <h2 style="font-family:var(--serif);font-weight:600;font-size:1rem;margin-bottom:0.75rem;color:var(--ink);">Cite this work</h2>
    <div class="citation-box" id="citation-text">
@article{ioi-framework-2025,<br>
&nbsp;&nbsp;title   = {Indicator of Inconsistency (IoI): A SPARQL-Based Framework for<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Cross-Artifact Contradiction Detection in Digital Forensics},<br>
&nbsp;&nbsp;journal = {Forensic Science International: Digital Investigation},<br>
&nbsp;&nbsp;year    = {2025},<br>
&nbsp;&nbsp;note    = {Under review},<br>
&nbsp;&nbsp;url     = {https://ioi-framework.github.io}<br>
}
    </div>
    <button class="citation-copy" onclick="copyCitation()" style="position:relative;top:auto;right:auto;margin-top:0.5rem;display:inline-block;">Copy BibTeX</button>
  </div>

  <div style="padding:1rem 1.25rem;background:var(--bg-tint);border:1px solid var(--rule);border-radius:4px;font-size:0.85rem;color:var(--ink-mid);">
    A preprint link will be added here once the paper is available publicly.
    In the meantime, see the <a href="/artifacts/">artifacts page</a> for datasets and code,
    or the <a href="/rules/">IoI rules library</a> for all SPARQL signatures.
  </div>
</div>
