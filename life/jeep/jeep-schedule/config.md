# jeep-schedule config

Machine values for `bin/jeep-maintenance`. The script reads the fenced JSON block.

```json
{
  "spreadsheet_id": "1IoBZnpmLEUxXw-nWoTy1Uf0oIRFo1Lftfccpj0zkQg4",
  "sheets_cli": "/opt/hatch/bin/hatch_gws_cli",
  "info_tab": "Info",
  "oil_tab": "Oil Changes",
  "other_tab": "Other",
  "notion_api": "~/workspace/custom-skills/notion/bin/notion-api",
  "notion_todo_database_id": "8ca2abf0828642019c4747d69eb65a71",
  "jeep_project_id": "c8cb4652-9497-4605-a8c4-2326d20ef04c",
  "closed_statuses": ["Done", "Not Doing"],
  "due_soon_miles": 1000,
  "due_soon_days": 30,
  "oil_interval_miles": 7000,
  "oil_interval_months": 12,
  "timezone": "America/Los_Angeles",
  "horizon_end": "2027-12-31"
}
```

`horizon_end` is how far ahead the schedule is planned (see SKILL.md).
The check warns in its output once that date has passed.
