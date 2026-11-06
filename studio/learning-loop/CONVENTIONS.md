# Skill Conventions

Canonical conventions for Peter's personal skills (the muse-skills
repo, symlinked into `~/workspace/custom-skills/`).
Owned by the learning-loop skill; enforced by its nightly audit.
**Follow these while drafting and while editing — every version complies,
not just the first.** The nightly sweep audits for drift; it is not a
substitute for following the conventions.

## Structure

- **Playbook in `SKILL.md`.** Agentic judgment and prose live here.
- **Machine values in `config.md`.** A fenced block (yaml or json); scripts
  read it at run time. Never hardcode machine values in scripts or prose.
- **Auth/connection knowledge in `CONNECTION.md`.** How the skill connects,
  what the credentials are called, where they live.
- **Deterministic work in `bin/` CLIs.** Script every deterministic part
  wherever possible — counting rows, filtering, parsing, API calls with
  fixed shapes. Prose is for judgment, not for counting. CLIs read their
  config from `config.md` at run time, never from hardcoded values.
- **CLIs fail loudly.** Every `bin/` CLI exits non-zero with a stderr
  message on any failure, and validates its results (return code + parsed
  fields) before claiming success. Never print success from an
  unvalidated parse or an error body. Silent failure is the worst kind —
  evidence: four simi-claims incidents of silent failure (Oct 8–9, 2026)
  hid a full cycle of bad data before anyone noticed.
- **Duplicate CLI copies stay in sync.** If the same `bin/` CLI exists
  in more than one place (across skills, or a skill and a
  custom-connector), a fix to one copy is incomplete until all copies
  match or defer to the canonical one. The nightly sweep audit diffs
  duplicate copies. Evidence: the 2026-10-14 notion-api fix repaired
  only the canonical skill copy, leaving the connector copy on a
  deleted path until that night's sweep found and fixed it.
- **Crons are one-liners.** A cron body invokes the skill
  (`Run the <name> skill: follow ~/workspace/custom-skills/<name>/SKILL.md ...`).
  The playbook lives in the skill, never in the cron.

## One skill tree — the repo (moved 2026-11-06, Peter's call)

- The source of truth is the **muse-skills repo**
  (`~/projects/muse-skills`, github.com/fonsecapeter/muse-skills):
  skills live in bucket folders there, under bare names (the
  `local-` prefix was dropped in the move). `manifest.json` is the
  roster of what exists.
- The live tree `~/workspace/custom-skills/` holds **symlinks** into
  the repo, made by the repo's `bin/link-skills` — exactly the
  roster, flat. Edit a skill in the repo checkout (editing through
  the symlink is the same file), never in a separate copy.
- New skills are created in the repo: draft in a bucket, add the
  roster entry, run `bin/link-skills` (see the new-skill skill).
- Never recreate a second tree or a mirrored copy. If a skill
  moves, move it — and update every cron body, config pointer, and
  dependency line in the same change (skill-deps `bin/map` verifies
  the graph).

## Public repo — nothing sensitive in a skill (Peter's call, 2026-11-05)

- The skills live in a public git repo (fonsecapeter/muse-skills).
  Anything written into a skill — playbook, config, test fixture,
  learning — is public.
- Skills carry mechanism, not content or secrets. Credentials belong in
  the credential store; personal data and private identifiers belong in
  the systems a skill points at, not in the skill itself.
- Use judgment about what counts as sensitive. When in doubt, leave it
  out or ask Peter.

## Durable rules — placement + trigger

- **A rule fails when it is passive background knowledge in the wrong
  place.** Every durable rule must (a) live in the skill named for the
  task it governs — not as fine print in an adjacent skill — and
  (b) bind to an automatic, recognizable trigger or a deterministic
  check, not to recall. If there is no trigger, give it one (a CLI
  check, a named chat signal, a sweep audit) or expect it to miss.
- Evidence: the completion-signal rule sat in notion fine print and
  missed twice (2026-10-06 checkbook, 2026-10-13 Xfinity) until it
  moved to the todo skill, keyed to a chat completion report; the
  recording protocol existed but needed Peter to ask (2026-10-13)
  until a correction from Peter was made its automatic trigger; the
  simi silent failures (Oct 8–9, 2026) ended only when CLIs were made
  to fail loudly and validate deterministically.

## Declarations

- **Dependencies are declared, not discovered.** Every skill has a
  `## Dependencies` section in SKILL.md, one line per dep:
  `- <skill> (<cli-path>) — <why>`. External things (built-in skills,
  wallet, browser) marked `(external ...)`. If a skill calls another
  skill's CLI, it must be declared here. The `skill-deps` skill maps them
  (`bin/map` → tree + mermaid, verifies targets exist, flags undeclared
  cross-refs).
- **Skills defer to each other through their CLIs.** If a skill needs
  another service, it calls that skill's CLI instead of reimplementing
  auth or requests (e.g. gtd-weekly-review → notion's `bin/notion-api`).

## Learning loop

- A `## Learning loop` section deferring to the learning-loop skill,
  exactly like the existing custom skills. Record learnings the moment they
  surface: `~/workspace/custom-skills/learning-loop/bin/record-learning
  <skill-name> "<learning>"`. A correction from Peter is an automatic
  trigger — record it in the same turn, unprompted.
- The nightly sweep implements pending learnings into the skills, moves
  each implemented learning into the central learned log (learning +
  change + skill id), then clears the pending entries. It also reviews
  recent learned entries for broader patterns and audits every skill
  against this file.

## Standing rules

- **Read-only by default.** Counting and reading are fine; writing to
  Peter's systems needs his explicit ask.
- **Custom skills only.** Never edit bundled skills under
  `/opt/muse/skills/`.
- **Small, composable, reusable, short, focused.** One skill, one job.
