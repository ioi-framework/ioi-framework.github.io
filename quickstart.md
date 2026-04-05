---
layout: default
title: "Quick Start"
description: "How to set up and run IoI signatures against your own CASE/UCO knowledge graphs."
---
<div class="page-wrap">
  <h1 class="page-title">Quick start</h1>
  <p class="page-subtitle">Get the IoI framework running against your own forensic datasets in four steps.</p>

  <div class="prose" style="margin-bottom:2rem;">
    <p>The framework operates in three layers:</p>
    <ul>
      <li><strong>Instantiators</strong> — Python scripts that map artifact parser CSV output to CASE/UCO JSON-LD knowledge graphs.</li>
      <li><strong>Knowledge Graph</strong> — named graphs loaded into a SPARQL 1.1 triplestore (Virtuoso), one per artifact source.</li>
      <li><strong>IoI Rules</strong> — SPARQL signatures that query across graphs to surface cross-artifact contradictions.</li>
    </ul>
  </div>

  <div class="section-header" style="margin-bottom:1.25rem;">
    <h2>Prerequisites</h2>
  </div>
  <div class="prose" style="margin-bottom:2rem;">
    <p>Python 3.9+, <code>rdflib</code> and <code>pandas</code> for instantiators and JSON-LD conversion, and a SPARQL 1.1 triplestore. Validation used OpenLink Virtuoso Open-Source Edition running in Docker.</p>
    <pre><code>pip install rdflib pandas</code></pre>
    <p>Pull the Virtuoso Docker image:</p>
    <pre><code>docker pull openlink/virtuoso-opensource-7:latest</code></pre>
  </div>

  <div class="section-header" style="margin-bottom:1.25rem;">
    <h2>Step-by-step</h2>
  </div>
  <div class="steps">

    <div class="step">
      <div class="step-num">1</div>
      <div class="step-content">
        <h3>Clone the repository</h3>
        <p>The repository contains all instantiator scripts, JSON-LD templates, ground-truth documents, and IoI SPARQL rules.</p>
        <pre><code>git clone https://github.com/ioi-framework/ioi-framework.git
cd ioi-framework</code></pre>
      </div>
    </div>

    <div class="step">
      <div class="step-num">2</div>
      <div class="step-content">
        <h3>Parse your artifacts</h3>
        <p>Use artifact-specific parsers to produce structured CSV output. The framework was validated with the following tools:</p>
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
        <p>Run the instantiator for each artifact. Each script maps parser CSV fields to the CASE/UCO ontology and serializes the result as JSON-LD.</p>
        <pre><code>mkdir -p outputs

python instantiators/mft_instantiator.py "&lt;MFT_CSV&gt;" outputs/mft_filled.jsonld
python instantiators/usn_instantiator.py "&lt;USN_CSV&gt;" outputs/usn_filled.jsonld</code></pre>
        <p>Convert JSON-LD to N-Triples for bulk loading:</p>
        <pre><code>python scripts/convert_to_ntriples.py outputs/mft_filled.jsonld outputs/mft_case.nt
python scripts/convert_to_ntriples.py outputs/usn_filled.jsonld outputs/usn_case.nt</code></pre>
        <p><strong>Note:</strong> For large MFT/USN files, use <code>--chunk-size 5000</code> to split the output into multiple JSON-LD chunks. Each chunk is then converted to N-Triples separately.</p>
        <pre><code>python instantiators/mft_instantiator.py "&lt;MFT_CSV&gt;" outputs/mft_filled.jsonld --chunk-size 5000
# Converts each chunk: outputs/mft_filled_chunk0.jsonld, _chunk1.jsonld, ...
for f in outputs/mft_filled_chunk*.jsonld; do
  python scripts/convert_to_ntriples.py "$f" "${f%.jsonld}.nt"
done</code></pre>
      </div>
    </div>

    <div class="step">
      <div class="step-num">4</div>
      <div class="step-content">
        <h3>Load graphs and execute IoI rules</h3>
        <p>Start Virtuoso, load the named graphs, then run a SPARQL signature:</p>
        <pre><code># Start Virtuoso
docker run --name vos -d -e DBA_PASSWORD=dba \
  -p 8890:8890 -p 1111:1111 \
  openlink/virtuoso-opensource-7:latest

# Copy N-Triples into the container
docker cp outputs/mft_case.nt vos:/database/mft_case.nt
docker cp outputs/usn_case.nt vos:/database/usn_case.nt

# Load named graphs
docker exec vos isql 1111 dba dba "exec=ld_dir('.', 'mft_case.nt', 'http://example.org/mft_case');"
docker exec vos isql 1111 dba dba "exec=ld_dir('.', 'usn_case.nt', 'http://example.org/usn_case');"
docker exec vos isql 1111 dba dba "exec=rdf_loader_run();"
docker exec vos isql 1111 dba dba "exec=checkpoint;"

# Execute an IoI rule
docker cp rules/temporal/IOI-007_usn_clear_before_event.rq vos:/database/rule.rq
docker exec vos bash -lc "printf 'SPARQL\n'; cat /database/rule.rq; printf '\n;'" \
  | docker exec -i vos isql 1111 dba dba</code></pre>
        <p>A non-empty result set indicates a detected inconsistency.</p>
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
