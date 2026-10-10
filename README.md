# Cription for Claude, Codex & other AI agents

On-device transcription and your Cription notes, available to AI coding agents and assistants through **plugins** and **skills**. The MCP server lives in [msandroid/cription-mcp](https://github.com/msandroid/cription-mcp).

- 🎙️ **Transcribe** local audio and video files with Apple's on-device SpeechAnalyzer (the engine Cription uses for its best-scoring languages, e.g. Japanese).
- 📝 **Summarize** transcripts into minutes, interview findings, lecture notes or sales-call summaries with Cription's templates.
- 🔎 **Search and read** the notes you recorded with the Cription Mac app (read-only).
- 🔒 **Private**: everything runs on your Mac. No audio, transcript or note is sent anywhere by this server.

[日本語は下にあります](#日本語)

## Requirements

- macOS 26 or later (for transcription; notes work on older macOS)
- Python 3.9+ (`python3`, bundled with the Xcode Command Line Tools)
- Xcode Command Line Tools (`xcode-select --install`) — the small Swift helper is compiled once on first use
- [`uv`](https://docs.astral.sh/uv/) (`brew install uv`) — the plugin starts the MCP server with `uvx`

## Install

### Claude Code (plugin: MCP server + skills)

```
/plugin marketplace add msandroid/cription-plugins
/plugin install cription@cription
```

### Codex

Skills (plugin):

```bash
codex plugin marketplace add msandroid/cription-plugins
```

Then open `/plugins` in Codex and install **cription**. Add the MCP server:

```bash
codex mcp add cription -- uvx --from git+https://github.com/msandroid/cription-mcp cription-mcp
```

### Claude Desktop

Easiest: download `cription-<version>.mcpb` from [cription-mcp Releases](https://github.com/msandroid/cription-mcp/releases) and double-click it (or drag it into Claude → Settings → Extensions).

Or add to `~/Library/Application Support/Claude/claude_desktop_config.json` and restart Claude:

```json
{
  "mcpServers": {
    "cription": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/msandroid/cription-mcp", "cription-mcp"]
    }
  }
}
```

Use the absolute path to `uvx` (`which uvx`) if Claude cannot find it.

### Cursor and other MCP clients

`.cursor/mcp.json` (or your client's equivalent):

```json
{
  "mcpServers": {
    "cription": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/msandroid/cription-mcp", "cription-mcp"]
    }
  }
}
```

Without `uv`: see [cription-mcp](https://github.com/msandroid/cription-mcp#without-uv).

## Tools

| Tool | What it does |
|---|---|
| `transcribe_audio` | Audio/video file → transcript with `[mm:ss]` timestamps. Options: `locale` (e.g. `ja-JP`), `terms` (names/jargon to spell right), `timestamps`, `save_to`. Long transcripts are saved to a file. |
| `speech_languages` | Locales the on-device engine supports and has installed. |
| `list_notes` | Your Cription notes, newest first (`limit`, `folder`, `since`). |
| `search_notes` | Full-text search over titles, summaries, transcripts and memos. |
| `get_note` | One note: transcript with speakers, summary, to-dos, memos, bookmarks. |
| `list_folders` | Note folders and counts. |
| `cription_status` | What this Mac supports and which note stores were found. |

## Skills

| Skill | Use |
|---|---|
| `transcribe` | Transcribing a file well: locale, terms, long recordings. |
| `summarize-transcript` | Cription's five summary templates (General, Meeting, Interview, Lecture, Sales call). |
| `cription-notes` | Answering questions from your recordings with citations. |

## Examples

- "Transcribe ~/Downloads/standup.m4a and list the action items with owners."
- "このインタビュー動画（~/Movies/interview.mov）を文字起こしして、印象的な発言を5つ挙げて"
- "What did we decide about pricing in last week's Cription notes?"

## Privacy

The server only reads files you ask it to transcribe and the Cription app's local preferences (`~/Library/Preferences/Cription.plist` or the app container). It writes only its compiled helper and long transcripts under `~/Library/Caches/cription-mcp` (or the plugin data folder). The AI client you use decides what it does with the results.

## Limits

- Supported transcription languages are Apple's SpeechAnalyzer locales (`speech_languages`). Cription the app supports more languages with additional engines.
- No speaker diarization in `transcribe_audio` yet; notes recorded in the app keep their speaker labels.
- Notes recorded on iPhone are visible only once they are on the Mac.

---

## 日本語

Cription の**オンデバイス文字起こし**と**ノート**を、Claude Code・Claude Desktop・Codex・Cursor などの AI エージェントから使えるようにする MCP サーバーとプラグインです。

- **文字起こし**：手元の音声・動画ファイルを Apple SpeechAnalyzer でオンデバイスで文字起こしします（日本語で Cription が最も精度の高いエンジン）。
- **要約**：Cription アプリと同じテンプレート（一般・会議・インタビュー・講義・商談）で議事録にします。
- **ノート検索**：Cription の Mac アプリで録音したノートを読み取り専用で検索・参照します。
- **プライバシー**：すべて Mac の中で処理し、音声・文字起こし・ノートを外部に送りません。

必要なもの：macOS 26 以降（文字起こし）、Xcode Command Line Tools（初回に小さな Swift ヘルパーをビルドします）、`uv`。MCP サーバー本体は [cription-mcp](https://github.com/msandroid/cription-mcp) にあります。

インストール方法は上の [Install](#install) を参照してください。Claude Code なら次の2行です。

```
/plugin marketplace add msandroid/cription-plugins
/plugin install cription@cription
```

## License

MIT
