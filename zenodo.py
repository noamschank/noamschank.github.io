"""Give site notes a DOI on Zenodo.

A note gets a DOI only if its front matter says `zenodo: true` and it has no
`doi:` yet. The script makes a PDF of the note, uploads it to Zenodo,
publishes it, and writes the DOI back into the note's front matter.

Publishing on Zenodo is permanent. That's why it's opt-in per note.

  python zenodo.py             real Zenodo (needs ZENODO_TOKEN)
  python zenodo.py --sandbox   practice copy at sandbox.zenodo.org
                               (needs ZENODO_SANDBOX_TOKEN); also handles
                               notes marked `draft: true`, so you can test
                               without the note appearing on the site
  python zenodo.py --dry-run   show what would happen, change nothing
"""

import os
import re
import subprocess
import sys
from pathlib import Path

import requests
import yaml

HERE = Path(__file__).parent
NOTES = HERE / "notes"
SITE = "https://noamschank.github.io"
CREATOR = {"name": "Schank, Noam"}
LICENSE = "cc-by-4.0"  # change here if you want another licence

FM = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def front_matter(path):
    m = FM.match(path.read_text(encoding="utf-8"))
    return (yaml.safe_load(m.group(1)) or {}) if m else {}


def write_doi(path, doi):
    text = path.read_text(encoding="utf-8")
    m = FM.match(text)
    block = m.group(1).rstrip("\n") + f'\ndoi: "{doi}"'
    path.write_text(f"---\n{block}\n---\n" + text[m.end():], encoding="utf-8")


def candidates(sandbox):
    for p in sorted(NOTES.glob("*.qmd")):
        if p.name.startswith("_") or p.name == "index.qmd":
            continue
        fm = front_matter(p)
        if fm.get("zenodo") is not True or fm.get("doi"):
            continue
        if fm.get("draft") and not sandbox:
            continue  # drafts are only for sandbox tests
        yield p, fm


def make_pdf(path):
    subprocess.run(["quarto", "render", str(path), "--to", "typst",
                    "--output-dir", "_zenodo"], check=True, cwd=HERE)
    # Inside the site project Quarto keeps the folder structure (_zenodo/notes/…).
    found = list((HERE / "_zenodo").rglob(path.stem + ".pdf"))
    if not found:
        raise FileNotFoundError(f"PDF for {path.name} not found")
    return found[0]


def deposit(path, fm, pdf, base, token):
    auth = {"Authorization": f"Bearer {token}"}
    web = f"{SITE}/notes/{path.stem}.html"

    r = requests.post(f"{base}/api/deposit/depositions", json={}, headers=auth, timeout=60)
    r.raise_for_status()
    dep = r.json()

    with open(pdf, "rb") as f:
        r = requests.put(f"{dep['links']['bucket']}/{pdf.name}", data=f, headers=auth, timeout=120)
    r.raise_for_status()

    meta = {
        "title": fm["title"],
        "upload_type": "publication",
        "publication_type": "other",
        "description": (fm.get("description") or fm["title"])
                       + f'<p>Web version: <a href="{web}">{web}</a></p>',
        "creators": [CREATOR],
        "publication_date": str(fm.get("date"))[:10],
        "access_right": "open",
        "license": LICENSE,
        "language": fm.get("lang", "deu"),
    }
    if fm.get("keywords"):
        meta["keywords"] = list(fm["keywords"])
    r = requests.put(f"{base}/api/deposit/depositions/{dep['id']}",
                     json={"metadata": meta}, headers=auth, timeout=60)
    if r.status_code >= 400:
        raise RuntimeError(f"metadata rejected: {r.text[:500]}")

    r = requests.post(f"{base}/api/deposit/depositions/{dep['id']}/actions/publish",
                      headers=auth, timeout=120)
    if r.status_code >= 400:
        raise RuntimeError(f"publish rejected: {r.text[:500]}")
    return r.json()["doi"]


def main():
    sandbox = "--sandbox" in sys.argv
    dry = "--dry-run" in sys.argv
    base = "https://sandbox.zenodo.org" if sandbox else "https://zenodo.org"
    token = os.environ.get("ZENODO_SANDBOX_TOKEN" if sandbox else "ZENODO_TOKEN")

    todo = list(candidates(sandbox))
    if not todo:
        print("No notes waiting for a DOI.")
        return
    if not token and not dry:
        print("No Zenodo token set; skipping:", ", ".join(p.name for p, _ in todo))
        return

    for path, fm in todo:
        if dry:
            print("Would deposit:", path.name, "-", fm.get("title"))
            continue
        pdf = make_pdf(path)
        doi = deposit(path, fm, pdf, base, token)
        print(f"{path.name}: {doi}" + (" (sandbox)" if sandbox else ""))
        if not sandbox:
            write_doi(path, doi)  # sandbox DOIs are fake; never write them back


if __name__ == "__main__":
    main()
