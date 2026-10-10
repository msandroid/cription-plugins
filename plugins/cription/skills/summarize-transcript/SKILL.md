---
name: summarize-transcript
description: Turn a transcript (from transcribe_audio, a Cription note, or pasted text) into meeting minutes, interview findings, lecture notes or a sales-call summary, using the same section templates as the Cription app. Use when the user asks for minutes, a summary, action items, or next steps from a recording.
---

# Summarize a transcript the Cription way

Cription's app summarizes notes with five templates. Use the one that fits (ask only if unclear), write in the transcript's language unless the user asks otherwise, and keep each bullet short and concrete.

| Template | Sections (English) | Sections (日本語) |
|---|---|---|
| General | Overview · Key points · Decisions · Next steps | 概要 · 要点 · 決定事項 · 次のステップ |
| Meeting | Overview · Decisions · Action items · Open issues | 概要 · 決定事項 · ToDo · 未決事項 |
| Interview | Overview · Key findings · Notable quotes · Follow-up questions | 概要 · 主な発見 · 印象的な発言 · 追加で聞くこと |
| Lecture | Overview · Key concepts · Important details · Review questions | 概要 · 重要な概念 · 大事な詳細 · 復習問題 |
| Sales call | Overview · Customer needs · Concerns and objections · Next steps | 概要 · 顧客のニーズ · 懸念と反論 · 次のステップ |

## Rules

- **Overview**: at most 3 bullets.
- **Action items / Next steps**: one line each as `- [ ] <task> — <owner>（<due date>）`; write `owner: unknown` rather than guessing.
- Only include what was actually said. Mark uncertain readings (ASR errors, numbers, names) with `(?)` and the `[mm:ss]` timestamp so the user can check.
- On-device ASR mishears homophones and numbers; fix obvious ones from context, but never invent figures.
- Output Markdown with `###` headings. Offer to save it to a file or turn action items into tasks/issues if the user has those tools.

## Sources

- A file: run the `transcribe` skill first.
- A Cription note: `search_notes` / `list_notes`, then `get_note`. If the note already has a `summary`, start from it and fill gaps from the transcript.
