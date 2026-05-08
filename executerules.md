---
layout: default
title: "Executing Rules"
description: "How to execute IoI signatures against your own CASE/UCO knowledge graphs."
permalink: /executerules/
---
<div class="page-wrap">
  <h1 class="page-title">Executing Rules</h1>
  <p class="page-subtitle">Execute IoI rules against your own forensic datasets in five steps.</p>

  <div style="margin-bottom:1.5rem;padding:1rem 1.15rem;background:var(--bg-tint);border:1px solid var(--rule);border-radius:4px;">
    <div style="font-family:var(--mono);font-size:0.65rem;letter-spacing:0.08em;text-transform:uppercase;color:var(--accent-mid);margin-bottom:0.4rem;">Testing with published datasets</div>
    <p style="font-size:0.88rem;color:var(--ink-mid);margin:0;">
      To reproduce one of the published anti-forensic cases directly, start on the <a href="/artifacts/">Artifacts &amp; Datasets</a> page, download a per-case reproducibility bundle from the <strong>Reproducibility bundle</strong> column, then follow the steps below using the included raw artifacts and parser outputs.
    </p>
  </div>

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
        <p>If you downloaded one of the published case bundles from <a href="/artifacts/">Artifacts &amp; Datasets</a>, use the bundled raw artifacts and CSV parser outputs here instead of exporting your own.</p>
        <p>Use artifact-specific parsers to produce structured CSV output. The framework was validated with the following tools:</p>
        <pre><code># NTFS $MFT and $UsnJrnl:$J
MFTECmd.exe -f "$MFT" --csv ./output --csvf mft.csv
MFTECmd.exe -f "$J"   --csv ./output --csvf usn.csv

# Windows Event Logs
EvtxECmd.exe -f Security.evtx --csv ./output

# LNK files
LECmd.exe -f target.lnk --csv ./output

# Manual Chrome History export (if you have a copied SQLite History DB)
python3 SCRIPTS/export_chrome_history.py "/path/to/History" ./output/history.json</code></pre>
      </div>
    </div>

    <div class="step">
      <div class="step-num">3</div>
      <div class="step-content">
        <h3>Instantiate CASE/UCO knowledge graphs</h3>
        <p>Run the instantiator for each artifact. Each script maps parser CSV fields to the CASE/UCO ontology and serializes the result as JSON-LD.</p>
        <pre><code>mkdir -p outputs

python instantiators/mft_instantiator.py "&lt;MFT_CSV&gt;" outputs/mft_filled.jsonld
python instantiators/usn_instantiator.py "&lt;USN_CSV&gt;" outputs/usn_filled.jsonld
python3 instantiators/history_instantiator.py ./output/history.json outputs/history_filled.jsonld</code></pre>
        <p>Convert every JSON-LD graph required by the rule to N-Triples for bulk loading. For browser-history work outside Autopsy, the flow is: copied Chrome <code>History</code> SQLite DB → <code>SCRIPTS/export_chrome_history.py</code> → <code>history_instantiator.py</code> → JSON-LD/N-Triples:</p>
        <pre><code>python3 SCRIPTS/convert_to_ntriples.py outputs/mft_filled.jsonld outputs/mft_case.nt
python3 SCRIPTS/convert_to_ntriples.py outputs/usn_filled.jsonld outputs/usn_case.nt
python3 SCRIPTS/convert_to_ntriples.py outputs/history_filled.jsonld outputs/history_case.nt</code></pre>
        <p>Use the rule page to identify the required named graphs. For example, IOI-002 requires <code>mft</code>, <code>usn</code>, and <code>history</code>; IOI-004 requires <code>mft</code> and <code>usn</code>.</p>
        <p><strong>Note:</strong> For large MFT/USN files, use <code>--chunk-size 5000</code> to split the output into multiple JSON-LD chunks. Each chunk is then converted to N-Triples separately.</p>
        <pre><code>python instantiators/mft_instantiator.py "&lt;MFT_CSV&gt;" outputs/mft_filled.jsonld --chunk-size 5000
# Converts each chunk: outputs/mft_filled_chunk0.jsonld, _chunk1.jsonld, ...
for f in outputs/mft_filled_chunk*.jsonld; do
  python3 SCRIPTS/convert_to_ntriples.py "$f" "${f%.jsonld}.nt"
done</code></pre>
      </div>
    </div>

    <div class="step">
      <div class="step-num">4</div>
      <div class="step-content">
        <h3>Start Virtuoso and verify your setup</h3>
        <p>Start Virtuoso and wait for it to be ready before loading data:</p>
        <pre><code>docker run --name vos -d -e DBA_PASSWORD=dba \
  -p 8890:8890 -p 1111:1111 \
  openlink/virtuoso-opensource-7:latest

# Wait ~10 seconds, then confirm it is ready
docker exec vos isql 1111 dba dba "exec=select 1;"

# Create import/query directories used by the commands below.
# Some Virtuoso images do not include /usr/share/proj by default.
docker exec vos mkdir -p /usr/share/proj /database</code></pre>
        <p>You should see <code>1</code> returned. If the command fails, wait a few more seconds and retry.</p>
        <p><strong>Verify your environment using the AF-004 test graphs</strong> (no real data needed). These synthetic graphs are included in the repository and produce a known result:</p>
        <pre><code># Copy test graphs into the container
docker cp CASES/AF-004/test/mft_test.nt vos:/usr/share/proj/mft_test.nt
docker cp CASES/AF-004/test/usn_test.nt vos:/usr/share/proj/usn_test.nt

