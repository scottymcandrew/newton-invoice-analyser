# Newton Invoice Analyser

## Cursor Cloud specific instructions

### Overview

Zero-dependency static HTML site. All HTML, CSS, and JavaScript live in a single `index.html` file. No package manager, no build step, no backend.

### Running the dev server

```bash
python3 -m http.server 8080
```

Serves the site from the repo root. Open `http://localhost:8080` in Chrome.

### Key caveats

- **No linter/tests/build:** The project has no `package.json`, no test framework, and no lint configuration. There is nothing to run for lint, test, or build commands.
- **CDN dependency:** `pdf.js` is loaded from `cdnjs.cloudflare.com` at runtime. Internet access is required for the app to parse PDFs.
- **No sample invoices in repo:** The app parses Newton Property Management PDF invoices. No sample PDFs are included; you must create or supply one for testing (see `refactor.py` for the expected HTML structure).
- **localStorage only:** All data is stored in the browser's `localStorage`. Clearing browser data resets everything.
- **Vercel deployment:** `vercel.json` configures clean URLs and security headers for production. The Vercel CLI is optional and only needed for deployment testing.
