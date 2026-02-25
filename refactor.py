import re

with open("index.html", "r") as f:
    content = f.read()

script_start = content.find("<script>\npdfjsLib")
if script_start == -1:
    script_start = content.find("<script>")
js_content = content[script_start:]

new_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#09090b">
<title>Newton Invoice Analyser — Balfour Park</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
<style>
/* === FOUNDATION & INTENTIONAL MINIMALISM === */
:root {
  --bg: #ffffff;
  --surface: #fafafa;
  --surface-hover: #f4f4f5;
  --text: #09090b;
  --text-muted: #71717a;
  --border: #09090b;
  --border-light: #e4e4e7;
  
  --high-bg: #fef2f2;
  --high-text: #7f1d1d;
  --high-border: #dc2626;
  --high-accent: #ef4444;
  
  --med-bg: #fffbf0;
  --med-text: #78350f;
  --med-border: #d97706;
  --med-accent: #f59e0b;
  
  --info-bg: #ffffff;
  --info-text: #09090b;
  --info-border: #09090b;
  --info-accent: #09090b;

  --success-bg: #f0fdf4;
  --success-text: #14532d;
  --success-border: #16a34a;
  
  --font-sans: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: #09090b;
    --surface: #18181b;
    --surface-hover: #27272a;
    --text: #fafafa;
    --text-muted: #a1a1aa;
    --border: #fafafa;
    --border-light: #27272a;
    
    --high-bg: #450a0a;
    --high-text: #fecaca;
    --high-border: #ef4444;
    --high-accent: #f87171;

    --med-bg: #451a03;
    --med-text: #fde68a;
    --med-border: #f59e0b;
    --med-accent: #fbbf24;

    --info-bg: #09090b;
    --info-text: #fafafa;
    --info-border: #fafafa;
    --info-accent: #fafafa;

    --success-bg: #052e16;
    --success-text: #bbf7d0;
    --success-border: #22c55e;
  }
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body { 
  font-family: var(--font-sans);
  background: var(--bg); 
  color: var(--text); 
  line-height: 1.6; 
  -webkit-font-smoothing: antialiased;
}

h1, h2, h3, h4, th { 
  font-weight: 700; 
  letter-spacing: -0.025em; 
  text-transform: uppercase;
}

/* === LAYOUT === */
#app-wrapper {
  display: flex;
  min-height: 100vh;
  flex-direction: column;
}

header {
  border-bottom: 2px solid var(--border);
  background: var(--bg);
  position: sticky;
  top: 0;
  z-index: 50;
}

.container { 
  max-width: 1024px; 
  margin: 0 auto; 
  padding: 0 24px; 
}

.header-inner {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  padding: 40px 0 0 0;
  gap: 32px;
}

@media (max-width: 768px) {
  .header-inner { flex-direction: column; align-items: flex-start; padding-top: 32px; gap: 16px; }
}

.brand h1 { font-size: 1.75rem; font-weight: 900; letter-spacing: -0.05em; line-height: 1.1; }
.brand p { color: var(--text-muted); font-size: 0.875rem; font-family: var(--font-mono); margin-top: 8px; text-transform: uppercase; }

/* === NAVIGATION === */
.tab-bar { 
  display: flex; 
  gap: 24px;
  overflow-x: auto;
  min-width: 100%;
}
.tab-btn { 
  background: transparent; 
  color: var(--text-muted); 
  border: none; 
  padding: 12px 0 12px 0;
  cursor: pointer; 
  font-size: 0.875rem; 
  font-weight: 600; 
  text-transform: uppercase;
  transition: all 0.2s; 
  border-bottom: 3px solid transparent;
  white-space: nowrap;
}
.tab-btn:hover { color: var(--text); }
.tab-btn.active { color: var(--text); border-bottom-color: var(--text); }

/* === CONTENT PANELS === */
main {
  padding: 48px 0;
  flex: 1;
}

.tab-content { display: none; animation: fadeIn 0.3s ease; }
.tab-content.active { display: block; }

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}

.card { 
  border: 1px solid var(--border-light); 
  background: var(--surface); 
  padding: 32px; 
  margin-bottom: 32px;
}
.card > h2 { font-size: 1.25rem; margin-bottom: 12px; border-bottom: 1px solid var(--border-light); padding-bottom: 12px; }
.card > p { color: var(--text-muted); font-size: 0.9rem; margin-bottom: 24px; max-width: 700px; }
.card h3 { font-size: 1rem; margin: 32px 0 16px; }

