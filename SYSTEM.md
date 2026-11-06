# How the buckets fit together

Peter's skills for Muse live in this repo, grouped in bucket
folders and symlinked flat into Muse's custom-skills folder —
`manifest.json` is the roster, `bin/link-skills` makes the links.

This file maps the boundaries between buckets. Each bucket owns
its internals: how an area works is documented with the bucket,
not here.

## The buckets

- **gtd/** — capture → commitments → follow-through: Google Tasks
  intake, the Notion TODO database, and the digests that surface
  what's due. The GTD system map lives at `gtd/SYSTEM.md`.
- **simi/** — Simi's Nationwide pet-insurance claims: staging vet
  invoices and tracking filings.
- **code/** — writing and shipping code: Peter's repos and
  Studio 1Way.
- **life/** — recurring real-world routines: appointments, inbox
  triage, vehicle maintenance.
- **studio/** — the skills system itself: how skills are written,
  what they depend on, and how they learn from corrections.

## Boundaries

- The repo is the source of truth; the live tree is symlinks into
  it. Nothing about a skill's behavior lives only in the live
  tree.
- Skills defer to each other through their `bin/` CLIs instead of
  reimplementing each other, and declare it in their Dependencies.
- A bucket's internals — its data, cadences, and conventions —
  stay inside the bucket. Cross-bucket facts live at the boundary
  they cross.
