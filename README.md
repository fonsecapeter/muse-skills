# muse-skills

My personal skills for Muse — Meta's personal AI agent — collected
as a repo. Skills are grouped in bucket folders here and symlinked
flat into Muse's custom-skills folder, so this repo is the source
of truth and the live tree is just links.

These skills are written for Muse (personal). They are **not
tested in Muse Code**.

## Layout

- `manifest.json` — the roster: every skill in the bundle, by name
  and bucket. `bin/link-skills` links exactly what it lists, so
  unlisted folders (drafts, retired skills) never reach the live
  tree.
- `simi/`, `gtd/`, `code/`, `life/`, `studio/` — the buckets.
- `SYSTEM.md` — how the buckets fit together. Each bucket's
  internals live with the bucket (e.g. `gtd/SYSTEM.md` is the GTD
  system map).
- `.python-version` — the Python the repo tooling runs on
  (pyenv).
- `bin/link-skills` — create or refresh the symlinks in the
  destination folder (default `~/workspace/custom-skills`);
  `--check` reports drift without changing anything.
- `bin/verify` — check that the repo and the live links agree with
  the roster.
- `bin/test` — run the tooling tests.

## A note on content

Skills here carry mechanism, never personal content: no
credentials, no account data, no todo lists. Anything sensitive
lives in Muse's credential store, not in a skill.