/* === UPLOAD INTERFACE === */
.graphic-banner {
  width: 100%;
  height: 200px;
  background-image: url('newton_graphic.png');
  background-size: cover;
  background-position: center;
  border: 1px solid var(--border-light);
  margin-bottom: 24px;
  filter: grayscale(100%) contrast(1.2) brightness(0.6);
  position: relative;
}
.graphic-banner::after {
  content: '';
  position: absolute; inset: 0;
  background: linear-gradient(to top, var(--surface) 0%, transparent 100%);
}

.drop-zone { 
  border: 2px dashed var(--border-light); 
  background: var(--bg);
  padding: 64px 24px; 
  text-align: center; 
  cursor: pointer; 
  transition: all 0.2s; 
}
.drop-zone:hover, .drop-zone.drag-over { 
  border-color: var(--text); 
  background: var(--surface-hover); 
}
.drop-zone .big { font-size: 2.5rem; margin-bottom: 16px; opacity: 0.8; }
.drop-zone p { color: var(--text); font-weight: 600; font-size: 1.1rem; }
.drop-zone span { color: var(--text-muted); font-size: 0.875rem; display: block; margin-top: 8px; font-family: var(--font-mono); }

/* === BUTTONS === */
.btn { 
  display: inline-flex; align-items: center; justify-content: center;
  padding: 10px 20px; 
  border: 1px solid transparent;
  cursor: pointer; 
  font-size: 0.875rem; 
  font-weight: 600; 
  text-transform: uppercase;
  transition: all 0.2s; 
  font-family: inherit;
}
.btn-primary { background: var(--text); color: var(--bg); }
.btn-primary:hover { opacity: 0.9; transform: translateY(-1px); }
.btn-outline { background: transparent; border-color: var(--border-light); color: var(--text); }
.btn-outline:hover { background: var(--surface-hover); border-color: var(--text); }
.btn-danger { background: var(--high-accent); color: var(--bg); }
.btn-green { background: var(--success-border); color: var(--bg); }
.btn-sm { padding: 4px 10px; font-size: 0.75rem; }

/* === TABLES === */
table { width: 100%; border-collapse: collapse; font-size: 0.875rem; text-align: left; margin-top: 16px; }
th { color: var(--text-muted); font-weight: 600; padding: 12px 16px; border-bottom: 2px solid var(--border-light); font-size: 0.75rem; font-family: var(--font-mono); }
td { padding: 16px; border-bottom: 1px solid var(--border-light); vertical-align: top; }
tr:last-child td { border-bottom: none; }
tr:hover td { background: var(--surface-hover); }

/* MOBILE TABLES via Nth-Child */
@media (max-width: 768px) {
  table, thead, tbody, th, td, tr { display: block; }
  thead tr { position: absolute; top: -9999px; left: -9999px; }
  tr { border: 1px solid var(--border-light); margin-bottom: 16px; background: var(--bg); }
  td { border: none; border-bottom: 1px solid var(--border-light); position: relative; padding-left: 45%; text-align: right; }
  td:last-child { border-bottom: none; }
  
  td::before {
    position: absolute; left: 16px; width: 40%; text-align: left;
    font-weight: 600; text-transform: uppercase; color: var(--text-muted); font-size: 0.75rem; font-family: var(--font-mono);
  }
  
  /* Uploads Table */
  #fileListBody td:nth-child(1)::before { content: "File"; }
  #fileListBody td:nth-child(2)::before { content: "Status"; }
  #fileListBody td:nth-child(3)::before { content: "Invoice #"; }
  #fileListBody td:nth-child(4)::before { content: "Total"; }
  
  /* Invoices Table */
  #resultsContent table:nth-of-type(1) td:nth-child(1)::before { content: "Invoice #"; }
  #resultsContent table:nth-of-type(1) td:nth-child(2)::before { content: "Type"; }
  #resultsContent table:nth-of-type(1) td:nth-child(3)::before { content: "Period"; }
  #resultsContent table:nth-of-type(1) td:nth-child(4)::before { content: "Charges"; }
  #resultsContent table:nth-of-type(1) td:nth-child(5)::before { content: "Total"; }

  /* Cost Summary */
  #resultsContent table:nth-of-type(2) td:nth-child(1)::before { content: "Category"; }
  #resultsContent table:nth-of-type(2) td:nth-child(2)::before { content: "Total"; }
  #resultsContent table:nth-of-type(2) td:nth-child(3)::before { content: "Per Year"; }
}

