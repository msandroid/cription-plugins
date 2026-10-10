---
name: cription-notes
description: Search and read the user's Cription recordings (meetings, lectures, interviews, voice notes) stored on their Mac. Use when the user asks about something they recorded with Cription — "what did we decide last week", "find the call with Sato", "my lecture notes on X".
---

# Use the user's Cription notes

The **cription** MCP server reads the notes the Cription Mac app keeps locally (read-only).

## Finding notes

- `search_notes(query)` matches titles, summaries, transcripts and memos. Search with distinctive words in the recording's language (Japanese works). Try synonyms or names if nothing matches.
- `list_notes(since="YYYY-MM-DD", folder=...)` for time-based questions ("last week", "yesterday's meeting"). Convert relative dates using today's date.
- `list_folders` shows how the user organizes notes.

## Reading

- `get_note(id)` returns the transcript with `[mm:ss]` timestamps and speaker names, plus the app's summary, checked to-dos, memos and bookmarks.
- Answer the question and cite the note title, date and timestamps. Do not paste whole transcripts unless asked.
- Transcripts are private recordings of real conversations: quote only what the task needs, and do not send them to other services unless the user asks.

## Limits

- Only notes on this Mac are visible. Notes recorded on iPhone appear once they are on the Mac.
- A note recorded seconds ago may not show yet (the app writes its store lazily); ask the user to wait or reopen the app.
- `cription_status` shows which note stores were found.
