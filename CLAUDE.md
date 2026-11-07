# noamschank.github.io

Personal academic website of Noam Schank (law student, Switzerland; fields:
constitutional law, legal methodology, legal theory, law and economics).
Owner is not a developer but knows GitHub: explain choices in plain words,
keep it simple.

## Stack
- Quarto website (`_quarto.yml`), built and deployed to GitHub Pages by
  `.github/workflows/publish.yml` on every push to main.
- Design: serif body (Source Serif 4), light and dark theme
  (`styles.scss`, `styles-dark.scss`), narrow text column, phone-first.
  No tracking, no cookies, no analytics, no JavaScript frameworks.
- Notes in `notes/*.qmd` appear automatically on the Notizen page, newest
  first, with an RSS feed. Template: `notes/_template.md`.
- Site language: German, with a short English bio on the home page.
- DOIs: `zenodo.py` runs in the publish workflow before rendering. A note
  with `zenodo: true` and no `doi:` is rendered to PDF (Quarto typst),
  deposited and PUBLISHED on Zenodo (licence cc-by-4.0, creator "Schank,
  Noam"), and the DOI is written back into its front matter and committed.
  Publishing on Zenodo is permanent: never set `zenodo: true` on a note
  yourself; only the owner does. Manual run with input zenodo=sandbox uses
  sandbox.zenodo.org (ZENODO_SANDBOX_TOKEN), also handles `draft: true`
  notes, and never writes sandbox DOIs back. `notes/_metadata.yml` adds a
  citation box and Google Scholar meta tags to every note.
- `website: draft-mode: gone` keeps `draft: true` notes off the site.

## Status (2026-11-07)
- v1 built and tested locally (phone + desktop, light + dark).
- Placeholders marked `.todo` (yellow boxes) on index, publications, teaching.
- `noindex` meta tag in `_quarto.yml` keeps search engines away until the
  owner has filled in the texts. Remove it (and say so) only when he asks.

## Rules
- Owner writes all texts. Never invent biography, affiliations,
  publications or claims. Leave a clear TODO where text is missing.
- Don't publish photos of the owner unless he adds them himself.
- A custom domain may be added later via a CNAME file; don't add one now.
- Must not depend on any claude.ai account feature. Everything is in this repo.