/* === BADGES === */
.badge { 
  display: inline-flex; align-items: center; padding: 4px 8px; 
  font-size: 0.75rem; font-weight: 700; font-family: var(--font-mono); text-transform: uppercase;
  border: 1px solid transparent; letter-spacing: 0.05em;
}
.badge-red { background: var(--high-bg); color: var(--high-accent); border-color: var(--high-border); }
.badge-orange { background: var(--med-bg); color: var(--med-accent); border-color: var(--med-border); }
.badge-green { background: var(--success-bg); color: var(--success-border); border-color: var(--success-border); }
.badge-blue { background: var(--info-bg); color: var(--info-text); border-color: var(--info-border); }

/* === FINDINGS OVERRIDE === */
.finding { 
  padding: 24px 24px 24px 64px; 
  margin: 16px 0; 
  border: 2px solid var(--high-border); 
  background: var(--high-bg); 
  color: var(--high-text);
  position: relative;
}
.finding::before {
  content: "⚠";
  position: absolute; top: 0; left: 0; bottom: 0;
  width: 48px; background: var(--high-border); color: var(--bg);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.5rem; font-weight: bold;
}
.finding.warning { 
  border-color: var(--med-border); background: var(--med-bg); color: var(--med-text); 
}
.finding.warning::before {
  background: var(--med-border); content: "!"; color: var(--bg);
}
.finding.info { 
  border-color: var(--info-border); background: var(--info-bg); color: var(--info-text); padding-left: 24px; border-width: 1px;
}
.finding.info::before { display: none; }

.finding h4 { font-size: 1.125rem; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.finding h4 .badge { border: none; background: transparent; padding: 0; font-size: 0.875rem; }
.finding.warning h4 .badge, .finding.info h4 .badge, .finding h4 .badge { color: inherit; }
.finding p { font-size: 0.875rem; opacity: 0.9; line-height: 1.6; }

/* === STATS GRID === */
.stats-grid { 
  display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 32px; 
}
.stat-card { 
  border: 1px solid var(--border-light); background: var(--bg); padding: 24px; 
  display: flex; flex-direction: column; justify-content: center;
}
.stat-card .value { font-size: 3rem; font-weight: 300; letter-spacing: -0.05em; line-height: 1; margin-bottom: 8px; color: var(--text); }
.stat-card .label { font-size: 0.75rem; text-transform: uppercase; font-weight: 700; color: var(--text-muted); font-family: var(--font-mono); letter-spacing: 0.05em; }

/* Results Override for Severity */
#resultsContent .stats-grid .stat-card:nth-child(2) { border-color: var(--high-border); background: var(--high-bg); }
#resultsContent .stats-grid .stat-card:nth-child(2) .value { color: var(--high-accent); font-weight: 600; }
#resultsContent .stats-grid .stat-card:nth-child(2) .label { color: var(--high-text); }
#resultsContent .stats-grid .stat-card:nth-child(3) .value { font-weight: 600; }

/* === PROGRESS === */
.progress-bar { height: 4px; background: var(--border-light); overflow: hidden; margin: 16px 0; }
.progress-bar .fill { height: 100%; background: var(--text); transition: width 0.3s; }

.hidden { display: none !important; }

/* === MODAL === */
#nameModal { 
  position: fixed; inset: 0; background: rgba(0,0,0,0.8); backdrop-filter: blur(4px);
  display: flex; align-items: center; justify-content: center; z-index: 100; padding: 24px;
}
#nameModal .modal-content { 
  background: var(--bg); border: 1px solid var(--border-light); padding: 40px; 
  width: 100%; max-width: 480px; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}
#nameModal h2 { font-size: 1.5rem; margin-bottom: 12px; }
#nameModal input { 
  width: 100%; padding: 12px; border: 1px solid var(--border-light); background: var(--surface); color: var(--text);
  font-size: 1rem; margin: 24px 0; outline: none; transition: border-color 0.2s;
  font-family: inherit;
}
#nameModal input:focus { border-color: var(--text); }
#nameModal .note { font-size: 0.875rem; color: var(--text-muted); }

