# Newton Invoice Analyser

Community billing discrepancy tool for Balfour Park residents (Newcraighall, Edinburgh) to analyse invoices from Newton Property Management.

## What it does

- Parses Newton Property Management PDF invoices entirely in-browser (no data leaves your device)
- Detects duplicate billing entries across invoices
- Flags debt collection fees being passed to homeowners
- Identifies share ratio changes (e.g. 1/32 → 1/191)
- Calculates annualised costs vs the quoted ~£110/year
- Community features: export/import data to build a collective case with neighbours

## Tech

Single-page static HTML app using [pdf.js](https://mozilla.github.io/pdf.js/) for client-side PDF parsing. No backend, no database, no tracking. Community data stored in localStorage.

## Live

[newton-property-sucks.cloud-native.cool](https://newton-property-sucks.cloud-native.cool)

## Legal context

This tool supports Scottish homeowners in exercising their rights under the Property Factors (Scotland) Act 2011 and the Code of Conduct for Property Factors.
