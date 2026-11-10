# GTD review — config

Machine-readable values are in the `json` block below; `bin/gtd-counts`
reads them from this file. Edit the values here, not in the script.

```json
{
  "google_tasks_lists": ["Intake", "Inventory"],
  "notion_api": "~/workspace/custom-connectors/custom.legacy-notion/bin/notion-api",
  "notion_todo_database_id": "8ca2abf0828642019c4747d69eb65a71",
  "closed_statuses": ["Done", "Not Doing"],
  "notion_todo_url": "https://www.notion.so/8ca2abf0828642019c4747d69eb65a71",
  "notion_actions_view_url": "https://www.notion.so/8ca2abf0828642019c4747d69eb65a71"
}
```

`notion_actions_view_url` points at the TODO database — Peter confirmed the
database link is fine, no specific view needed.