/* === EMPTY STATE === */
.empty-state { text-align: center; padding: 64px 24px; }
.empty-state .icon { font-size: 2.5rem; margin-bottom: 16px; opacity: 0.3; filter: grayscale(1); }
.empty-state p { color: var(--text-muted); font-size: 0.875rem; max-width: 400px; margin: 0 auto; }

/* === COMMUNITY LIST === */
.resident-row { display: flex; align-items: center; justify-content: space-between; gap: 16px; padding: 16px; border-bottom: 1px solid var(--border-light); flex-wrap: wrap; }
.resident-row:last-child { border-bottom: none; }
.resident-row .name { font-weight: 600; flex: 1; min-width: 120px; text-transform: uppercase; font-size: 0.875rem;}
.resident-row .amount { font-family: var(--font-mono); font-weight: 600; text-align: right; }

/* === PRINT STYLES === */
@media print {
  body { background: white !important; color: black !important; font-size: 11pt; }
  header, .tab-bar, .card, .stat-card, .finding { border: none !important; box-shadow: none !important; background: transparent !important; color: black !important; }
  header, .btn, .tab-bar, .graphic-banner { display: none !important; }
  #tab-results { display: block !important; }
  .finding { border: 1px solid black !important; border-left: 4px solid black !important; padding: 16px !important; margin: 12px 0 !important; }
  .finding::before { display: none !important; }
  .badge { border: 1px solid black !important; color: black !important; }
  table th { border-bottom: 2px solid black !important; color: black !important; }
  table td { border-bottom: 1px solid #ccc !important; }
  .stats-grid { display: grid !important; grid-template-columns: repeat(4, 1fr) !important; margin-bottom: 24px; gap: 16px; }
  .stat-card { border: 1px solid black !important; padding: 16px !important; }
  @page { margin: 1.5cm; }
}
</style>
</head>
<body>

<div id="app-wrapper">
  <header>
    <div class="container header-inner">
      <div class="brand">
        <h1>Newton Invoice Analyser</h1>
        <p>Balfour Park Residents — Billing Discrepancy Tool</p>
      </div>
      <div class="tab-bar">
        <button class="tab-btn active" onclick="showTab('upload')">Upload Engine</button>
        <button class="tab-btn" onclick="showTab('results')">Financial Ledger</button>
        <button class="tab-btn" onclick="showTab('community')">Community Data</button>
      </div>
    </div>
  </header>

  <main class="container">
    
    <!-- UPLOAD TAB -->
    <div id="tab-upload" class="tab-content active">
      <div class="card">
        <div class="graphic-banner"></div>
        <h2>Data Extraction Protocol</h2>
        <p>
          Drop your Newton Property Management PDF invoices below. This tool locally parses the documents in your browser, extracting billing anomalies and identifying potential overcharges. Zero data is sent to the cloud.
        </p>
        
        <div class="drop-zone" id="dropZone" onclick="document.getElementById('fileInput').click()">
          <div class="big">📄</div>
          <p>Drop PDF invoices here or click to select</p>
          <span>Accepts common charge invoices & outstanding balance notices</span>
        </div>
        <input type="file" id="fileInput" multiple accept=".pdf" style="display:none" onchange="handleFiles(this.files)">

        <div id="fileList" class="hidden" style="margin-top: 32px;">
          <h3>Queued Documents</h3>
          <table>
            <thead><tr><th>File</th><th>Status</th><th>Invoice #</th><th>Total</th></tr></thead>
            <tbody id="fileListBody"></tbody>
          </table>
          <div style="margin-top: 24px; display: flex; gap: 12px; flex-wrap: wrap;">
            <button class="btn btn-primary" onclick="analyseAll()">Commence Analysis</button>
            <button class="btn btn-outline" onclick="clearAll()">Clear Buffer</button>
          </div>
        </div>

        <div id="parseProgress" class="hidden" style="margin-top: 32px;">
          <p style="font-size: 0.875rem; font-family: var(--font-mono); font-weight: 600; text-transform: uppercase;">Crunching Document Matrices...</p>
          <div class="progress-bar"><div class="fill" id="progressFill" style="width: 0%"></div></div>
        </div>
      </div>

      <div class="card">
        <h2>What The Engine Detects</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-top: 24px;">
          <div style="display: flex; align-items: center; gap: 12px; font-size: 0.875rem;"><span class="badge badge-red">HIGH</span> Duplicate entries across invoices</div>
          <div style="display: flex; align-items: center; gap: 12px; font-size: 0.875rem;"><span class="badge badge-red">HIGH</span> Malicious debt collection fees</div>
          <div style="display: flex; align-items: center; gap: 12px; font-size: 0.875rem;"><span class="badge badge-orange">MEDIUM</span> Covert share ratio adjustments</div>
          <div style="display: flex; align-items: center; gap: 12px; font-size: 0.875rem;"><span class="badge badge-orange">MEDIUM</span> Costs inflated after "corrections"</div>
          <div style="display: flex; align-items: center; gap: 12px; font-size: 0.875rem;"><span class="badge badge-blue">INFO</span> Annual cost divergence from quote</div>
          <div style="display: flex; align-items: center; gap: 12px; font-size: 0.875rem;"><span class="badge badge-blue">INFO</span> Improper demands during dispute</div>
        </div>
      </div>
    </div>

    <!-- RESULTS TAB -->
    <div id="tab-results" class="tab-content">
      <div id="noResults" class="card">
        <div class="empty-state">
          <div class="icon">▤</div>
          <p>The ledger is empty. Supply your Newton PDF invoices to generate the financial discrepancy report.</p>
        </div>
      </div>
      <div id="resultsContent" class="hidden"></div>
    </div>

    <!-- COMMUNITY TAB -->
    <div id="tab-community" class="tab-content">
      <div class="card" style="border-top: 4px solid var(--border);">
        <h2>Community Intelligence</h2>
        <p>
          Isolate systemic overcharging by synthesizing data with your neighbours. Export your local ledger and import peer ledgers to expose broader patterns.
        </p>
        <div class="stats-grid" id="communityStats">
          <div class="stat-card"><div class="value" id="commResidents">0</div><div class="label">Total Residents</div></div>
          <div class="stat-card"><div class="value" id="commInvoices">0</div><div class="label">Invoices Scanned</div></div>
          <div class="stat-card"><div class="value" id="commFindings">0</div><div class="label">Anomalies Detected</div></div>
          <div class="stat-card"><div class="value" id="commAvgAnnual">-</div><div class="label">Mean Annual Cost</div></div>
        </div>

        <div style="display: flex; gap: 12px; margin-bottom: 8px; flex-wrap: wrap;">
          <button class="btn btn-primary" onclick="exportMyData()">Export My Ledger</button>
          <button class="btn btn-outline" onclick="document.getElementById('importInput').click()">Import Peer Ledger</button>
          <input type="file" id="importInput" accept=".json" style="display:none" onchange="importData(this.files[0])">
          <button class="btn btn-green" onclick="exportCommunityReport()">Export Global Report</button>
        </div>
      </div>

      <div class="card">
        <h2>Resident Database</h2>
        <div id="residentsList">
          <div class="empty-state">
            <div class="icon">☷</div>
            <p>No resident data present. Run your analysis and import neighbour files to populate this vector.</p>
          </div>
        </div>
      </div>

      <div class="card">
        <h2>Systemic Anomalies</h2>
        <div id="commonFindings">
          <div class="empty-state">
            <p>Cross-resident findings will calculate here post-import.</p>
          </div>
        </div>
      </div>
    </div>
  </main>
</div>

<!-- NAME MODAL -->
<div id="nameModal" class="hidden">
  <div class="modal-content">
    <h2>Identification Required</h2>
    <p class="note">Specify a resident alias to tag your data in the community view. This identifier never leaves your device unless explicitly exported to a peer.</p>
    <input type="text" id="residentName" placeholder="e.g. 14A Balfour Park" autofocus>
    <p class="note" style="margin-bottom: 24px;">Your Newton account number will be derived autonomously from the uploaded documents.</p>
    <button class="btn btn-primary" onclick="confirmName()" style="width: 100%;">Execute Analysis</button>
  </div>
</div>\n"""

final_content = new_html + js_content

with open("index.html", "w") as f:
    f.write(final_content)

print("Refactor complete.")