# Load named graphs
docker exec -i vos isql 1111 dba dba <<'EOF'
DB.DBA.TTLP_MT(file_to_string_output('/usr/share/proj/mft_test.nt'), '', 'https://ioi-framework.github.io/cases/AF-004/graphs/mft', 512);
DB.DBA.TTLP_MT(file_to_string_output('/usr/share/proj/usn_test.nt'), '', 'https://ioi-framework.github.io/cases/AF-004/graphs/usn', 512);
SPARQL SELECT ?g (COUNT(*) AS ?count)
WHERE {
  GRAPH ?g { ?s ?p ?o }
  FILTER(?g IN (
    <https://ioi-framework.github.io/cases/AF-004/graphs/mft>,
    <https://ioi-framework.github.io/cases/AF-004/graphs/usn>
  ))
}
GROUP BY ?g;
EXIT;
EOF

# Run IOI-004 — expect 1 row
docker cp RULES/structural/IOI-004_vss_traces_missing.rq vos:/database/rule.rq
docker exec vos bash -lc "printf 'SPARQL\n'; sed '/^#/d' /database/rule.rq; printf '\n;'" \
  | docker exec -i vos isql 1111 dba dba</code></pre>
        <p>A result with <strong>1 row</strong> confirms Virtuoso is correctly loaded and rules execute as expected. The row corresponds to bare <code>{GUID}</code> VSS deletion evidence; <code>Apps_{GUID}</code> names are ignored to avoid Windows Search false positives. IOI-004 also requires the full VSS infrastructure triad (<code>tracking.log</code>, <code>IndexerVolumeGuid</code>, <code>_OnDiskSnapshotProp</code>) to be present before correlating to GUID deletions. This flow uses <code>/usr/share/proj</code> because Virtuoso's default <code>DirsAllowed</code> configuration reads from that directory, and <code>TTLP_MT</code> loads the triples directly once the files are there. See <code>CASES/AF-004/ground_truth.md</code> for what this result means forensically.</p>
      </div>
    </div>

    <div class="step">
      <div class="step-num">5</div>
      <div class="step-content">
        <h3>Load your own graphs and execute IoI rules</h3>
        <p>Copy every N-Triples file required by your selected rule into the container, load each file into the matching named graph IRI, verify nonzero graph counts, then run the rule. The example below shows AF-002 because it uses three graphs; adapt the file names, graph IRIs, and rule path for other cases.</p>
        <pre><code># Ensure Virtuoso's import directory exists.
docker exec vos mkdir -p /usr/share/proj /database

# Copy N-Triples into the container
docker cp outputs/mft_case.nt vos:/usr/share/proj/mft_case.nt
docker cp outputs/usn_case.nt vos:/usr/share/proj/usn_case.nt
docker cp outputs/history_case.nt vos:/usr/share/proj/history_case.nt

# Load named graphs
docker exec -i vos isql 1111 dba dba <<'EOF'
SPARQL CLEAR GRAPH <https://ioi-framework.github.io/cases/AF-002/graphs/mft>;
SPARQL CLEAR GRAPH <https://ioi-framework.github.io/cases/AF-002/graphs/usn>;
SPARQL CLEAR GRAPH <https://ioi-framework.github.io/cases/AF-002/graphs/history>;

DB.DBA.TTLP_MT(file_to_string_output('/usr/share/proj/mft_case.nt'), '', 'https://ioi-framework.github.io/cases/AF-002/graphs/mft', 512);
DB.DBA.TTLP_MT(file_to_string_output('/usr/share/proj/usn_case.nt'), '', 'https://ioi-framework.github.io/cases/AF-002/graphs/usn', 512);
DB.DBA.TTLP_MT(file_to_string_output('/usr/share/proj/history_case.nt'), '', 'https://ioi-framework.github.io/cases/AF-002/graphs/history', 512);

SPARQL SELECT ?g (COUNT(*) AS ?count)
WHERE {
  GRAPH ?g { ?s ?p ?o }
  FILTER(?g IN (
    <https://ioi-framework.github.io/cases/AF-002/graphs/mft>,
    <https://ioi-framework.github.io/cases/AF-002/graphs/usn>,
    <https://ioi-framework.github.io/cases/AF-002/graphs/history>
  ))
}
GROUP BY ?g;
EXIT;
EOF

# Execute an IoI rule
docker cp RULES/semantic/IOI-002_chrome_history_missing.rq vos:/database/rule.rq
docker exec vos bash -lc "printf 'SPARQL\n'; sed '/^#/d' /database/rule.rq; printf '\n;'" \
  | docker exec -i vos isql 1111 dba dba</code></pre>
        <p>A non-empty result set indicates a detected inconsistency. If the graph-count query returns zero for any required graph, fix loading before debugging the rule. Read the corresponding <code>CASES/AF-NNN/ground_truth.md</code> to interpret the result.</p>
      </div>
    </div>

  </div>

  <div style="margin-top:2.5rem;padding:1.25rem;background:var(--bg-tint);border:1px solid var(--rule);border-radius:4px;">
    <div style="font-family:var(--mono);font-size:0.65rem;letter-spacing:0.08em;text-transform:uppercase;color:var(--accent-mid);margin-bottom:0.4rem;">Need help?</div>
    <p style="font-size:0.88rem;color:var(--ink-mid);margin:0;">
      See the <a href="/artifacts/">artifacts &amp; datasets</a> page for published reproducibility bundles and downloadable case datasets,
      the <a href="/cases/">scenarios</a> for ground-truth specifications,
      and the <a href="/rules/">IoI rules library</a> for all SPARQL signatures.
      Open an issue on <a href="https://github.com/ioi-framework" target="_blank" rel="noopener">GitHub ↗</a> if you encounter problems.
    </p>
  </div>
</div>
