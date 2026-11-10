# todo-update config

Machine values for `bin/check-item`. The script reads the fenced JSON
block at run time — never hardcode these in scripts or prose.

```json
{
  "notion_api": "~/workspace/custom-skills/notion/bin/notion-api"
}
```

Notes:
- `notion_api` is the notion skill's CLI — this skill defers all
  Notion access to it (declared in SKILL.md Dependencies).
