---
layout: default
title: "Quick Start"
description: "How to set up and run IoI signatures against your own CASE/UCO knowledge graphs."
---
<div class="page-wrap">
  <h1 class="page-title">Quick start</h1>
  <p class="page-subtitle">Get the IoI framework running against your own forensic datasets in four steps.</p>

  <div class="section-header" style="margin-bottom:1.25rem;">
    <h2>Prerequisites</h2>
  </div>
  <div class="prose" style="margin-bottom:2rem;">
    <p>The framework requires Python 3.9+, <code>rdflib</code> for JSON-LD to N-Triples conversion, and a SPARQL 1.1 triplestore. The proof-of-concept validation used OpenLink Virtuoso Open-Source Edition running in Docker.</p>
    <pre><code>pip install rdflib</code></pre>
    <p>Pull the Virtuoso Docker image:</p>
    <pre><code>docker pull openlink/virtuoso-opensource-7</code></pre>
  </div>

  <div class="section-header" style="margin-bottom:1.25rem;">
    <h2>Step-by-step</h2>
  </div>
  <div class="steps">

    <div class="step">
      <div class="step-num">1</div>
      <div class="step-content">
        <h3>Clone the repository</h3>
        <p>The repository contains all templates, Template Instantiators, ground-truth documents, and IoI SPARQL rules.</p>
        <pre><code>git clone https://github.com/ioi-framework/ioi-framework.git
cd ioi-framework</code></pre>
      </div>
    </div>

    <div class="step">
      <div class="step-num">2</div>
      <div class="step-content">
        <h3>Parse your artifacts</h3>
        <p>Use the artifact-specific parsers to produce structured CSV or JSON output. The framework was validated with the following tools:</p>
        <pre><code># NTFS $MFT and $UsnJrnl:$J
MFTECmd.exe -f "$MFT" --csv ./output --csvf mft.csv
MFTECmd.exe -f "$J"   --csv ./output --csvf usn.csv

# Windows Event Logs
EvtxECmd.exe -f Security.evtx --csv ./output

# LNK files
LECmd.exe -f target.lnk --csv ./output</code></pre>
      </div>
    </div>

    <div class="step">
      <div class="step-num">3</div>
      <div class="step-content">
        <h3>Instantiate CASE/UCO knowledge graphs</h3>
        <p>Run the Template Instantiator for your scenario. Each instantiator maps parser CSV fields to the corresponding CASE/UCO ontology template and serializes the result as JSON-LD.</p>
        <pre><code>python instantiators/mft_instantiator.py \
  --input output/mft.csv \
  --template templates/mft_template.jsonld \
  --output graphs/mft_case.jsonld

python instantiators/usn_instantiator.py \
  --input output/usn.csv \
  --output graphs/usn_case.jsonld</code></pre>
        <p>Convert JSON-LD to N-Triples for bulk loading:</p>
        <pre><code>python scripts/jsonld_to_ntriples.py \
  --input graphs/ --output ntriples/</code></pre>
      </div>
    </div>

    <div class="step">
      <div class="step-num">4</div>
      <div class="step-content">
        <h3>Load graphs and execute IoI rules</h3>
        <p>Start Virtuoso, load the named graphs, then run the SPARQL signatures:</p>
        <pre><code>docker-compose up -d virtuoso

# Load named graphs via isql
isql 1111 dba dba \
  "ld_dir('/data/ntriples', 'mft_case.nt', 'http://ioi/mft_case');
   ld_dir('/data/ntriples', 'usn_case.nt', 'http://ioi/usn_case');
   rdf_loader_run(); checkpoint;"

# Execute an IoI rule
isql 1111 dba dba < rules/sparql/ioi-002.rq</code></pre>
        <p>A non-empty result set indicates a detected inconsistency. Zero results on baseline graphs confirm no false positives.</p>
      </div>
    </div>

  </div>

  <div style="margin-top:2.5rem;padding:1.25rem;background:var(--bg-tint);border:1px solid var(--rule);border-radius:4px;">
    <div style="font-family:var(--mono);font-size:0.65rem;letter-spacing:0.08em;text-transform:uppercase;color:var(--accent-mid);margin-bottom:0.4rem;">Need help?</div>
    <p style="font-size:0.88rem;color:var(--ink-mid);margin:0;">
      See the <a href="/artifacts/">artifacts &amp; datasets</a> page for pre-built knowledge graphs,
      the <a href="/cases/">scenarios</a> for ground-truth specifications,
      and the <a href="/rules/">IoI rules library</a> for all SPARQL signatures.
      Open an issue on <a href="https://github.com/ioi-framework" target="_blank" rel="noopener">GitHub ↗</a> if you encounter problems.
    </p>
  </div>
</div>
