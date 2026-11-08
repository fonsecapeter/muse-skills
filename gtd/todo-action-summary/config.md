# todo-action-summary config

Machine values for `bin/todo-summary`. The script reads the fenced JSON block.

```json
{
  "notion_api": "~/workspace/custom-connectors/custom.legacy-notion/bin/notion-api",
  "notion_todo_database_id": "8ca2abf0828642019c4747d69eb65a71",
  "closed_statuses": ["Done", "Not Doing"],
  "notion_actions_view_url": "https://www.notion.so/8ca2abf0828642019c4747d69eb65a71",
  "timezone": "America/Los_Angeles",
  "stale_days": 30
}
```

`notion_actions_view_url` points at the TODO database — Peter confirmed the
database link is fine, no specific view needed.
