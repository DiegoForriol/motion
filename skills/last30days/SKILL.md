# last30days

Summarize the user's activity over the last 30 days across Gmail, Google Calendar, and Google Drive.

## Trigger

Use this skill when the user asks for a recap, digest, summary, or review of the past month — phrases like "what happened in the last 30 days", "catch me up on last month", "what did I work on recently", or "give me a monthly summary".

## What it does

1. Queries Gmail for threads from the last 30 days (sent, received, important).
2. Queries Google Calendar for events in the same window.
3. Queries Google Drive for files created or modified in the last 30 days.
4. Synthesizes the data into a concise digest grouped by theme or project, highlighting key decisions, meetings, and deliverables.

## Tools used

| MCP server | Tools |
|---|---|
| Gmail | `search_threads`, `get_thread` |
| Google Calendar | `list_calendars`, `list_events` |
| Google Drive | `list_recent_files`, `search_files` |

## Instructions

### Date range

Compute the 30-day window from today's date (available in context as `currentDate`):
- `start`: 30 days before `currentDate` (ISO 8601, e.g. `2026-05-08`)
- `end`: `currentDate` (e.g. `2026-06-07`)

### Step 1 — Fetch calendar events

Call `list_calendars` to get the user's calendar IDs, then call `list_events` for each calendar with the date range. Collect event titles, dates, attendees, and any attached notes.

### Step 2 — Fetch email threads

Call `search_threads` with a query such as `after:<start_date> before:<end_date>` (Gmail date format: `YYYY/MM/DD`). Retrieve up to 20 representative threads (prioritize threads with multiple participants, labels like IMPORTANT or STARRED, and threads the user replied to). For each, call `get_thread` only when the subject alone is insufficient.

### Step 3 — Fetch Drive activity

Call `list_recent_files` to get recently modified files. Optionally call `search_files` with `modifiedTime > '<start_date>T00:00:00Z'` for a fuller picture.

### Step 4 — Synthesize

Group findings into sections such as:
- **Meetings & events** — key recurring meetings, one-offs, travel
- **Email highlights** — important threads, decisions made, action items
- **Documents & files** — files created or heavily edited
- **Themes & projects** — cross-cutting topics that appear across multiple sources

Keep the summary concise (under 400 words by default). Offer to drill into any section.

## Output format

```
## Last 30 days — <start_date> to <end_date>

### Meetings & events
...

### Email highlights
...

### Documents & files
...

### Themes & projects
...
```

## Privacy note

Never quote email body text verbatim unless the user explicitly asks. Summarize content; do not reproduce personal or sensitive details.
