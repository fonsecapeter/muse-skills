---
name: "studio1way-add-project"
description: "Add a new art project to Peter's Studio 1Way website: run the intake with Peter, then delegate the mechanics to the repo's own add-project skill in the studio1way repo. Use whenever Peter wants to add a piece to the site, sends photos of new work for the portfolio, or says 'put this on the website'."
---

# Add a Studio 1Way project

New pieces go on https://www.studio1way.com.

For the project format, the per-category fields and enums, the ask
list, and the `scripts/scaffold-project` + `scripts/check-project`
tooling, read and follow the repo skill at
`~/projects/studio1way/.agents/skills/add-project/SKILL.md` — the
tooling parses the enums from the Java models, so it cannot drift.

## Peter's rules (on top of the repo skill)

- **Description is Peter's, verbatim.** Curated; never draft, polish,
  or guess one. If he has not provided it, ask and hold the project
  until he does.
- **Ask once, in one message**, for every field he did not mention —
  the repo skill's ask list for the category, description first if
  missing. Do not drip one question per field.
- **Name is his title**, exactly as he gives it.
- **Draft alt text and image names from the photos** (actually look at
  them) and include the drafts in the ask message; he approves or
  edits.
- **Hand over via the PR**: the project JSON plus CI's preview
  screenshots on the PR are his review surface — local dev-server
  previews don't work from this machine.

## This machine's quirks

- Repo: `~/projects/studio1way` (values in `config.md`). Invoke the
  repo skill's scripts with `python3 <path>` so their executable bits
  do not matter after API pushes.
- ImageMagick: Ubuntu's package is IM6 (`convert`); the repo's
  `bin/resize-img` calls `magick`. A shim at `~/workspace/tools/bin`
  covers the name — put it on PATH (`config.md`'s `extra_path`) when
  running the scaffolder. If `magick` vanishes after a VM swap,
  reinstall via `~/workspace/tools/apt/install.sh`.
- Backend tests as the final gate: the repo's `bin/native/test` with
  the JDK/Node toolchains on PATH; the full sandbox recipe is in
  `~/TOOLS.md` ("Java / Node native builds on this VM").

## Shipping

- Project commits follow the repo's pattern: `Add <name lowercase>`.
- Merging to main deploys the site — that click is Peter's.

## Dependencies

- learning-loop (bin/record-learning) — learning loop

## Learning loop

Owned by the learning-loop skill (see Dependencies). Record with
`~/workspace/custom-skills/learning-loop/bin/record-learning studio1way-add-project "<learning>"`.

## Available connectors

- [GitHub](/opt/hatch/connectors/github/CONNECTOR.md) for pushing the branch and opening the PR.

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.
