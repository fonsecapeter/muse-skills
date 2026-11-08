# todo-file config

Machine values for creating todos. Read at run time — never hardcode
these in prose.

```json
{
  "notion_api": "~/workspace/custom-skills/notion/bin/notion-api",
  "todo_database_id": "8ca2abf0828642019c4747d69eb65a71",
  "projects_database_id": "db1d8746-4de1-4cd9-9cf6-9c44accbfa89"
}
```

Notes:
- `notion_api` is the notion skill's CLI — this skill defers all
  Notion access to it (declared in SKILL.md Dependencies).
