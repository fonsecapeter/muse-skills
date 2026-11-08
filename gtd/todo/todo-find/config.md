# todo-find config

Machine values for `bin/find-todo`. The script reads the fenced JSON
block at run time — never hardcode these in scripts or prose.

```json
{
  "notion_api": "~/workspace/custom-skills/notion/bin/notion-api",
  "todo_database_id": "8ca2abf0828642019c4747d69eb65a71",
  "todo_actions_url": "https://www.notion.so/8ca2abf0828642019c4747d69eb65a71"
}
```

Notes:
- `notion_api` is the notion skill's CLI — this skill defers all
  Notion access to it (declared in SKILL.md Dependencies).
- `todo_actions_url` points at the TODO database; Peter confirmed the
  database link is fine, no specific view needed.
