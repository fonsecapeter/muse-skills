# skill-deps config

Machine values live in the fenced block below; `bin/map` reads them from here.

```yaml
# The one tree of personal skills to map (single tree since the
# 2026-11-05 consolidation). Directory names are normalized by
# stripping a leading local-/local_ prefix.
skills_dirs:
  - ~/workspace/custom-skills
# Directories that are not standalone skills (note folders, amendments).
exclude_dirs:
  - recovered-skill-notes
  - local-spaces
  - local_outbound_call_preflight
```
