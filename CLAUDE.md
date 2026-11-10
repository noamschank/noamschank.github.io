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
- Languages: German at the root, French in `fr/`, English in `en/` (pages: index,
  cv, publications, teaching). Notizen and Stellungnahmen are German only.
  `lang.html` (tiny script) relabels the navbar and points DE/FR/EN to the
  same page in the other language; without JS the site works in German.
  Keep the three language versions of a page in step when editing.
- `project.render` lists only `*.qmd` files, so CLAUDE.md and README.md are
  never published.
- Teaching materials: PDFs go in `materialien/` and are linked from
  `teaching.qmd` (and fr/en versions).
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
- `website: search: false`: no search bar (owner's choice, 2026-11-10).

## Status (2026-11-09)
- Content filled in from the owner's CV and approved by him in chat:
  bio (first person), CV, two articles, NZZ and Wikimedia CH interviews,
  hobbies, email and LinkedIn. Portrait in `images/portrait.jpg`, supplied
  by the owner for the site.
- `noindex` removed at the owner's request; the site is meant to be found.
- Tutorial listed as University of Fribourg, taught in German: unconfirmed.
- Notizen and Stellungnahmen are hidden (excluded in `project.render`,
  navbar entries commented out) until the owner has content for them.

## Rules
- Owner writes all texts. Never invent biography, affiliations,
  publications or claims. Leave a clear TODO where text is missing.
- Don't publish photos of the owner unless he supplies them himself.
- Custom domain: noamschank.com (registrar green.ch). `CNAME` file and
  `site-url` set; the domain itself is set in GitHub → Settings → Pages.
- Must not depend on any claude.ai account feature. Everything is in this repo.
